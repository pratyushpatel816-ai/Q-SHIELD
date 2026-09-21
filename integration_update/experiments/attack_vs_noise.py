import csv
import statistics

from qshield.quantum.teleportation import (
    TeleportationEngine
)

from qshield.security.threat_detector import (
    QuantumThreatDetector
)


def run_experiment():

    print()
    print("=" * 90)
    print("Q-SHIELD")
    print("PHASE 4D: ATTACK VS NATURAL NOISE EXPERIMENT")
    print("=" * 90)

    scenarios = [
        {
            "name": "Clean_Channel",
            "noise_probability": 0.00,
            "attack_type": "none"
        },
        {
            "name": "Low_Noise",
            "noise_probability": 0.03,
            "attack_type": "none"
        },
        {
            "name": "Moderate_Noise",
            "noise_probability": 0.10,
            "attack_type": "none"
        },
        {
            "name": "High_Noise",
            "noise_probability": 0.20,
            "attack_type": "none"
        },
        {
            "name": "Pauli_X_Attack",
            "noise_probability": 0.00,
            "attack_type": "pauli_x"
        },
        {
            "name": "Pauli_Y_Attack",
            "noise_probability": 0.00,
            "attack_type": "pauli_y"
        },
        {
            "name": "Pauli_Z_Attack",
            "noise_probability": 0.00,
            "attack_type": "pauli_z"
        },
        {
            "name": "Entanglement_Disruption",
            "noise_probability": 0.00,
            "attack_type": "entanglement_disruption"
        }
    ]

    bases = ["Z", "X", "Y"]

    trials = 20

    engine = TeleportationEngine(
        shots=1024
    )

    detector = QuantumThreatDetector(
    warn_threshold=0.05,
    reject_threshold=0.20

    )

    results = []

    print()
    print(
        f"{'Scenario':<28}"
        f"{'Mismatch':<15}"
        f"{'Fidelity':<15}"
        f"{'Decision':<12}"
        f"{'Detection':<12}"
    )

    print("-" * 90)

    for scenario in scenarios:

        mismatch_values = []
        fidelity_values = []
        decisions = []

        for trial in range(trials):

            quantum_results = []

            for basis in bases:

                result = engine.run(
                    bit=0,
                    basis=basis,
                    noise_type="depolarizing",
                    noise_probability=
                        scenario["noise_probability"],
                    attack_type=
                        scenario["attack_type"]
                )

                quantum_results.append(
                    result
                )

                mismatch_values.append(
                    result["mismatch_rate"]
                )

                fidelity_values.append(
                    result["fidelity_proxy"]
                )

            detection = detector.analyze(
                quantum_results
            )

            decisions.append(
                detection["decision"]
            )

        mean_mismatch = statistics.mean(
            mismatch_values
        )

        mean_fidelity = statistics.mean(
            fidelity_values
        )

        reject_count = decisions.count(
            "REJECT"
        )

        detection_rate = (
            reject_count / trials
        )

        if reject_count > trials / 2:
            dominant_decision = "REJECT"

        elif decisions.count("WARN") > trials / 2:
            dominant_decision = "WARN"

        else:
            dominant_decision = "ACCEPT"

        row = {
            "scenario":
                scenario["name"],

            "noise_probability":
                scenario["noise_probability"],

            "attack_type":
                scenario["attack_type"],

            "mean_mismatch":
                round(mean_mismatch, 6),

            "mean_fidelity":
                round(mean_fidelity, 6),

            "dominant_decision":
                dominant_decision,

            "detection_rate":
                round(detection_rate, 6)
        }

        results.append(row)

        print(
            f"{scenario['name']:<28}"
            f"{mean_mismatch:<15.6f}"
            f"{mean_fidelity:<15.6f}"
            f"{dominant_decision:<12}"
            f"{detection_rate:<12.2%}"
        )

    with open(
        "experiments/attack_vs_noise_results.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "scenario",
                "noise_probability",
                "attack_type",
                "mean_mismatch",
                "mean_fidelity",
                "dominant_decision",
                "detection_rate"
            ]
        )

        writer.writeheader()

        writer.writerows(
            results
        )

    print()
    print("=" * 90)
    print("EXPERIMENT COMPLETED")
    print(
        "Results saved to:"
    )
    print(
        "experiments/attack_vs_noise_results.csv"
    )
    print("=" * 90)


if __name__ == "__main__":
    run_experiment()