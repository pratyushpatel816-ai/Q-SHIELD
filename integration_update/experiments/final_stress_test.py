import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from qshield.quantum.teleportation import (
    TeleportationEngine
)

from qshield.detection.dual_signal_detector import (
    DualSignalDetector
)


# ============================================================
# CONFIGURATION
# ============================================================

TRIALS_PER_SCENARIO = 20

DETECTION_THRESHOLD = 0.25

MISMATCH_WEIGHT = 0.7
BELL_WEIGHT = 0.3

SHOT_COUNTS = [
    128,
    256,
    512,
    1024,
    2048
]

NOISE_TYPES = [
    "bit_flip",
    "phase_flip",
    "bit_phase_flip",
    "depolarizing",
    "readout"
]

HIGH_NOISE_LEVELS = [
    0.20,
    0.25,
    0.30
]

ATTACK_TYPES = [
    "pauli_x",
    "pauli_y",
    "pauli_z",
    "entanglement_disruption"
]


# ============================================================
# METRIC CALCULATION
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
        "fnr": fnr,

        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn
    }


# ============================================================
# DETECTOR CREATION
# ============================================================

def create_detector():

    return DualSignalDetector(

        mismatch_weight=MISMATCH_WEIGHT,

        bell_weight=BELL_WEIGHT,

        detection_threshold=DETECTION_THRESHOLD
    )


# ============================================================
# NORMAL CHANNEL TEST
# ============================================================

def evaluate_normal_channel(
    engine,
    detector,
    noise_type,
    noise_probability,
    trials
):

    false_positives = 0
    true_negatives = 0

    for _ in range(trials):

        bit = random.choice([0, 1])

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

        detection = detector.detect(

            mismatch_rate=
            result["mismatch_rate"],

            bell_measurements=
            result["bell_measurements"]
        )

        if detection["attack_detected"]:

            false_positives += 1

        else:

            true_negatives += 1

    return false_positives, true_negatives


# ============================================================
# ATTACK UNDER NOISE TEST
# ============================================================

def evaluate_attack_channel(
    engine,
    detector,
    noise_type,
    noise_probability,
    attack_type,
    trials
):

    true_positives = 0
    false_negatives = 0

    for _ in range(trials):

        bit = random.choice([0, 1])

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

        detection = detector.detect(

            mismatch_rate=
            result["mismatch_rate"],

            bell_measurements=
            result["bell_measurements"]
        )

        if detection["attack_detected"]:

            true_positives += 1

        else:

            false_negatives += 1

    return true_positives, false_negatives


# ============================================================
# SINGLE STRESS CONFIGURATION
# ============================================================

def run_stress_configuration(
    shots,
    noise_type,
    noise_probability
):

    engine = TeleportationEngine(
        shots=shots
    )

    detector = create_detector()

    tp = 0
    fp = 0
    tn = 0
    fn = 0


    # --------------------------------------------------------
    # NORMAL CHANNEL
    # --------------------------------------------------------

    normal_fp, normal_tn = (
        evaluate_normal_channel(

            engine,

            detector,

            noise_type,

            noise_probability,

            TRIALS_PER_SCENARIO
        )
    )

    fp += normal_fp
    tn += normal_tn


    # --------------------------------------------------------
    # ATTACK CHANNEL
    # --------------------------------------------------------

    for attack_type in ATTACK_TYPES:

        attack_tp, attack_fn = (
            evaluate_attack_channel(

                engine,

                detector,

                noise_type,

                noise_probability,

                attack_type,

                TRIALS_PER_SCENARIO
            )
        )

        tp += attack_tp
        fn += attack_fn


    metrics = calculate_metrics(
        tp,
        fp,
        tn,
        fn
    )

    metrics["shots"] = shots
    metrics["noise_type"] = noise_type
    metrics["noise_probability"] = noise_probability

    return metrics


# ============================================================
# MAIN EXPERIMENT
# ============================================================

