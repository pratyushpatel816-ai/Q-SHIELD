"""Deterministic validation harness for Q-SHIELD impersonation controls.

This harness validates the identity and payload-binding layers without requiring
Qiskit. It deliberately separates three cases:

1. Legitimate registered sender -> ACCEPT at identity layer.
2. Unknown sender -> REJECT as IMPERSONATION_ATTEMPT.
3. Registered sender disabled -> REJECT as IMPERSONATION_ATTEMPT.
4. Sender field changed after a payload was bound to a signature hash ->
   MESSAGE_TAMPERING at the payload-binding layer.

The fourth case is not a cryptographic identity proof: it checks that the
current SHA-256 payload binding detects alteration of the sender field.
This is component-level validation, not an end-to-end QDS security proof.
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from qshield.security.identity import IdentityRegistry  # noqa: E402

OUTPUT_DIR = Path(__file__).resolve().parent / "results"
CSV_PATH = OUTPUT_DIR / "impersonation_validation_results.csv"
SUMMARY_PATH = OUTPUT_DIR / "impersonation_validation_summary.json"

SCENARIOS = (
    "legitimate_registered_sender",
    "unknown_sender",
    "revoked_sender",
    "sender_field_tampering",
)


def make_payload(sender_id: str, sequence_no: int) -> dict:
    now = datetime.now(timezone.utc)
    return {
        "sender_id": sender_id,
        "receiver_id": "TRAFFIC_GATEWAY_01",
        "device_id": "SMART_TRAFFIC_GATEWAY_01",
        "command": "AUTHORIZE_FIRMWARE_UPDATE",
        "firmware_hash": "firmware_sha256_placeholder",
        "nonce": f"nonce-{sequence_no}",
        "session_id": f"session-{sequence_no}",
        "timestamp": now.isoformat(),
        "expiry": now.isoformat(),
        "sequence_no": sequence_no,
    }


def hash_payload(payload: dict) -> str:
    # Same canonicalization contract as qshield.protocol.payload.CanonicalPayload:
    # sorted keys, compact separators, UTF-8 SHA-256. Kept local so this
    # component-level harness does not require the quantum/Qiskit stack.
    canonical = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def result_row(trial: int, scenario: str, expected: str, actual: str, rule_id: str,
               evidence: dict | None = None) -> dict:
    passed = expected == actual
    return {
        "trial": trial,
        "scenario": scenario,
        "expected_decision": expected,
        "actual_decision": actual,
        "rule_id": rule_id,
        "passed": passed,
        "evidence": json.dumps(evidence or {}, sort_keys=True),
    }


def run_trial(trial: int) -> list[dict]:
    registry = IdentityRegistry()
    rows: list[dict] = []

    # 1. Legitimate registered sender.
    payload = make_payload("CITY_CONTROL_CENTER", trial)
    actual = "ACCEPT" if registry.validate_sender(payload["sender_id"]) else "REJECT"
    rows.append(result_row(
        trial,
        "legitimate_registered_sender",
        "ACCEPT",
        actual,
        "IDENTITY_CHECK_PASSED",
        {"sender_id": payload["sender_id"]},
    ))

    # 2. Unknown sender.
    payload = make_payload(f"UNKNOWN_ATTACKER_{trial}", trial)
    authorized = registry.validate_sender(payload["sender_id"])
    actual = "ACCEPT" if authorized else "REJECT"
    rows.append(result_row(
        trial,
        "unknown_sender",
        "REJECT",
        actual,
        "IMPERSONATION_ATTEMPT" if not authorized else "IDENTITY_CHECK_PASSED",
        {"sender_id": payload["sender_id"], "authorized": authorized},
    ))

    # 3. Registered sender that has been explicitly de-authorized.
    registry.senders["CITY_CONTROL_CENTER"]["authorized"] = False
    payload = make_payload("CITY_CONTROL_CENTER", trial)
    authorized = registry.validate_sender(payload["sender_id"])
    actual = "ACCEPT" if authorized else "REJECT"
    rows.append(result_row(
        trial,
        "revoked_sender",
        "REJECT",
        actual,
        "IMPERSONATION_ATTEMPT" if not authorized else "IDENTITY_CHECK_PASSED",
        {"sender_id": payload["sender_id"], "authorized": authorized},
    ))

    # 4. Sender altered after the payload hash was bound.
    original = make_payload("CITY_CONTROL_CENTER", trial)
    bound_hash = hash_payload(original)
    tampered = deepcopy(original)
    tampered["sender_id"] = f"SPOOFED_SENDER_{trial}"
    actual_hash = hash_payload(tampered)
    actual = "REJECT" if actual_hash != bound_hash else "ACCEPT"
    rows.append(result_row(
        trial,
        "sender_field_tampering",
        "REJECT",
        actual,
        "MESSAGE_TAMPERING" if actual_hash != bound_hash else "MESSAGE_BINDING_PASSED",
        {
            "original_sender_id": original["sender_id"],
            "tampered_sender_id": tampered["sender_id"],
            "hash_changed": actual_hash != bound_hash,
            "bound_hash_prefix": bound_hash[:16],
            "actual_hash_prefix": actual_hash[:16],
        },
    ))

    return rows


def main() -> None:
    trials = 100
    rows: list[dict] = []
    for trial in range(1, trials + 1):
        rows.extend(run_trial(trial))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "trial",
        "scenario",
        "expected_decision",
        "actual_decision",
        "rule_id",
        "passed",
        "evidence",
    ]

    with CSV_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    scenario_summary = {}
    for scenario in SCENARIOS:
        scenario_rows = [row for row in rows if row["scenario"] == scenario]
        scenario_summary[scenario] = {
            "trials": len(scenario_rows),
            "passed": sum(bool(row["passed"]) for row in scenario_rows),
            "failed": sum(not bool(row["passed"]) for row in scenario_rows),
            "expected_accepts": sum(row["expected_decision"] == "ACCEPT" for row in scenario_rows),
            "actual_accepts": sum(row["actual_decision"] == "ACCEPT" for row in scenario_rows),
            "expected_rejects": sum(row["expected_decision"] == "REJECT" for row in scenario_rows),
            "actual_rejects": sum(row["actual_decision"] == "REJECT" for row in scenario_rows),
        }

    summary = {
        "trials": trials,
        "total_cases": len(rows),
        "passed_cases": sum(bool(row["passed"]) for row in rows),
        "failed_cases": sum(not bool(row["passed"]) for row in rows),
        "all_cases_passed": all(bool(row["passed"]) for row in rows),
        "scenario_summary": scenario_summary,
        "scope": "IdentityRegistry and SHA-256 payload-binding component validation; not end-to-end QDS validation.",
        "qiskit_end_to_end": "not_run_in_harness_environment",
        "csv_path": str(CSV_PATH),
    }

    SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"CSV: {CSV_PATH}")
    print(f"Summary: {SUMMARY_PATH}")


if __name__ == "__main__":
    main()
