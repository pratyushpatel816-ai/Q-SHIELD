"""
Q-SHIELD
PHASE 4Q: MULTI-NOISE MODEL GENERALIZATION

Evaluates Fixed vs Blind Adaptive Thresholding across
multiple quantum noise channels.

Noise Models:
1. Bit Flip
2. Phase Flip
3. Bit-Phase Flip
4. Depolarizing
5. Readout Error
"""

import csv
import random
import numpy as np

from qshield.quantum.teleportation import TeleportationEngine


# ============================================================
# CONFIGURATION
# ============================================================

FIXED_THRESHOLD = 0.26
BASE_THRESHOLD = 0.26
ADAPTATION_FACTOR = 0.40

SHOTS = 1024
TRIALS_PER_SCENARIO = 20

NOISE_TYPES = [
    "bit_flip",
    "phase_flip",
    "bit_phase_flip",
    "depolarizing",
    "readout"
]

NOISE_PROBABILITIES = [
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

OUTPUT_FILE = (
    "experiments/"
    "multi_noise_generalization_results.csv"
)


# ============================================================
# QUANTUM PROBE
# ============================================================

PROBE_STATES = [
    (0, "Z"),
    (1, "Z"),
    (0, "X"),
    (1, "X")
]


def run_probe(
    noise_type="none",
    noise_probability=0.0,
    attack_type="none"
):
    """
    Execute quantum probe states and return
    mean mismatch rate.
    """

    mismatches = []

    engine = TeleportationEngine(
        shots=SHOTS
    )

    for bit, basis in PROBE_STATES:

        result = engine.run(
            bit=bit,
            basis=basis,
            noise_type=noise_type,
            noise_probability=noise_probability,
            attack_type=attack_type
        )

        mismatches.append(
            result["mismatch_rate"]
        )

    return float(
        np.mean(mismatches)
    )


# ============================================================
# BLIND NOISE ESTIMATION
# ============================================================

def estimate_noise(mismatch_rate):
    """
    Blind estimation of channel disturbance.

    The estimator uses only observed mismatch statistics.
    It does NOT use the true noise probability.
    """

    estimated_noise = min(
        mismatch_rate * 2.0,
        0.50
    )

    return estimated_noise


# ============================================================
# ADAPTIVE THRESHOLD
# ============================================================

def calculate_adaptive_threshold(
    mismatch_rate
):
    """
    Calculate threshold using blind mismatch-based
    noise estimation.
    """

    estimated_noise = estimate_noise(
        mismatch_rate
    )

    threshold = (
        BASE_THRESHOLD
        + ADAPTATION_FACTOR
        * estimated_noise
    )

    return min(
        threshold,
        0.50
    )


# ============================================================
# METRIC CALCULATION
# ============================================================

def calculate_metrics(
    tp,
    fp,
    tn,
    fn
):

    total = tp + fp + tn + fn

    accuracy = (
        (tp + tn) / total
        if total > 0 else 0
    )

    precision = (
        tp / (tp + fp)
        if (tp + fp) > 0
        else 0
    )

    recall = (
        tp / (tp + fn)
        if (tp + fn) > 0
        else 0
    )

    f1_score = (
        2 * precision * recall
        / (precision + recall)
        if (precision + recall) > 0
        else 0
    )

    fpr = (
        fp / (fp + tn)
        if (fp + tn) > 0
        else 0
    )

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
        "fpr": fpr
    }


# ============================================================
# MAIN EXPERIMENT
# ============================================================

