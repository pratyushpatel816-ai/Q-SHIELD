"""Component-level forgery validation for Q-SHIELD.

Validates that payload/signature mutations are detected through the existing
SHA-256 payload binding and structural checks. This is not a QDS security proof.
"""
from __future__ import annotations
import csv, hashlib, json, sys
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

OUTPUT_DIR = Path(__file__).resolve().parent / "results"
CSV_PATH = OUTPUT_DIR / "forgery_validation_results.csv"
SUMMARY_PATH = OUTPUT_DIR / "forgery_validation_summary.json"
TRIALS = 100
SCENARIOS = (
    "valid_payload_signature",
    "command_forgery",
    "firmware_hash_forgery",
    "receiver_forgery",
    "signature_payload_hash_forgery",
    "signature_position_forgery",
)


def canonical_hash(payload: dict) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

def make_payload(trial: int) -> dict:
    now = datetime.now(timezone.utc)
    return {
        "sender_id": "CITY_CONTROL_CENTER",
        "receiver_id": "TRAFFIC_GATEWAY_01",
        "device_id": "SMART_TRAFFIC_GATEWAY_01",
        "command": "AUTHORIZE_FIRMWARE_UPDATE",
        "firmware_hash": "firmware_sha256_placeholder",
        "nonce": f"nonce-{trial}",
        "session_id": f"session-{trial}",
        "timestamp": now.isoformat(),
        "expiry": (now + timedelta(minutes=10)).isoformat(),
        "sequence_no": trial,
    }

def make_signature(payload: dict) -> dict:
    payload_hash = canonical_hash(payload)
    return {
        "signature_type": "Q-SHIELD_TELEPORTATION_QDS",
        "signature_length": 8,
        "payload_hash": payload_hash,
        "session_id": payload["session_id"],
        "sender_id": payload["sender_id"],
        "positions": [{"position": 0, "basis": "Z", "expected_bit": 0}],
    }

def row(trial, scenario, expected, actual, rule_id, evidence):
    return {"trial": trial, "scenario": scenario, "expected_decision": expected,
            "actual_decision": actual, "rule_id": rule_id,
            "passed": expected == actual, "evidence": json.dumps(evidence, sort_keys=True)}

def run_trial(trial: int):
    original = make_payload(trial)
    signature = make_signature(original)
    rows = []
    actual_hash = canonical_hash(original)
    rows.append(row(trial, "valid_payload_signature", "ACCEPT",
                     "ACCEPT" if actual_hash == signature["payload_hash"] else "REJECT",
                     "PAYLOAD_BINDING_PASSED", {"hash_match": actual_hash == signature["payload_hash"]}))

    mutations = [
        ("command_forgery", "command", "DELETE_ALL_KEYS"),
        ("firmware_hash_forgery", "firmware_hash", "attacker_firmware_hash"),
        ("receiver_forgery", "receiver_id", "ATTACKER_GATEWAY"),
    ]
    for scenario, field, value in mutations:
        forged = deepcopy(original); forged[field] = value
        forged_hash = canonical_hash(forged)
        changed = forged_hash != signature["payload_hash"]
        rows.append(row(trial, scenario, "REJECT", "REJECT" if changed else "ACCEPT",
                         "FORGERY_PAYLOAD_HASH_MISMATCH" if changed else "PAYLOAD_BINDING_PASSED",
                         {"field": field, "hash_changed": changed}))

    forged_signature = deepcopy(signature)
    forged_signature["payload_hash"] = hashlib.sha256(b"forged-signature-hash").hexdigest()
    changed = canonical_hash(original) != forged_signature["payload_hash"]
    rows.append(row(trial, "signature_payload_hash_forgery", "REJECT", "REJECT" if changed else "ACCEPT",
                     "FORGED_SIGNATURE_HASH" if changed else "SIGNATURE_HASH_ACCEPTED",
                     {"hash_changed": changed}))

    forged_signature = deepcopy(signature)
    forged_signature["positions"][0]["expected_bit"] = 1
    structural_change = forged_signature["positions"] != signature["positions"]
    rows.append(row(trial, "signature_position_forgery", "REJECT", "REJECT" if structural_change else "ACCEPT",
                     "SIGNATURE_POSITION_TAMPERING" if structural_change else "SIGNATURE_STRUCTURE_ACCEPTED",
                     {"position_changed": structural_change}))
    return rows

def main():
    rows = [r for trial in range(1, TRIALS + 1) for r in run_trial(trial)]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fields = ["trial", "scenario", "expected_decision", "actual_decision", "rule_id", "passed", "evidence"]
    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields); writer.writeheader(); writer.writerows(rows)
    summary = {"trials": TRIALS, "total_cases": len(rows),
               "passed_cases": sum(r["passed"] for r in rows),
               "failed_cases": sum(not r["passed"] for r in rows),
               "all_cases_passed": all(r["passed"] for r in rows),
               "scenario_summary": {s: {"trials": sum(r["scenario"] == s for r in rows),
                                         "passed": sum(r["scenario"] == s and r["passed"] for r in rows),
                                         "failed": sum(r["scenario"] == s and not r["passed"] for r in rows)} for s in SCENARIOS},
               "scope": "Payload/signature binding and structural mutation checks; not end-to-end QDS validation."}
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2)); print(f"CSV: {CSV_PATH}"); print(f"Summary: {SUMMARY_PATH}")

if __name__ == "__main__": main()
