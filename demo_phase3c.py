from qshield.quantum.teleportation import (
    TeleportationEngine
)

from qshield.security.threat_detector import (
    QuantumThreatDetector
)


def separator():
    print("\n" + "=" * 75)


def run_experiment(attack_type):

    engine = TeleportationEngine(
        shots=512
    )

    detector = QuantumThreatDetector(
        warn_threshold=0.05,
        reject_threshold=0.20
    )

    # Multi-basis challenge schedule
    probes = [
        (0, "Z"),
        (1, "Z"),
        (0, "X"),
        (1, "X"),
        (0, "Y"),
        (1, "Y")
    ]

    results = []

    print(
        f"\nATTACK SCENARIO: "
        f"{attack_type.upper()}"
    )

    print("-" * 75)

    for bit, basis in probes:

        result = engine.run(
            bit=bit,
            basis=basis,
            attack_type=attack_type
        )

        results.append(result)

        print(
            f"State={result['expected_state']:<5} "
            f"| Basis={basis} "
            f"| Match={result['match_rate']:.4f} "
            f"| Mismatch={result['mismatch_rate']:.4f}"
        )

    threat_result = detector.analyze(
        results
    )

    separator()

    print("THREAT DETECTION RESULT")

    print(
        f"Decision: "
        f"{threat_result['decision']}"
    )

    print(
        f"Severity: "
        f"{threat_result['severity']}"
    )

    print(
        f"Rule ID: "
        f"{threat_result['rule_id']}"
    )

    print(
        f"Reason: "
        f"{threat_result['reason']}"
    )

    evidence = threat_result["evidence"]

    print(
        f"\nAverage Match Rate: "
        f"{evidence['average_match_rate']:.4f}"
    )

    print(
        f"Average Mismatch Rate: "
        f"{evidence['average_mismatch_rate']:.4f}"
    )

    print(
        f"Average Fidelity: "
        f"{evidence['average_fidelity']:.4f}"
    )

    print("\nBasis-Level Summary:")

    for basis, stats in (
        evidence["basis_summary"].items()
    ):

        print(
            f"Basis {basis}: "
            f"Mismatch="
            f"{stats['average_mismatch_rate']:.4f}, "
            f"Fidelity="
            f"{stats['average_fidelity']:.4f}"
        )

    return threat_result


def main():

    print("\nQ-SHIELD")
    print(
        "PHASE 3C: MULTI-BASIS "
        "QUANTUM THREAT DETECTION"
    )

    separator()

    attacks = [
        "none",
        "pauli_x",
        "pauli_y",
        "pauli_z",
        "entanglement_disruption"
    ]

    summary = {}

    for attack in attacks:

        result = run_experiment(
            attack
        )

        summary[attack] = result

        separator()

    print("\nFINAL ATTACK CLASSIFICATION")

    print("-" * 75)

    for attack, result in (
        summary.items()
    ):

        mismatch = (
            result["evidence"]
            ["average_mismatch_rate"]
        )

        print(
            f"{attack.upper():<28} "
            f"| Decision: "
            f"{result['decision']:<6} "
            f"| Severity: "
            f"{result['severity']:<6} "
            f"| Mismatch: "
            f"{mismatch:.4f}"
        )

    separator()

    print(
        "PHASE 3C DEMONSTRATION COMPLETED"
    )


if __name__ == "__main__":
    main()