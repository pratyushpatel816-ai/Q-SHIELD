import csv
import os
import random

from qshield.quantum.teleportation import TeleportationEngine
from qshield.detection.security_constrained_threshold import (
    SecurityConstrainedThreshold
)


# ============================================================
# CONFIGURATION
# ============================================================

SHOTS = 1024
TRIALS_PER_SCENARIO = 20

FIXED_THRESHOLD = 0.26

ADAPTATION_FACTOR = 0.4

# Security caps to evaluate
MAX_THRESHOLDS = [
    0.28,
    0.30,
    0.32,
    0.34,
    0.36
]


# ============================================================
# EXPERIMENT SCENARIOS
# ============================================================

NORMAL_SCENARIOS = [
    ("bit_flip", 0.00),
    ("bit_flip", 0.05),
    ("bit_flip", 0.10),
    ("bit_flip", 0.15),
    ("bit_flip", 0.20),

    ("phase_flip", 0.00),
    ("phase_flip", 0.05),
    ("phase_flip", 0.10),
    ("phase_flip", 0.15),
    ("phase_flip", 0.20),

    ("bit_phase_flip", 0.00),
    ("bit_phase_flip", 0.05),
    ("bit_phase_flip", 0.10),
    ("bit_phase_flip", 0.15),
    ("bit_phase_flip", 0.20),

    ("depolarizing", 0.00),
    ("depolarizing", 0.05),
    ("depolarizing", 0.10),
    ("depolarizing", 0.15),
    ("depolarizing", 0.20),

    ("readout", 0.00),
    ("readout", 0.05),
    ("readout", 0.10),
    ("readout", 0.15),
    ("readout", 0.20),
]


ATTACK_SCENARIOS = [
    ("bit_flip", 0.10, "pauli_x"),
    ("bit_flip", 0.10, "pauli_y"),
    ("bit_flip", 0.10, "pauli_z"),
    ("bit_flip", 0.10, "entanglement_disruption"),

    ("phase_flip", 0.10, "pauli_x"),
    ("phase_flip", 0.10, "pauli_y"),
    ("phase_flip", 0.10, "pauli_z"),
    ("phase_flip", 0.10, "entanglement_disruption"),

    ("bit_phase_flip", 0.10, "pauli_x"),
    ("bit_phase_flip", 0.10, "pauli_y"),
    ("bit_phase_flip", 0.10, "pauli_z"),
    ("bit_phase_flip", 0.10, "entanglement_disruption"),

    ("depolarizing", 0.10, "pauli_x"),
    ("depolarizing", 0.10, "pauli_y"),
    ("depolarizing", 0.10, "pauli_z"),
    ("depolarizing", 0.10, "entanglement_disruption"),

    ("readout", 0.10, "pauli_x"),
    ("readout", 0.10, "pauli_y"),
    ("readout", 0.10, "pauli_z"),
    ("readout", 0.10, "entanglement_disruption"),
]


# ============================================================
# METRIC FUNCTIONS
# ============================================================

def calculate_metrics(tp, fp, tn, fn):

    total = tp + fp + tn + fn

    accuracy = (
        (tp + tn) / total
        if total > 0 else 0
    )

    precision = (
        tp / (tp + fp)
        if (tp + fp) > 0 else 0
    )

    recall = (
        tp / (tp + fn)
        if (tp + fn) > 0 else 0
    )

    f1_score = (
        2 * precision * recall /
        (precision + recall)
        if (precision + recall) > 0
        else 0
    )

    fpr = (
        fp / (fp + tn)
        if (fp + tn) > 0 else 0
    )

    fnr = (
        fn / (fn + tp)
        if (fn + tp) > 0 else 0
    )

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
        "fpr": fpr,
        "fnr": fnr
    }


# ============================================================
# QUANTUM EXPERIMENT
# ============================================================

def run_quantum_trial(
    noise_type="none",
    noise_probability=0.0,
    attack_type="none"
):

    engine = TeleportationEngine(
        shots=SHOTS
    )

    bit = random.randint(0, 1)

    basis = random.choice([
        "X",
        "Y",
        "Z"
    ])

    result = engine.run(
        bit=bit,
        basis=basis,
        noise_type=noise_type,
        noise_probability=noise_probability,
        attack_type=attack_type
    )

    return result["mismatch_rate"]


# ============================================================
# EVALUATE METHOD
# ============================================================

