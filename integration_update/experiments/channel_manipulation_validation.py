"""Component-level validation for channel-manipulation integrity controls."""
from __future__ import annotations
import csv, hashlib, json
from pathlib import Path

TRIALS = 100
OUT = Path(__file__).resolve().parent / "results"
OUT.mkdir(parents=True, exist_ok=True)


def digest(packet: dict) -> str:
    body = {k: packet[k] for k in ("session_id", "sequence", "basis", "measurement", "payload")}
    return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def verify(packet: dict) -> tuple[str, str, dict]:
    expected = digest(packet)
    if packet.get("channel_tag") != expected:
        return "REJECT", "CHANNEL_INTEGRITY_FAILURE", {"tag_match": False}
    if packet.get("sequence", 0) <= 0:
        return "REJECT", "CHANNEL_SEQUENCE_INVALID", {"sequence": packet.get("sequence")}
    if packet.get("basis") not in {"X", "Y", "Z"}:
        return "REJECT", "CHANNEL_PARAMETER_TAMPERING", {"basis": packet.get("basis")}
    return "ACCEPT", "CHANNEL_INTEGRITY_VALID", {"tag_match": True}


def make_packet(i: int) -> dict:
    p = {"session_id": f"S-{i}", "sequence": i + 1, "basis": "X", "measurement": i % 2, "payload": f"msg-{i}"}
    p["channel_tag"] = digest(p)
    return p


def main() -> None:
    rows = []
    scenarios = ["valid_channel", "payload_mutation", "measurement_mutation", "basis_mutation", "sequence_mutation", "channel_tag_mutation"]
    for scenario in scenarios:
        for i in range(TRIALS):
            packet = make_packet(i)
            expected = "ACCEPT" if scenario == "valid_channel" else "REJECT"
            if scenario == "payload_mutation": packet["payload"] += "-tampered"
            elif scenario == "measurement_mutation": packet["measurement"] ^= 1
            elif scenario == "basis_mutation": packet["basis"] = "Y"
            elif scenario == "sequence_mutation": packet["sequence"] = 0
            elif scenario == "channel_tag_mutation": packet["channel_tag"] = "00" * 32
            actual, rule, evidence = verify(packet)
            passed = actual == expected
            rows.append({"trial": i + 1, "scenario": scenario, "expected_decision": expected, "actual_decision": actual, "rule_id": rule, "passed": passed, "evidence": json.dumps(evidence, sort_keys=True)})
    csv_path = OUT / "channel_manipulation_validation_results.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys()); writer.writeheader(); writer.writerows(rows)
    summary = {"trials_per_scenario": TRIALS, "scenarios": scenarios, "total_cases": len(rows), "passed_cases": sum(r["passed"] for r in rows), "failed_cases": sum(not r["passed"] for r in rows), "all_cases_passed": all(r["passed"] for r in rows), "scope": "component-level integrity and channel-parameter mutation checks"}
    (OUT / "channel_manipulation_validation_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__": main()
