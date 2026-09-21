from qshield.quantum.teleportation import TeleportationEngine
from qshield.security.threat_detector import QuantumThreatDetector

import csv


FIXED_THRESHOLD = 0.26
BASE_THRESHOLD = 0.26
ADAPTATION_FACTOR = 0.40
SHOTS = 2048
TRIALS = 20


def run_probes(
    engine,
    noise_type="none",
    noise_probability=0.0,
    attack_type="none"
):
    """
    Run quantum probes across all measurement bases.
    """

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


def calculate_adaptive_threshold(
    noise_probability
):
    """
    Noise-aware adaptive threshold.

    T_adaptive = T_base + alpha * noise

    The threshold increases when natural channel
    noise is expected to be higher.
    """

    threshold = (
        BASE_THRESHOLD
        + ADAPTATION_FACTOR
        * noise_probability
    )

    # Prevent threshold from becoming unrealistic.
    return min(threshold, 0.60)


def classify_fixed(
    probes
):
    """
    Classification using fixed threshold.
    """

    detector = QuantumThreatDetector(
        warn_threshold=0.05,
        reject_threshold=FIXED_THRESHOLD
    )

    analysis = detector.analyze(probes)

    return analysis


def classify_adaptive(
    probes,
    noise_probability
):
    """
    Classification using adaptive threshold.
    """

    adaptive_threshold = (
        calculate_adaptive_threshold(
            noise_probability
        )
    )

    detector = QuantumThreatDetector(
        warn_threshold=0.05,
        reject_threshold=adaptive_threshold
    )

    analysis = detector.analyze(probes)

    return analysis


def calculate_metrics(
    predictions,
    labels
):
    """
    Calculate classification metrics.
    """

    tp = 0
    fp = 0
    tn = 0
    fn = 0

    for predicted, actual in zip(
        predictions,
        labels
    ):

        if actual == "ATTACK":

            if predicted:
                tp += 1
            else:
                fn += 1

        else:

            if predicted:
                fp += 1
            else:
                tn += 1

    total = tp + fp + tn + fn

    accuracy = (
        (tp + tn) / total
        if total else 0
    )

    precision = (
        tp / (tp + fp)
        if (tp + fp) else 0
    )

    recall = (
        tp / (tp + fn)
        if (tp + fn) else 0
    )

    f1 = (
        2 * precision * recall /
        (precision + recall)
        if (precision + recall) else 0
    )

    fpr = (
        fp / (fp + tn)
        if (fp + tn) else 0
    )

    return {
        "TP": tp,
        "FP": fp,
        "TN": tn,
        "FN": fn,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "fpr": fpr
    }


