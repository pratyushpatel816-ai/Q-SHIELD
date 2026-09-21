from qshield.quantum.teleportation import TeleportationEngine
from qshield.security.threat_detector import QuantumThreatDetector

import csv
import statistics


OPTIMAL_THRESHOLD = 0.26
TRIALS = 30
SHOTS = 1024


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


def calculate_metrics(
    tp,
    fp,
    tn,
    fn
):
    accuracy = (
        (tp + tn) / (tp + fp + tn + fn)
    )

    precision = (
        tp / (tp + fp)
        if (tp + fp) > 0
        else 0.0
    )

    recall = (
        tp / (tp + fn)
        if (tp + fn) > 0
        else 0.0
    )

    f1_score = (
        2 * precision * recall /
        (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )

    fpr = (
        fp / (fp + tn)
        if (fp + tn) > 0
        else 0.0
    )

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
        "fpr": fpr
    }


def run_experiment():

    print()
    print("=" * 95)
    print("Q-SHIELD")
    print("PHASE 4H: CROSS-TRIAL VALIDATION")
    print("=" * 95)

    print(
        f"\nOptimized Rejection Threshold: "
        f"{OPTIMAL_THRESHOLD}"
    )

    print(
        f"Independent Trials: {TRIALS}"
    )

    scenarios = [

        # ---------------------------
        # NORMAL CONDITIONS
        # ---------------------------

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

        # ---------------------------
        # ATTACK CONDITIONS
        # ---------------------------

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

    all_trial_results = []

    print()
    print(
        f"{'Trial':<8}"
        f"{'Accuracy':<14}"
        f"{'Precision':<14}"
        f"{'Recall':<14}"
        f"{'F1 Score':<14}"
        f"{'FPR':<12}"
    )

    print("-" * 76)

    for trial in range(1, TRIALS + 1):

        engine = TeleportationEngine(
            shots=SHOTS
        )

        detector = QuantumThreatDetector(
            warn_threshold=0.05,
            reject_threshold=OPTIMAL_THRESHOLD
        )

        tp = 0
        fp = 0
        tn = 0
        fn = 0

        for scenario in scenarios:

            probes = run_probes(
                engine,
                noise_type=scenario["noise_type"],
                noise_probability=scenario[
                    "noise_probability"
                ],
                attack_type=scenario["attack_type"]
            )

            analysis = detector.analyze(
                probes
            )

            predicted_attack = (
                analysis["decision"] == "REJECT"
            )

            actual_attack = (
                scenario["label"] == "ATTACK"
            )

            if actual_attack and predicted_attack:
                tp += 1

            elif not actual_attack and predicted_attack:
                fp += 1

            elif not actual_attack and not predicted_attack:
                tn += 1

            else:
                fn += 1

        metrics = calculate_metrics(
            tp,
            fp,
            tn,
            fn
        )

        metrics["trial"] = trial

        all_trial_results.append(
            metrics
        )

        print(
            f"{trial:<8}"
            f"{metrics['accuracy']:<14.4f}"
            f"{metrics['precision']:<14.4f}"
            f"{metrics['recall']:<14.4f}"
            f"{metrics['f1_score']:<14.4f}"
            f"{metrics['fpr']:<12.4f}"
        )

    # --------------------------------
    # STATISTICAL SUMMARY
    # --------------------------------

    metric_names = [
        "accuracy",
        "precision",
        "recall",
        "f1_score",
        "fpr"
    ]

    print()
    print("=" * 95)
    print("CROSS-TRIAL STATISTICAL SUMMARY")
    print("=" * 95)

    print(
        f"{'Metric':<20}"
        f"{'Mean':<18}"
        f"{'Std Dev':<18}"
        f"{'Min':<18}"
        f"{'Max':<18}"
    )

    print("-" * 92)

    summary = {}

    for metric in metric_names:

        values = [
            result[metric]
            for result in all_trial_results
        ]

        mean_value = statistics.mean(
            values
        )

        std_value = statistics.stdev(
            values
        ) if len(values) > 1 else 0.0

        min_value = min(values)
        max_value = max(values)

        summary[metric] = {
            "mean": mean_value,
            "std": std_value,
            "min": min_value,
            "max": max_value
        }

        print(
            f"{metric:<20}"
            f"{mean_value:<18.6f}"
            f"{std_value:<18.6f}"
            f"{min_value:<18.6f}"
            f"{max_value:<18.6f}"
        )

    # --------------------------------
    # SAVE RESULTS
    # --------------------------------

    output_file = (
        "experiments/"
        "cross_validation_results.csv"
    )

    with open(
        output_file,
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "trial",
                "accuracy",
                "precision",
                "recall",
                "f1_score",
                "fpr"
            ]
        )

        writer.writeheader()

        writer.writerows(
            all_trial_results
        )

    print()
    print("=" * 95)
    print("VALIDATION CONCLUSION")
    print("=" * 95)

    print(
        f"Threshold {OPTIMAL_THRESHOLD:.2f} "
        f"validated across {TRIALS} independent trials."
    )

    print(
        f"Mean Accuracy: "
        f"{summary['accuracy']['mean']:.4f} "
        f"± {summary['accuracy']['std']:.4f}"
    )

    print(
        f"Mean Recall: "
        f"{summary['recall']['mean']:.4f} "
        f"± {summary['recall']['std']:.4f}"
    )

    print(
        f"Mean False Positive Rate: "
        f"{summary['fpr']['mean']:.4f} "
        f"± {summary['fpr']['std']:.4f}"
    )

    print()
    print(
        f"Results saved to:\n{output_file}"
    )

    print("=" * 95)
    print("PHASE 4H COMPLETED")
    print("=" * 95)


if __name__ == "__main__":
    run_experiment()