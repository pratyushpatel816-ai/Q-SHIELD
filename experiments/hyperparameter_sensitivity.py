import os
import sys
import csv
import random
import numpy as np

from scipy.stats import wilcoxon

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from qshield.quantum.teleportation import TeleportationEngine


# ================================================================
# Q-SHIELD
# PHASE 5C: HYPERPARAMETER SENSITIVITY ANALYSIS
# ================================================================


FIXED_THRESHOLD = 0.26
BASE_THRESHOLD = 0.26

# Adaptation strengths to evaluate
ADAPTATION_FACTORS = [
    0.0,
    0.1,
    0.2,
    0.3,
    0.4,
    0.5,
    0.6,
    0.8,
    1.0
]

SHOTS = 1024
TRIALS_PER_SCENARIO = 20

NOISE_TYPES = [
    "bit_flip",
    "phase_flip",
    "bit_phase_flip",
    "depolarizing",
    "readout"
]

NOISE_LEVELS = [
    0.00,
    0.05,
    0.10,
    0.15,
    0.20
]

ATTACK_TYPES = [
    "pauli_x",
    "pauli_y",
    "pauli_z",
    "entanglement_disruption"
]


# ================================================================
# NOISE ESTIMATION
# ================================================================

def estimate_noise_from_mismatch(mismatch_rate):
    """
    Blind noise estimation based on observed mismatch.

    The estimate is deliberately bounded to avoid
    excessively increasing the rejection threshold.
    """

    estimated_noise = mismatch_rate / 2.0

    return min(
        max(estimated_noise, 0.0),
        0.5
    )


# ================================================================
# ADAPTIVE THRESHOLD
# ================================================================

def calculate_adaptive_threshold(
    estimated_noise,
    adaptation_factor
):

    threshold = (
        BASE_THRESHOLD
        + adaptation_factor * estimated_noise
    )

    # Safety bound
    return min(threshold, 0.60)


# ================================================================
# METRIC CALCULATION
# ================================================================

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
        2 * precision * recall
        / (precision + recall)
        if (precision + recall) > 0 else 0
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


# ================================================================
# NORMAL CHANNEL EXPERIMENT
# ================================================================

def evaluate_normal_channel(
    engine,
    noise_type,
    noise_probability,
    adaptation_factor
):

    false_rejections = 0

    mismatch_values = []
    threshold_values = []

    for _ in range(TRIALS_PER_SCENARIO):

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
            attack_type="none"
        )

        mismatch = result["mismatch_rate"]

        estimated_noise = (
            estimate_noise_from_mismatch(
                mismatch
            )
        )

        threshold = (
            calculate_adaptive_threshold(
                estimated_noise,
                adaptation_factor
            )
        )

        rejected = mismatch > threshold

        if rejected:
            false_rejections += 1

        mismatch_values.append(mismatch)
        threshold_values.append(threshold)

    return {
        "false_rejections": false_rejections,
        "true_negatives":
            TRIALS_PER_SCENARIO
            - false_rejections,

        "mean_mismatch":
            np.mean(mismatch_values),

        "mean_threshold":
            np.mean(threshold_values)
    }


# ================================================================
# ATTACK CHANNEL EXPERIMENT
# ================================================================

def evaluate_attack_channel(
    engine,
    noise_type,
    noise_probability,
    attack_type,
    adaptation_factor
):

    detections = 0

    mismatch_values = []
    threshold_values = []

    for _ in range(TRIALS_PER_SCENARIO):

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

        mismatch = result["mismatch_rate"]

        estimated_noise = (
            estimate_noise_from_mismatch(
                mismatch
            )
        )

        threshold = (
            calculate_adaptive_threshold(
                estimated_noise,
                adaptation_factor
            )
        )

        detected = mismatch > threshold

        if detected:
            detections += 1

        mismatch_values.append(mismatch)
        threshold_values.append(threshold)

    return {
        "detections": detections,

        "false_negatives":
            TRIALS_PER_SCENARIO
            - detections,

        "mean_mismatch":
            np.mean(mismatch_values),

        "mean_threshold":
            np.mean(threshold_values)
    }


# ================================================================
# MAIN EXPERIMENT
# ================================================================

