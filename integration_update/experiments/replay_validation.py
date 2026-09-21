"""Deterministic validation harness for Q-SHIELD anti-replay controls.

This harness validates the ReplayRegistry in isolation, without requiring a
quantum simulator. It tests nonce reuse, sequence rollback, expiry handling,
and successful monotonic progression. It does not claim end-to-end QDS
security validation.
"""

from __future__ import annotations

import csv
import json
import sys
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from qshield.security.replay import ReplayRegistry  # noqa: E402


OUTPUT_DIR = Path(__file__).resolve().parent / "results"
CSV_PATH = OUTPUT_DIR / "replay_validation_results.csv"
SUMMARY_PATH = OUTPUT_DIR / "replay_validation_summary.json"


SCENARIOS = (
    "first_valid_payload",
    "reused_nonce",
    "sequence_rollback",
    "expired_payload",
    "valid_increasing_sequence",
)


def make_payload(*, nonce: str, sequence_no: int, expiry: datetime) -> dict:
    return {
        "sender_id": "CITY_CONTROL_CENTER",
        "receiver_id": "TRAFFIC_GATEWAY_01",
        "device_id": "SMART_TRAFFIC_GATEWAY_01",
        "command": "AUTHORIZE_FIRMWARE_UPDATE",
        "firmware_hash": "firmware_sha256_placeholder",
        "nonce": nonce,
        "session_id": f"session-{nonce}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "expiry": expiry.isoformat(),
        "sequence_no": sequence_no,
    }


def evaluate(
    registry: ReplayRegistry,
    scenario: str,
    payload: dict,
    expected_valid: bool,
    expected_rule_id: str,
    consume_after_validation: bool = False,
) -> dict:
    result = registry.validate_payload(payload)
    passed = (
        result["valid"] == expected_valid
        and result["rule_id"] == expected_rule_id
    )

    if consume_after_validation and result["valid"]:
        registry.consume_payload(payload)

    return {
        "scenario": scenario,
        "expected_valid": expected_valid,
        "actual_valid": result["valid"],
        "expected_rule_id": expected_rule_id,
        "actual_rule_id": result["rule_id"],
        "reason": result["reason"],
        "passed": passed,
    }


def run_trial(trial: int) -> list[dict]:
    registry = ReplayRegistry()
    now = datetime.now(timezone.utc)
    future = now + timedelta(minutes=10)
    past = now - timedelta(minutes=1)

    first = make_payload(
        nonce=f"trial-{trial}-nonce-1",
        sequence_no=1,
        expiry=future,
    )

    rows = []
    rows.append(
        evaluate(
            registry,
            "first_valid_payload",
            first,
            expected_valid=True,
            expected_rule_id="REPLAY_CHECK_PASSED",
            consume_after_validation=True,
        )
    )

    rows.append(
        evaluate(
            registry,
            "reused_nonce",
            deepcopy(first),
            expected_valid=False,
            expected_rule_id="REPLAY_ATTACK",
        )
    )

    rollback = make_payload(
        nonce=f"trial-{trial}-nonce-rollback",
        sequence_no=1,
        expiry=future,
    )
    rows.append(
        evaluate(
            registry,
            "sequence_rollback",
            rollback,
            expected_valid=False,
            expected_rule_id="REPLAY_ATTACK",
        )
    )

    expired = make_payload(
        nonce=f"trial-{trial}-nonce-expired",
        sequence_no=2,
        expiry=past,
    )
    rows.append(
        evaluate(
            registry,
            "expired_payload",
            expired,
            expected_valid=False,
            expected_rule_id="REPLAY_ATTACK",
        )
    )

    valid_next = make_payload(
        nonce=f"trial-{trial}-nonce-2",
        sequence_no=2,
        expiry=future,
    )
    rows.append(
        evaluate(
            registry,
            "valid_increasing_sequence",
            valid_next,
            expected_valid=True,
            expected_rule_id="REPLAY_CHECK_PASSED",
            consume_after_validation=True,
        )
    )

    return rows


def main() -> None:
    trials = 100
    rows = []
    for trial in range(1, trials + 1):
        for row in run_trial(trial):
            row["trial"] = trial
            rows.append(row)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "trial",
        "scenario",
        "expected_valid",
        "actual_valid",
        "expected_rule_id",
        "actual_rule_id",
        "reason",
        "passed",
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
            "passed": sum(row["passed"] for row in scenario_rows),
            "failed": sum(not row["passed"] for row in scenario_rows),
            "actual_valid_count": sum(row["actual_valid"] for row in scenario_rows),
        }

    summary = {
        "trials": trials,
        "total_cases": len(rows),
        "passed_cases": sum(row["passed"] for row in rows),
        "failed_cases": sum(not row["passed"] for row in rows),
        "all_cases_passed": all(row["passed"] for row in rows),
        "scenario_summary": scenario_summary,
        "scope": "ReplayRegistry isolation validation; not end-to-end QDS validation.",
        "csv_path": str(CSV_PATH),
    }

    SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(json.dumps(summary, indent=2))
    print(f"CSV: {CSV_PATH}")
    print(f"Summary: {SUMMARY_PATH}")


if __name__ == "__main__":
    main()