def main():

    random.seed(42)
    np.random.seed(42)

    print("=" * 100)

    print("Q-SHIELD")

    print(
        "PHASE 5I: FINAL ROBUSTNESS "
        "STRESS TEST"
    )

    print("=" * 100)

    print()

    print(
        f"Trials per Scenario: "
        f"{TRIALS_PER_SCENARIO}"
    )

    print(
        f"Detection Threshold: "
        f"{DETECTION_THRESHOLD}"
    )

    print(
        f"Mismatch Weight: "
        f"{MISMATCH_WEIGHT}"
    )

    print(
        f"Bell Weight: "
        f"{BELL_WEIGHT}"
    )

    print()

    results = []


    # ========================================================
    # RUN STRESS TESTS
    # ========================================================

    print("-" * 100)

    print(
        "RUNNING HIGH-STRESS "
        "QUANTUM CHANNEL EVALUATION"
    )

    print("-" * 100)


    total_experiments = (

        len(SHOT_COUNTS)

        * len(NOISE_TYPES)

        * len(HIGH_NOISE_LEVELS)
    )

    experiment_number = 0


    for shots in SHOT_COUNTS:

        for noise_type in NOISE_TYPES:

            for noise_probability in HIGH_NOISE_LEVELS:

                experiment_number += 1

                print()

                print(
                    f"[{experiment_number}/"
                    f"{total_experiments}]"
                )

                print(

                    f"Shots={shots} | "

                    f"Noise={noise_type} | "

                    f"Probability="
                    f"{noise_probability:.2f}"
                )


                metrics = (
                    run_stress_configuration(

                        shots,

                        noise_type,

                        noise_probability
                    )
                )

                results.append(metrics)


                print(

                    f"Accuracy="
                    f"{metrics['accuracy']:.4f} | "

                    f"Precision="
                    f"{metrics['precision']:.4f} | "

                    f"Recall="
                    f"{metrics['recall']:.4f} | "

                    f"F1="
                    f"{metrics['f1_score']:.4f} | "

                    f"FPR="
                    f"{metrics['fpr']:.4f}"
                )


    # ========================================================
    # CREATE DATAFRAME
    # ========================================================

    df = pd.DataFrame(results)


    # ========================================================
    # SAVE RESULTS
    # ========================================================

    output_file = (
        "experiments/"
        "final_stress_test_results.csv"
    )

    df.to_csv(
        output_file,
        index=False
    )


    # ========================================================
    # SUMMARY BY SHOT COUNT
    # ========================================================

    shot_summary = (

        df.groupby("shots")[

            [
                "accuracy",
                "precision",
                "recall",
                "f1_score",
                "fpr",
                "fnr"
            ]

        ]

        .mean()

        .reset_index()
    )


    shot_summary_file = (

        "experiments/"
        "stress_test_shot_summary.csv"
    )

    shot_summary.to_csv(

        shot_summary_file,

        index=False
    )


    # ========================================================
    # SUMMARY BY NOISE TYPE
    # ========================================================

    noise_summary = (

        df.groupby("noise_type")[

            [
                "accuracy",
                "precision",
                "recall",
                "f1_score",
                "fpr",
                "fnr"
            ]

        ]

        .mean()

        .reset_index()
    )


    noise_summary_file = (

        "experiments/"
        "stress_test_noise_summary.csv"
    )

    noise_summary.to_csv(

        noise_summary_file,

        index=False
    )


    # ========================================================
    # OVERALL RESULTS
    # ========================================================

    print()

    print("=" * 100)

    print(
        "FINAL STRESS TEST SUMMARY"
    )

    print("=" * 100)

    print()

    print(

        f"{'Metric':<20}"
        f"{'Mean':<15}"
        f"{'Minimum':<15}"
        f"{'Maximum':<15}"

    )

    print("-" * 65)


    metrics_to_display = [

        "accuracy",
        "precision",
        "recall",
        "f1_score",
        "fpr",
        "fnr"
    ]


    for metric in metrics_to_display:

        mean_value = df[metric].mean()

        min_value = df[metric].min()

        max_value = df[metric].max()


        print(

            f"{metric:<20}"

            f"{mean_value:<15.4f}"

            f"{min_value:<15.4f}"

            f"{max_value:<15.4f}"

        )


    # ========================================================
    # VISUALIZATION 1
    # SHOT COUNT VS PERFORMANCE
    # ========================================================

    plt.figure(
        figsize=(10, 6)
    )

    plt.plot(

        shot_summary["shots"],

        shot_summary["accuracy"],

        marker="o",

        label="Accuracy"
    )

    plt.plot(

        shot_summary["shots"],

        shot_summary["f1_score"],

        marker="s",

        label="F1 Score"
    )

    plt.plot(

        shot_summary["shots"],

        shot_summary["recall"],

        marker="^",

        label="Recall"
    )

    plt.xlabel(
        "Quantum Shot Count"
    )

    plt.ylabel(
        "Performance Score"
    )

    plt.title(
        "Q-SHIELD Stress Test: "
        "Performance vs Shot Count"
    )

    plt.grid(True)

    plt.legend()

    plt.tight_layout()

    plt.savefig(

        "experiments/"
        "stress_test_shot_performance.png",

        dpi=300
    )

    plt.close()


    # ========================================================
    # VISUALIZATION 2
    # NOISE TYPE PERFORMANCE
    # ========================================================

    plt.figure(
        figsize=(10, 6)
    )

    x = np.arange(
        len(noise_summary)
    )

    width = 0.25

    plt.bar(

        x - width,

        noise_summary["accuracy"],

        width,

        label="Accuracy"
    )

    plt.bar(

        x,

        noise_summary["f1_score"],

        width,

        label="F1 Score"
    )

    plt.bar(

        x + width,

        noise_summary["fpr"],

        width,

        label="FPR"
    )

    plt.xticks(

        x,

        noise_summary["noise_type"],

        rotation=20
    )

    plt.ylabel(
        "Metric Value"
    )

    plt.title(
        "Q-SHIELD Stress Test: "
        "Performance Across Noise Channels"
    )

    plt.legend()

    plt.tight_layout()

    plt.savefig(

        "experiments/"
        "stress_test_noise_comparison.png",

        dpi=300
    )

    plt.close()


    # ========================================================
    # VISUALIZATION 3
    # NOISE LEVEL VS PERFORMANCE
    # ========================================================

    noise_level_summary = (

        df.groupby(
            "noise_probability"
        )[

            [
                "accuracy",
                "f1_score",
                "fpr"
            ]

        ]

        .mean()

        .reset_index()
    )


    plt.figure(
        figsize=(10, 6)
    )

    plt.plot(

        noise_level_summary[
            "noise_probability"
        ],

        noise_level_summary[
            "accuracy"
        ],

        marker="o",

        label="Accuracy"
    )

    plt.plot(

        noise_level_summary[
            "noise_probability"
        ],

        noise_level_summary[
            "f1_score"
        ],

        marker="s",

        label="F1 Score"
    )

    plt.plot(

        noise_level_summary[
            "noise_probability"
        ],

        noise_level_summary[
            "fpr"
        ],

        marker="^",

        label="FPR"
    )

    plt.xlabel(
        "Noise Probability"
    )

    plt.ylabel(
        "Metric Value"
    )

    plt.title(
        "Q-SHIELD Stress Test: "
        "Robustness Under Increasing Noise"
    )

    plt.grid(True)

    plt.legend()

    plt.tight_layout()

    plt.savefig(

        "experiments/"
        "stress_test_noise_levels.png",

        dpi=300
    )

    plt.close()


    # ========================================================
    # FINAL OUTPUT
    # ========================================================

    print()

    print("=" * 100)

    print(
        "GENERATED FILES"
    )

    print("=" * 100)

    print()

    print(
        "1. experiments/"
        "final_stress_test_results.csv"
    )

    print(
        "2. experiments/"
        "stress_test_shot_summary.csv"
    )

    print(
        "3. experiments/"
        "stress_test_noise_summary.csv"
    )

    print(
        "4. experiments/"
        "stress_test_shot_performance.png"
    )

    print(
        "5. experiments/"
        "stress_test_noise_comparison.png"
    )

    print(
        "6. experiments/"
        "stress_test_noise_levels.png"
    )

    print()

    print("=" * 100)

    print(
        "PHASE 5I COMPLETED"
    )

    print("=" * 100)


if __name__ == "__main__":
    main()