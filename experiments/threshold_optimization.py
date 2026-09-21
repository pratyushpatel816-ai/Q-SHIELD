from qshield.quantum.teleportation import TeleportationEngine
from qshield.security.threat_detector import (
    QuantumThreatDetector
)

import csv


def run_probes(
    engine,
    noise_type="none",
    noise_probability=0.0,
    attack_type="none"
):
    results = []

    for basis in ["Z", "X", "Y"]:

        result = engine.run(
            bit=0,
            basis=basis,
            noise_type=noise_type,
            noise_probability=noise_probability,
            attack_type=attack_type
        )

        results.append(result)

    return results


def run_experiment():

    print()
    print("=" * 95)
    print("Q-SHIELD")
    print("PHASE 4F: AUTOMATED THRESHOLD OPTIMIZATION")
    print("=" * 95)

    engine = TeleportationEngine(
        shots=2048
    )

    scenarios = [

        {
            "name": "Clean_Channel",
            "noise_type": "none",
            "noise_probability": 0.0,
            "attack_type": "none",
            "label": "NORMAL"
        },

        {
            "name": "Low_Noise",
            "noise_type": "bit_flip",
            "noise_probability": 0.03,
            "attack_type": "none",
            "label": "NORMAL"
        },

        {
            "name": "Moderate_Noise",
            "noise_type": "bit_flip",
            "noise_probability": 0.10,
            "attack_type": "none",
            "label": "NORMAL"
        },

        {
            "name": "High_Noise",
            "noise_type": "bit_flip",
            "noise_probability": 0.20,
            "attack_type": "none",
            "label": "NORMAL"
        },

        {
            "name": "Pauli_X",
            "noise_type": "none",
            "noise_probability": 0.0,
            "attack_type": "pauli_x",
            "label": "ATTACK"
        },

        {
            "name": "Pauli_Y",
            "noise_type": "none",
            "noise_probability": 0.0,
            "attack_type": "pauli_y",
            "label": "ATTACK"
        },

        {
            "name": "Pauli_Z",
            "noise_type": "none",
            "noise_probability": 0.0,
            "attack_type": "pauli_z",
            "label": "ATTACK"
        },

        {
            "name": "Entanglement_Disruption",
            "noise_type": "none",
            "noise_probability": 0.0,
            "attack_type": "entanglement_disruption",
            "label": "ATTACK"
        }
    ]

    # Generate probe data once so every threshold
    # is evaluated against the same dataset.
    scenario_results = []

    print("\nGenerating quantum probe dataset...")

    for scenario in scenarios:

        probes = run_probes(
            engine,
            noise_type=scenario["noise_type"],
            noise_probability=scenario[
                "noise_probability"
            ],
            attack_type=scenario["attack_type"]
        )

        scenario_results.append({
            "name": scenario["name"],
            "label": scenario["label"],
            "probes": probes
        })

    # Threshold must be greater than warn_threshold=0.05
    thresholds = [
        round(i / 100, 2)
        for i in range(6, 51)
    ]

    optimization_results = []

    print()
    print(
        f"{'Threshold':<12}"
        f"{'TPR':<12}"
        f"{'FPR':<12}"
        f"{'Accuracy':<14}"
        f"{'Score':<12}"
    )

    print("-" * 62)

    for threshold in thresholds:

        detector = QuantumThreatDetector(
            warn_threshold=0.05,
            reject_threshold=threshold
        )

        true_positive = 0
        false_positive = 0
        true_negative = 0
        false_negative = 0

        for item in scenario_results:

            analysis = detector.analyze(
                item["probes"]
            )

            predicted_attack = (
                analysis["decision"] == "REJECT"
            )

            actual_attack = (
                item["label"] == "ATTACK"
            )

            if actual_attack and predicted_attack:
                true_positive += 1

            elif not actual_attack and predicted_attack:
                false_positive += 1

            elif not actual_attack and not predicted_attack:
                true_negative += 1

            elif actual_attack and not predicted_attack:
                false_negative += 1

        tpr = (
            true_positive /
            (true_positive + false_negative)
            if (true_positive + false_negative)
            else 0
        )

        fpr = (
            false_positive /
            (false_positive + true_negative)
            if (false_positive + true_negative)
            else 0
        )

        accuracy = (
            true_positive + true_negative
        ) / len(scenario_results)

        # Optimization objective:
        # maximize attack detection while minimizing
        # false positives.
        score = tpr - fpr

        result = {
            "threshold": threshold,
            "TPR": round(tpr, 6),
            "FPR": round(fpr, 6),
            "accuracy": round(accuracy, 6),
            "score": round(score, 6),
            "TP": true_positive,
            "FP": false_positive,
            "TN": true_negative,
            "FN": false_negative
        }

        optimization_results.append(result)

        print(
            f"{threshold:<12.2f}"
            f"{tpr:<12.4f}"
            f"{fpr:<12.4f}"
            f"{accuracy:<14.4f}"
            f"{score:<12.4f}"
        )

    # Select optimal threshold.
    # Priority:
    # 1. Maximum detection score
    # 2. Maximum accuracy
    # 3. Lower threshold preference
    best_result = max(
        optimization_results,
        key=lambda x: (
            x["score"],
            x["accuracy"],
            -x["threshold"]
        )
    )

    print()
    print("=" * 95)
    print("OPTIMIZATION RESULT")
    print("=" * 95)

    print(
        f"Recommended Threshold: "
        f"{best_result['threshold']:.2f}"
    )

    print(
        f"True Positive Rate: "
        f"{best_result['TPR']:.4f}"
    )

    print(
        f"False Positive Rate: "
        f"{best_result['FPR']:.4f}"
    )

    print(
        f"Accuracy: "
        f"{best_result['accuracy']:.4f}"
    )

    print(
        f"Optimization Score: "
        f"{best_result['score']:.4f}"
    )

    print(
        f"Confusion Matrix: "
        f"TP={best_result['TP']}, "
        f"FP={best_result['FP']}, "
        f"TN={best_result['TN']}, "
        f"FN={best_result['FN']}"
    )

    # Save results.
    output_file = (
        "experiments/"
        "threshold_optimization_results.csv"
    )

    with open(
        output_file,
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "threshold",
                "TPR",
                "FPR",
                "accuracy",
                "score",
                "TP",
                "FP",
                "TN",
                "FN"
            ]
        )

        writer.writeheader()
        writer.writerows(
            optimization_results
        )

    print()
    print(
        f"Results saved to:\n{output_file}"
    )

    print("=" * 95)
    print("PHASE 4F COMPLETED")
    print("=" * 95)


if __name__ == "__main__":
    run_experiment()