def evaluate_threshold_cap(max_threshold):

    detector = SecurityConstrainedThreshold(
        base_threshold=FIXED_THRESHOLD,
        adaptation_factor=ADAPTATION_FACTOR,
        max_threshold=max_threshold
    )

    tp = fp = tn = fn = 0

    detailed_results = []

    # --------------------------------------------------------
    # NORMAL CHANNEL TESTING
    # --------------------------------------------------------

    for noise_type, noise_probability in NORMAL_SCENARIOS:

        for trial in range(TRIALS_PER_SCENARIO):

            mismatch = run_quantum_trial(
                noise_type=noise_type,
                noise_probability=noise_probability,
                attack_type="none"
            )

            detection = detector.detect(
                mismatch
            )

            attack_detected = (
                detection["attack_detected"]
            )

            # Normal channel:
            # Detection = False Positive

            if attack_detected:
                fp += 1
            else:
                tn += 1

            detailed_results.append({
                "scenario_type": "normal",
                "noise_type": noise_type,
                "noise_probability": noise_probability,
                "attack_type": "none",
                "trial": trial + 1,
                "mismatch_rate": mismatch,
                "threshold": detection["threshold"],
                "threshold_capped": detection[
                    "threshold_capped"
                ],
                "attack_detected": attack_detected,
                "correct": not attack_detected,
                "max_threshold": max_threshold
            })

    # --------------------------------------------------------
    # ATTACK CHANNEL TESTING
    # --------------------------------------------------------

    for (
        noise_type,
        noise_probability,
        attack_type
    ) in ATTACK_SCENARIOS:

        for trial in range(TRIALS_PER_SCENARIO):

            mismatch = run_quantum_trial(
                noise_type=noise_type,
                noise_probability=noise_probability,
                attack_type=attack_type
            )

            detection = detector.detect(
                mismatch
            )

            attack_detected = (
                detection["attack_detected"]
            )

            # Attack channel:
            # Detection = True Positive

            if attack_detected:
                tp += 1
            else:
                fn += 1

            detailed_results.append({
                "scenario_type": "attack",
                "noise_type": noise_type,
                "noise_probability": noise_probability,
                "attack_type": attack_type,
                "trial": trial + 1,
                "mismatch_rate": mismatch,
                "threshold": detection["threshold"],
                "threshold_capped": detection[
                    "threshold_capped"
                ],
                "attack_detected": attack_detected,
                "correct": attack_detected,
                "max_threshold": max_threshold
            })

    metrics = calculate_metrics(
        tp,
        fp,
        tn,
        fn
    )

    metrics.update({
        "max_threshold": max_threshold,
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn
    })

    return metrics, detailed_results


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n" + "=" * 100)
    print("Q-SHIELD")
    print(
        "PHASE 5D: SECURITY-CONSTRAINED "
        "ADAPTIVE THRESHOLD ANALYSIS"
    )
    print("=" * 100)

    print(f"\nQuantum Shots: {SHOTS}")
    print(
        f"Trials per Scenario: "
        f"{TRIALS_PER_SCENARIO}"
    )
    print(
        f"Base Threshold: "
        f"{FIXED_THRESHOLD}"
    )
    print(
        f"Adaptation Factor: "
        f"{ADAPTATION_FACTOR}"
    )

    all_metrics = []
    all_details = []

    print("\n" + "-" * 100)
    print(
        "EVALUATING SECURITY THRESHOLD CAPS"
    )
    print("-" * 100)

    for max_threshold in MAX_THRESHOLDS:

        print(
            f"\nTesting Maximum Threshold: "
            f"{max_threshold:.2f}"
        )

        metrics, details = evaluate_threshold_cap(
            max_threshold
        )

        all_metrics.append(metrics)
        all_details.extend(details)

        print(
            f"Accuracy={metrics['accuracy']:.4f} | "
            f"Precision={metrics['precision']:.4f} | "
            f"Recall={metrics['recall']:.4f} | "
            f"F1={metrics['f1_score']:.4f} | "
            f"FPR={metrics['fpr']:.4f}"
        )

    # --------------------------------------------------------
    # RESULTS TABLE
    # --------------------------------------------------------

    print("\n" + "=" * 100)
    print(
        "SECURITY-CONSTRAINED ADAPTATION RESULTS"
    )
    print("=" * 100)

    print(
        f"\n{'Max Threshold':<18}"
        f"{'Accuracy':<12}"
        f"{'Precision':<12}"
        f"{'Recall':<12}"
        f"{'F1 Score':<12}"
        f"{'FPR':<12}"
        f"{'FNR':<12}"
    )

    print("-" * 90)

    for result in all_metrics:

        print(
            f"{result['max_threshold']:<18.2f}"
            f"{result['accuracy']:<12.4f}"
            f"{result['precision']:<12.4f}"
            f"{result['recall']:<12.4f}"
            f"{result['f1_score']:<12.4f}"
            f"{result['fpr']:<12.4f}"
            f"{result['fnr']:<12.4f}"
        )

    # --------------------------------------------------------
    # SELECT BEST CONFIGURATION
    # --------------------------------------------------------

    best_result = max(
        all_metrics,
        key=lambda x: x["f1_score"]
    )

    print("\n" + "=" * 100)
    print(
        "OPTIMAL SECURITY-CONSTRAINED CONFIGURATION"
    )
    print("=" * 100)

    print(
        f"\nBest Maximum Threshold: "
        f"{best_result['max_threshold']:.2f}"
    )

    print(
        f"Accuracy: "
        f"{best_result['accuracy']:.4f}"
    )

    print(
        f"Precision: "
        f"{best_result['precision']:.4f}"
    )

    print(
        f"Recall: "
        f"{best_result['recall']:.4f}"
    )

    print(
        f"F1 Score: "
        f"{best_result['f1_score']:.4f}"
    )

    print(
        f"False Positive Rate: "
        f"{best_result['fpr']:.4f}"
    )

    # --------------------------------------------------------
    # SAVE RESULTS
    # --------------------------------------------------------

    os.makedirs(
        "experiments",
        exist_ok=True
    )

    summary_file = (
        "experiments/"
        "security_constrained_summary.csv"
    )

    detail_file = (
        "experiments/"
        "security_constrained_detailed.csv"
    )

    if all_metrics:

        with open(
            summary_file,
            "w",
            newline=""
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=all_metrics[0].keys()
            )

            writer.writeheader()
            writer.writerows(
                all_metrics
            )

    if all_details:

        with open(
            detail_file,
            "w",
            newline=""
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=all_details[0].keys()
            )

            writer.writeheader()
            writer.writerows(
                all_details
            )

    print("\nResults saved:")

    print(
        "1. experiments/"
        "security_constrained_summary.csv"
    )

    print(
        "2. experiments/"
        "security_constrained_detailed.csv"
    )

    print("\n" + "=" * 100)
    print(
        "PHASE 5D COMPLETED"
    )
    print("=" * 100)


if __name__ == "__main__":
    main()