def run_experiment():

    print()
    print("=" * 100)
    print("Q-SHIELD")
    print(
        "PHASE 4Q: MULTI-NOISE MODEL GENERALIZATION"
    )
    print("=" * 100)

    print()
    print(f"Fixed Threshold: {FIXED_THRESHOLD}")
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
        f"{TRIALS_PER_SCENARIO}"
    )

    print()
    print(
        "Noise Models:"
    )

    for noise in NOISE_TYPES:
        print(f" - {noise}")

    print()
    print("-" * 100)
    print(
        "RUNNING MULTI-NOISE GENERALIZATION"
    )
    print("-" * 100)

    rows = []

    # Global confusion matrices

    fixed_tp = 0
    fixed_fp = 0
    fixed_tn = 0
    fixed_fn = 0

    adaptive_tp = 0
    adaptive_fp = 0
    adaptive_tn = 0
    adaptive_fn = 0

    # ========================================================
    # LOOP THROUGH NOISE MODELS
    # ========================================================

    for noise_type in NOISE_TYPES:

        print()
        print("=" * 100)
        print(
            f"NOISE MODEL: "
            f"{noise_type.upper()}"
        )
        print("=" * 100)

        # ----------------------------------------------------
        # NORMAL CHANNEL TESTS
        # ----------------------------------------------------

        for probability in NOISE_PROBABILITIES:

            fixed_rejections = 0
            adaptive_rejections = 0

            mismatch_values = []
            threshold_values = []

            for trial in range(
                TRIALS_PER_SCENARIO
            ):

                mismatch = run_probe(
                    noise_type=noise_type,
                    noise_probability=probability,
                    attack_type="none"
                )

                adaptive_threshold = (
                    calculate_adaptive_threshold(
                        mismatch
                    )
                )

                mismatch_values.append(
                    mismatch
                )

                threshold_values.append(
                    adaptive_threshold
                )

                # Fixed threshold decision

                fixed_reject = (
                    mismatch
                    >= FIXED_THRESHOLD
                )

                # Adaptive threshold decision

                adaptive_reject = (
                    mismatch
                    >= adaptive_threshold
                )

                if fixed_reject:

                    fixed_rejections += 1
                    fixed_fp += 1

                else:

                    fixed_tn += 1

                if adaptive_reject:

                    adaptive_rejections += 1
                    adaptive_fp += 1

                else:

                    adaptive_tn += 1

            mean_mismatch = float(
                np.mean(mismatch_values)
            )

            mean_threshold = float(
                np.mean(threshold_values)
            )

            fixed_rejection_rate = (
                fixed_rejections
                / TRIALS_PER_SCENARIO
            )

            adaptive_rejection_rate = (
                adaptive_rejections
                / TRIALS_PER_SCENARIO
            )

            print(
                f"Normal | "
                f"Noise={probability:.2f} | "
                f"Mismatch={mean_mismatch:.4f} | "
                f"Adaptive T={mean_threshold:.4f} | "
                f"Fixed Reject="
                f"{fixed_rejection_rate:.2%} | "
                f"Adaptive Reject="
                f"{adaptive_rejection_rate:.2%}"
            )

            rows.append({
                "noise_type": noise_type,
                "noise_probability": probability,
                "condition": "normal",
                "attack_type": "none",
                "mean_mismatch": mean_mismatch,
                "adaptive_threshold": mean_threshold,
                "fixed_rejection_rate":
                    fixed_rejection_rate,
                "adaptive_rejection_rate":
                    adaptive_rejection_rate
            })

        # ----------------------------------------------------
        # ATTACK TESTS
        # ----------------------------------------------------

        for probability in NOISE_PROBABILITIES:

            for attack_type in ATTACK_TYPES:

                fixed_detected = 0
                adaptive_detected = 0

                mismatch_values = []
                threshold_values = []

                for trial in range(
                    TRIALS_PER_SCENARIO
                ):

                    mismatch = run_probe(
                        noise_type=noise_type,
                        noise_probability=probability,
                        attack_type=attack_type
                    )

                    adaptive_threshold = (
                        calculate_adaptive_threshold(
                            mismatch
                        )
                    )

                    mismatch_values.append(
                        mismatch
                    )

                    threshold_values.append(
                        adaptive_threshold
                    )

                    fixed_reject = (
                        mismatch
                        >= FIXED_THRESHOLD
                    )

                    adaptive_reject = (
                        mismatch
                        >= adaptive_threshold
                    )

                    if fixed_reject:

                        fixed_detected += 1
                        fixed_tp += 1

                    else:

                        fixed_fn += 1

                    if adaptive_reject:

                        adaptive_detected += 1
                        adaptive_tp += 1

                    else:

                        adaptive_fn += 1

                mean_mismatch = float(
                    np.mean(mismatch_values)
                )

                mean_threshold = float(
                    np.mean(threshold_values)
                )

                fixed_detection_rate = (
                    fixed_detected
                    / TRIALS_PER_SCENARIO
                )

                adaptive_detection_rate = (
                    adaptive_detected
                    / TRIALS_PER_SCENARIO
                )

                print(
                    f"Attack | "
                    f"Noise={probability:.2f} | "
                    f"{attack_type:25} | "
                    f"Mismatch={mean_mismatch:.4f} | "
                    f"Fixed Detect="
                    f"{fixed_detection_rate:.2%} | "
                    f"Adaptive Detect="
                    f"{adaptive_detection_rate:.2%}"
                )

                rows.append({
                    "noise_type": noise_type,
                    "noise_probability":
                        probability,
                    "condition": "attack",
                    "attack_type": attack_type,
                    "mean_mismatch":
                        mean_mismatch,
                    "adaptive_threshold":
                        mean_threshold,
                    "fixed_rejection_rate":
                        fixed_detection_rate,
                    "adaptive_rejection_rate":
                        adaptive_detection_rate
                })

    # ========================================================
    # CALCULATE FINAL METRICS
    # ========================================================

    fixed_metrics = calculate_metrics(
        fixed_tp,
        fixed_fp,
        fixed_tn,
        fixed_fn
    )

    adaptive_metrics = calculate_metrics(
        adaptive_tp,
        adaptive_fp,
        adaptive_tn,
        adaptive_fn
    )

    # ========================================================
    # PRINT FINAL RESULTS
    # ========================================================

    print()
    print("=" * 100)
    print(
        "MULTI-NOISE GENERALIZATION SUMMARY"
    )
    print("=" * 100)

    print()

    print(
        f"{'Metric':<15}"
        f"{'Fixed':<20}"
        f"{'Blind Adaptive':<20}"
    )

    print("-" * 55)

    metrics = [
        "accuracy",
        "precision",
        "recall",
        "f1_score",
        "fpr"
    ]

    for metric in metrics:

        print(
            f"{metric.upper():<15}"
            f"{fixed_metrics[metric]:<20.4f}"
            f"{adaptive_metrics[metric]:<20.4f}"
        )

    print()

    print(
        "FIXED CONFUSION MATRIX"
    )

    print(
        f"TP={fixed_tp} | "
        f"FP={fixed_fp} | "
        f"TN={fixed_tn} | "
        f"FN={fixed_fn}"
    )

    print()

    print(
        "BLIND ADAPTIVE CONFUSION MATRIX"
    )

    print(
        f"TP={adaptive_tp} | "
        f"FP={adaptive_fp} | "
        f"TN={adaptive_tn} | "
        f"FN={adaptive_fn}"
    )

    # ========================================================
    # SAVE RESULTS
    # ========================================================

    fieldnames = [
        "noise_type",
        "noise_probability",
        "condition",
        "attack_type",
        "mean_mismatch",
        "adaptive_threshold",
        "fixed_rejection_rate",
        "adaptive_rejection_rate"
    ]

    with open(
        OUTPUT_FILE,
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for row in rows:
            writer.writerow(row)

    print()
    print("=" * 100)
    print(
        "RESULTS SAVED"
    )
    print("=" * 100)

    print(
        OUTPUT_FILE
    )

    print()
    print(
        "PHASE 4Q COMPLETED"
    )

    print("=" * 100)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    random.seed(42)
    np.random.seed(42)

    run_experiment()