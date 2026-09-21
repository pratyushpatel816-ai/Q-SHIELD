"""
Q-SHIELD
PHASE 4Q: MULTI-NOISE ROBUSTNESS EVALUATION

Evaluates Fixed vs Blind Adaptive thresholding across
multiple quantum noise channels.
"""

import csv
import numpy as np

from qshield.quantum.teleportation import TeleportationEngine


FIXED_THRESHOLD = 0.26
BASE_THRESHOLD = 0.26
ADAPTATION_FACTOR = 0.4

SHOTS = 1024
TRIALS = 20

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


def calculate_metrics(tp, fp, tn, fn):

    total = tp + fp + tn + fn

    accuracy = (tp + tn) / total if total else 0

    precision = tp / (tp + fp) if (tp + fp) else 0

    recall = tp / (tp + fn) if (tp + fn) else 0

    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) else 0
    )

    fpr = fp / (fp + tn) if (fp + tn) else 0

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "fpr": fpr
    }


def estimate_noise_from_mismatch(mismatch):

    """
    Blind noise estimation.

    Conservative estimation based only on
    observed mismatch behaviour.
    """

    estimated = mismatch * 1.5

    return min(estimated, 0.50)


def adaptive_threshold(estimated_noise):

    threshold = (
        BASE_THRESHOLD
        + ADAPTATION_FACTOR * estimated_noise
    )

    return min(threshold, 0.50)


def run_normal_channel(noise_type, noise_probability):

    engine = TeleportationEngine(shots=SHOTS)

    mismatches = []

    for trial in range(TRIALS):

        bit = trial % 2
        basis = ["X", "Y", "Z"][trial % 3]

        result = engine.run(
            bit=bit,
            basis=basis,
            noise_type=noise_type,
            noise_probability=noise_probability,
            attack_type="none"
        )

        mismatches.append(
            result["mismatch_rate"]
        )

    return mismatches


def run_attack_channel(
    noise_type,
    noise_probability,
    attack_type
):

    engine = TeleportationEngine(shots=SHOTS)

    mismatches = []

    for trial in range(TRIALS):

        bit = trial % 2
        basis = ["X", "Y", "Z"][trial % 3]

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

    return mismatches