def run_experiment():

    print()
    print("=" * 100)
    print("Q-SHIELD")
    print("PHASE 4K: ADAPTIVE THRESHOLD EVALUATION")
    print("=" * 100)

    print(
        f"\nFixed Threshold: {FIXED_THRESHOLD}"
    )

    print(
        f"Base Adaptive Threshold: "
        f"{BASE_THRESHOLD}"
    )

    print(
        f"Adaptation Factor: "
        f"{ADAPTATION_FACTOR}"
    )

    print(
        f"Trials per Scenario: "
        f"{TRIALS}"
    )

    engine = TeleportationEngine(
        shots=SHOTS
    )

    scenarios = [

        # NORMAL CONDITIONS

        {
            "name": "Clean_Channel",
            "noise_probability": 0.00,
            "noise_type": "none",
            "attack_type": "none",
            "label": "NORMAL"
        },

        {
            "name": "Noise_0.05",
            "noise_probability": 0.05,
            "noise_type": "bit_flip",
            "attack_type": "none",
            "label": "NORMAL"
        },

        {
            "name": "Noise_0.10",
            "noise_probability": 0.10,
            "noise_type": "bit_flip",
            "attack_type": "none",
            "label": "NORMAL"
        },

        {
            "name": "Noise_0.15",
            "noise_probability": 0.15,
            "noise_type": "bit_flip",
            "attack_type": "none",
            "label": "NORMAL"
        },

        {
            "name": "Noise_0.20",
            "noise_probability": 0.20,
            "noise_type": "bit_flip",
            "attack_type": "none",
            "label": "NORMAL"
        },

        {
            "name": "Noise_0.25",
            "noise_probability": 0.25,
            "noise_type": "bit_flip",
            "attack_type": "none",
            "label": "NORMAL"
        },

        {
            "name": "Noise_0.30",
            "noise_probability": 0.30,
            "noise_type": "bit_flip",
            "attack_type": "none",
            "label": "NORMAL"
        },

        # ATTACK CONDITIONS

        {
            "name": "Pauli_X",
            "noise_probability": 0.00,
            "noise_type": "none",
            "attack_type": "pauli_x",
            "label": "ATTACK"
        },

        {
            "name": "Pauli_Y",
            "noise_probability": 0.00,
            "noise_type": "none",
            "attack_type": "pauli_y",
            "label": "ATTACK"
        },

        {
            "name": "Pauli_Z",
            "noise_probability": 0.00,
            "noise_type": "none",
            "attack_type": "pauli_z",
            "label": "ATTACK"
        },

        {
            "name": "Entanglement_Disruption",
            "noise_probability": 0.00,
            "noise_type": "none",
            "attack_type": (
                "entanglement_disruption"
            ),
            "label": "ATTACK"
        },

        # ATTACK + NOISE

        {
            "name": "Pauli_X_Noise_0.10",
            "noise_probability": 0.10,
            "noise_type": "bit_flip",
            "attack_type": "pauli_x",
            "label": "ATTACK"
        },

        {
            "name": "Pauli_Y_Noise_0.10",
            "noise_probability": 0.10,
            "noise_type": "bit_flip",
            "attack_type": "pauli_y",
            "label": "ATTACK"
        },

        {
            "name": "Pauli_Z_Noise_0.10",
            "noise_probability": 0.10,
            "noise_type": "bit_flip",
            "attack_type": "pauli_z",
            "label": "ATTACK"
        },

        {
            "name": "Disruption_Noise_0.10",
            "noise_probability": 0.10,
            "noise_type": "bit_flip",
            "attack_type": (
                "entanglement_disruption"
            ),
            "label": "ATTACK"
        }
    ]

    fixed_predictions = []
    adaptive_predictions = []
    labels = []

    experiment_rows = []

    print()
    print(
        f"{'Scenario':<30}"
        f"{'Noise':<10}"
        f"{'Adaptive T':<14}"
        f"{'Fixed Reject':<15}"
        f"{'Adaptive Reject':<18}"
    )

    print("-" * 87)

    for scenario in scenarios:

        fixed_rejections = 0
        adaptive_rejections = 0

        adaptive_threshold = (
            calculate_adaptive_threshold(
                scenario["noise_probability"]
            )
        )

        for _ in range(TRIALS):

            probes = run_probes(
                engine,
                noise_type=scenario["noise_type"],
                noise_probability=(
                    scenario["noise_probability"]
                ),
                attack_type=scenario["attack_type"]
            )

            fixed_analysis = classify_fixed(
                probes
            )

            adaptive_analysis = classify_adaptive(
                probes,
                scenario["noise_probability"]
            )

            fixed_attack = (
                fixed_analysis["decision"]
                == "REJECT"
            )

            adaptive_attack = (
                adaptive_analysis["decision"]
                == "REJECT"
            )

            if fixed_attack:
                fixed_rejections += 1

            if adaptive_attack:
                adaptive_rejections += 1

            fixed_predictions.append(
                fixed_attack
            )

            adaptive_predictions.append(
                adaptive_attack
            )

            labels.append(
                scenario["label"]
            )

        fixed_rate = (
            fixed_rejections / TRIALS
        )

        adaptive_rate = (
            adaptive_rejections / TRIALS
        )

        experiment_rows.append({

            "scenario":
                scenario["name"],

            "label":
                scenario["label"],

            "noise_probability":
                scenario["noise_probability"],

            "adaptive_threshold":
                round(
                    adaptive_threshold,
                    4
                ),

            "fixed_rejection_rate":
                round(
                    fixed_rate,
                    4
                ),

            "adaptive_rejection_rate":
                round(
                    adaptive_rate,
                    4
                )
        })

        print(
            f"{scenario['name']:<30}"
            f"{scenario['noise_probability']:<10.2f}"
            f"{adaptive_threshold:<14.3f}"
            f"{fixed_rate:<15.2%}"
            f"{adaptive_rate:<18.2%}"
        )

    # Calculate metrics

    fixed_metrics = calculate_metrics(
        fixed_predictions,
        labels
    )

    adaptive_metrics = calculate_metrics(
        adaptive_predictions,
        labels
    )

    print()
    print("=" * 100)
    print("PERFORMANCE COMPARISON")
    print("=" * 100)

    print()

    print(
        f"{'Metric':<20}"
        f"{'Fixed':<20}"
        f"{'Adaptive':<20}"
    )

    print("-" * 60)

    metrics_to_display = [
        "accuracy",
        "precision",
        "recall",
        "f1_score",
        "fpr"
    ]

    for metric in metrics_to_display:

        print(
            f"{metric.upper():<20}"
            f"{fixed_metrics[metric]:<20.4f}"
            f"{adaptive_metrics[metric]:<20.4f}"
        )

    print()

    print(
        f"{'Confusion Matrix':<20}"
        f"{'Fixed':<20}"
        f"{'Adaptive':<20}"
    )

    print("-" * 60)

    for metric in ["TP", "FP", "TN", "FN"]:

        print(
            f"{metric:<20}"
            f"{fixed_metrics[metric]:<20}"
            f"{adaptive_metrics[metric]:<20}"
        )

    # Save scenario-level results

    output_file = (
        "experiments/"
        "adaptive_threshold_results.csv"
    )

    with open(
        output_file,
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "scenario",
                "label",
                "noise_probability",
                "adaptive_threshold",
                "fixed_rejection_rate",
                "adaptive_rejection_rate"
            ]
        )

        writer.writeheader()

        writer.writerows(
            experiment_rows
        )

    print()
    print(
        "Results saved to:"
    )
    print(output_file)

    print()
    print("=" * 100)
    print("PHASE 4K COMPLETED")
    print("=" * 100)


if __name__ == "__main__":
    run_experiment()