def main():

    print()
    print("=" * 105)
    print("Q-SHIELD")
    print("PHASE 5C: HYPERPARAMETER SENSITIVITY ANALYSIS")
    print("=" * 105)

    print()
    print(f"Base Threshold: {BASE_THRESHOLD}")
    print(
        f"Adaptation Factors: "
        f"{ADAPTATION_FACTORS}"
    )
    print(
        f"Trials per Scenario: "
        f"{TRIALS_PER_SCENARIO}"
    )
    print(
        f"Quantum Shots: {SHOTS}"
    )

    engine = TeleportationEngine(
        shots=SHOTS
    )

    summary_results = []

    os.makedirs(
        "experiments",
        exist_ok=True
    )

    detailed_file = (
        "experiments/"
        "hyperparameter_sensitivity_detailed.csv"
    )

    # ============================================================
    # OPEN DETAILED CSV
    # ============================================================

    with open(
        detailed_file,
        "w",
        newline=""
    ) as csv_file:

        writer = csv.writer(csv_file)

        writer.writerow([
            "adaptation_factor",
            "scenario_type",
            "noise_type",
            "noise_probability",
            "attack_type",
            "mean_mismatch",
            "mean_threshold",
            "outcome_count"
        ])

        # ========================================================
        # TEST EACH ADAPTATION FACTOR
        # ========================================================

        for alpha in ADAPTATION_FACTORS:

            print()
            print("-" * 105)
            print(
                f"TESTING ADAPTATION FACTOR "
                f"α = {alpha}"
            )
            print("-" * 105)

            tp = 0
            fp = 0
            tn = 0
            fn = 0

            # ====================================================
            # NORMAL CHANNELS
            # ====================================================

            for noise_type in NOISE_TYPES:

                for noise_probability in NOISE_LEVELS:

                    result = (
                        evaluate_normal_channel(
                            engine,
                            noise_type,
                            noise_probability,
                            alpha
                        )
                    )

                    fp += (
                        result[
                            "false_rejections"
                        ]
                    )

                    tn += (
                        result[
                            "true_negatives"
                        ]
                    )

                    writer.writerow([
                        alpha,
                        "normal",
                        noise_type,
                        noise_probability,
                        "none",
                        round(
                            result[
                                "mean_mismatch"
                            ],
                            6
                        ),
                        round(
                            result[
                                "mean_threshold"
                            ],
                            6
                        ),
                        result[
                            "false_rejections"
                        ]
                    ])

            # ====================================================
            # ATTACK CHANNELS
            #
            # Test attacks at moderate noise
            # ====================================================

            ATTACK_NOISE_LEVEL = 0.10

            for noise_type in NOISE_TYPES:

                for attack_type in ATTACK_TYPES:

                    result = (
                        evaluate_attack_channel(
                            engine,
                            noise_type,
                            ATTACK_NOISE_LEVEL,
                            attack_type,
                            alpha
                        )
                    )

                    tp += (
                        result[
                            "detections"
                        ]
                    )

                    fn += (
                        result[
                            "false_negatives"
                        ]
                    )

                    writer.writerow([
                        alpha,
                        "attack",
                        noise_type,
                        ATTACK_NOISE_LEVEL,
                        attack_type,
                        round(
                            result[
                                "mean_mismatch"
                            ],
                            6
                        ),
                        round(
                            result[
                                "mean_threshold"
                            ],
                            6
                        ),
                        result[
                            "detections"
                        ]
                    ])

            # ====================================================
            # CALCULATE METRICS
            # ====================================================

            metrics = calculate_metrics(
                tp,
                fp,
                tn,
                fn
            )

            summary_results.append({
                "adaptation_factor": alpha,
                "tp": tp,
                "fp": fp,
                "tn": tn,
                "fn": fn,
                **metrics
            })

            print()
            print(
                f"α={alpha:.1f} | "
                f"Accuracy={metrics['accuracy']:.4f} | "
                f"Precision={metrics['precision']:.4f} | "
                f"Recall={metrics['recall']:.4f} | "
                f"F1={metrics['f1_score']:.4f} | "
                f"FPR={metrics['fpr']:.4f} | "
                f"FNR={metrics['fnr']:.4f}"
            )

    # ============================================================
    # SAVE SUMMARY
    # ============================================================

    summary_file = (
        "experiments/"
        "hyperparameter_sensitivity_summary.csv"
    )

    with open(
        summary_file,
        "w",
        newline=""
    ) as csv_file:

        fieldnames = [
            "adaptation_factor",
            "tp",
            "fp",
            "tn",
            "fn",
            "accuracy",
            "precision",
            "recall",
            "f1_score",
            "fpr",
            "fnr"
        ]

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for row in summary_results:
            writer.writerow(row)

    # ============================================================
    # RESULTS TABLE
    # ============================================================

    print()
    print("=" * 105)
    print(
        "HYPERPARAMETER SENSITIVITY RESULTS"
    )
    print("=" * 105)

    print()
    print(
        f"{'Alpha':<10}"
        f"{'Accuracy':<12}"
        f"{'Precision':<12}"
        f"{'Recall':<12}"
        f"{'F1 Score':<12}"
        f"{'FPR':<12}"
        f"{'FNR':<12}"
    )

    print("-" * 82)

    for row in summary_results:

        print(
            f"{row['adaptation_factor']:<10.1f}"
            f"{row['accuracy']:<12.4f}"
            f"{row['precision']:<12.4f}"
            f"{row['recall']:<12.4f}"
            f"{row['f1_score']:<12.4f}"
            f"{row['fpr']:<12.4f}"
            f"{row['fnr']:<12.4f}"
        )

    # ============================================================
    # IDENTIFY BEST OPERATING POINT
    # ============================================================

    best_result = max(
        summary_results,
        key=lambda x: x["f1_score"]
    )

    print()
    print("=" * 105)
    print(
        "OPTIMAL ADAPTATION FACTOR "
        "(BASED ON F1 SCORE)"
    )
    print("=" * 105)

    print()
    print(
        f"Best α: "
        f"{best_result['adaptation_factor']}"
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

    print()
    print("=" * 105)
    print(
        "SCIENTIFIC INTERPRETATION"
    )
    print("=" * 105)

    print("""
The sensitivity analysis evaluates how the adaptation
strength influences Q-SHIELD's detection performance.

Low adaptation factors retain behavior closer to fixed
thresholding and may generate more false positives under
quantum noise.

Higher adaptation factors increase tolerance to estimated
channel noise and can reduce false alarms. However,
excessively large adaptation may increase the acceptance
threshold sufficiently to reduce attack detection recall.

The resulting precision-recall and false-positive trade-off
provides an empirical basis for selecting the adaptation
factor rather than relying on an arbitrary hyperparameter.
""")

    print()
    print(
        "Results saved:"
    )

    print(
        "1. experiments/"
        "hyperparameter_sensitivity_detailed.csv"
    )

    print(
        "2. experiments/"
        "hyperparameter_sensitivity_summary.csv"
    )

    print()
    print("=" * 105)
    print(
        "PHASE 5C COMPLETED"
    )
    print("=" * 105)


if __name__ == "__main__":
    main()