def main():

    print("\n" + "=" * 100)
    print("Q-SHIELD")
    print("PHASE 4Q: MULTI-NOISE ROBUSTNESS EVALUATION")
    print("=" * 100)

    print(f"\nFixed Threshold: {FIXED_THRESHOLD}")
    print(f"Base Adaptive Threshold: {BASE_THRESHOLD}")
    print(f"Adaptation Factor: {ADAPTATION_FACTOR}")
    print(f"Trials per Scenario: {TRIALS}")

    results = []

    fixed_tp = fixed_fp = fixed_tn = fixed_fn = 0
    adaptive_tp = adaptive_fp = adaptive_tn = adaptive_fn = 0

    print("\n" + "-" * 100)
    print("NORMAL CHANNEL EVALUATION")
    print("-" * 100)

    for noise_type in NOISE_TYPES:

        for noise_probability in NOISE_LEVELS:

            if noise_probability == 0:

                mismatches = run_normal_channel(
                    "none",
                    0.0
                )

            else:

                mismatches = run_normal_channel(
                    noise_type,
                    noise_probability
                )

            fixed_rejected = 0
            adaptive_rejected = 0

            thresholds = []

            for mismatch in mismatches:

                if mismatch > FIXED_THRESHOLD:

                    fixed_rejected += 1
                    fixed_fp += 1

                else:

                    fixed_tn += 1

                estimated_noise = (
                    estimate_noise_from_mismatch(
                        mismatch
                    )
                )

                threshold = adaptive_threshold(
                    estimated_noise
                )

                thresholds.append(threshold)

                if mismatch > threshold:

                    adaptive_rejected += 1
                    adaptive_fp += 1

                else:

                    adaptive_tn += 1

            avg_mismatch = np.mean(mismatches)
            avg_threshold = np.mean(thresholds)

            print(
                f"{noise_type:<18} "
                f"Noise={noise_probability:.2f} | "
                f"Mismatch={avg_mismatch:.4f} | "
                f"Fixed Reject={fixed_rejected}/{TRIALS} | "
                f"Adaptive Reject={adaptive_rejected}/{TRIALS}"
            )

            results.append({
                "scenario_type": "normal",
                "noise_type": noise_type,
                "noise_probability": noise_probability,
                "attack_type": "none",
                "average_mismatch": avg_mismatch,
                "fixed_threshold": FIXED_THRESHOLD,
                "adaptive_threshold": avg_threshold,
                "fixed_rejections": fixed_rejected,
                "adaptive_rejections": adaptive_rejected
            })

    print("\n" + "-" * 100)
    print("ATTACK CHANNEL EVALUATION")
    print("-" * 100)

    attacks = [
        "pauli_x",
        "pauli_y",
        "pauli_z",
        "entanglement_disruption"
    ]

    for noise_type in NOISE_TYPES:

        for attack in attacks:

            mismatches = run_attack_channel(
                noise_type,
                0.10,
                attack
            )

            fixed_detected = 0
            adaptive_detected = 0

            thresholds = []

            for mismatch in mismatches:

                if mismatch > FIXED_THRESHOLD:

                    fixed_detected += 1
                    fixed_tp += 1

                else:

                    fixed_fn += 1

                estimated_noise = (
                    estimate_noise_from_mismatch(
                        mismatch
                    )
                )

                threshold = adaptive_threshold(
                    estimated_noise
                )

                thresholds.append(threshold)

                if mismatch > threshold:

                    adaptive_detected += 1
                    adaptive_tp += 1

                else:

                    adaptive_fn += 1

            avg_mismatch = np.mean(mismatches)
            avg_threshold = np.mean(thresholds)

            print(
                f"{noise_type:<18} "
                f"{attack:<28} | "
                f"Mismatch={avg_mismatch:.4f} | "
                f"Fixed Detect={fixed_detected}/{TRIALS} | "
                f"Adaptive Detect={adaptive_detected}/{TRIALS}"
            )

            results.append({
                "scenario_type": "attack",
                "noise_type": noise_type,
                "noise_probability": 0.10,
                "attack_type": attack,
                "average_mismatch": avg_mismatch,
                "fixed_threshold": FIXED_THRESHOLD,
                "adaptive_threshold": avg_threshold,
                "fixed_rejections": fixed_detected,
                "adaptive_rejections": adaptive_detected
            })

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

    print("\n" + "=" * 100)
    print("MULTI-NOISE ROBUSTNESS PERFORMANCE")
    print("=" * 100)

    print(
        f"\n{'Metric':<15}"
        f"{'Fixed':<20}"
        f"{'Blind Adaptive':<20}"
    )

    print("-" * 55)

    for metric in [
        "accuracy",
        "precision",
        "recall",
        "f1_score",
        "fpr"
    ]:

        print(
            f"{metric.upper():<15}"
            f"{fixed_metrics[metric]:<20.4f}"
            f"{adaptive_metrics[metric]:<20.4f}"
        )

    print("\nConfusion Matrix")

    print(
        f"\nFixed:"
        f"\nTP={fixed_tp}"
        f" FP={fixed_fp}"
        f" TN={fixed_tn}"
        f" FN={fixed_fn}"
    )

    print(
        f"\nBlind Adaptive:"
        f"\nTP={adaptive_tp}"
        f" FP={adaptive_fp}"
        f" TN={adaptive_tn}"
        f" FN={adaptive_fn}"
    )

    csv_file = (
        "experiments/multi_noise_robustness_results.csv"
    )

    with open(
        csv_file,
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys()
        )

        writer.writeheader()

        for row in results:

            writer.writerow(row)

    print("\nResults saved to:")
    print(csv_file)

    print("\n" + "=" * 100)
    print("PHASE 4Q COMPLETED")
    print("=" * 100)


if __name__ == "__main__":
    main()