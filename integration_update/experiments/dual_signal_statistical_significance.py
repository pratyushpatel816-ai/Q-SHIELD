import random
import numpy as np
import pandas as pd

from scipy.stats import (
    ttest_rel,
    wilcoxon,
    t
)

from qshield.quantum.teleportation import (
    TeleportationEngine
)

from qshield.detection.dual_signal_detector import (
    DualSignalDetector
)


# ============================================================
# CONFIGURATION
# ============================================================

SHOTS = 1024
TRIALS_PER_SCENARIO = 10
INDEPENDENT_SEEDS = 20

DETECTION_THRESHOLD = 0.25

NOISE_TYPES = [
    "bit_flip",
    "phase_flip",
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

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
        "fpr": fpr
    }


# ============================================================
# SINGLE DETECTOR EVALUATION
# ============================================================

def evaluate_detector(
    mismatch_weight,
    bell_weight,
    seed
):

    random.seed(seed)
    np.random.seed(seed)

    engine = TeleportationEngine(
        shots=SHOTS
    )

    detector = DualSignalDetector(
        mismatch_weight=mismatch_weight,
        bell_weight=bell_weight,
        detection_threshold=DETECTION_THRESHOLD
    )

    tp = 0
    fp = 0
    tn = 0
    fn = 0


    # ========================================================
    # NORMAL CHANNEL EVALUATION
    # ========================================================

    for noise_type in NOISE_TYPES:

        for noise_probability in NOISE_LEVELS:

            for _ in range(
                TRIALS_PER_SCENARIO
            ):

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
                    fp += 1
                else:
                    tn += 1


    # ========================================================
    # ATTACK CHANNEL EVALUATION
    # ========================================================

    for attack_type in ATTACK_TYPES:

        for _ in range(
            TRIALS_PER_SCENARIO
        ):

            bit = random.choice([0, 1])

            basis = random.choice([
                "X",
                "Y",
                "Z"
            ])

            result = engine.run(
                bit=bit,
                basis=basis,
                noise_type="depolarizing",
                noise_probability=0.10,
                attack_type=attack_type
            )

            detection = detector.detect(
                mismatch_rate=
                result["mismatch_rate"],

                bell_measurements=
                result["bell_measurements"]
            )

            if detection["attack_detected"]:
                tp += 1
            else:
                fn += 1


    return calculate_metrics(
        tp,
        fp,
        tn,
        fn
    )


# ============================================================
# CONFIDENCE INTERVAL
# ============================================================

def confidence_interval(values):

    values = np.array(values)

    mean = np.mean(values)

    std = np.std(
        values,
        ddof=1
    )

    n = len(values)

    sem = std / np.sqrt(n)

    confidence = 0.95

    alpha = 1 - confidence

    critical_value = t.ppf(
        1 - alpha / 2,
        n - 1
    )

    margin = (
        critical_value * sem
    )

    lower = mean - margin

    upper = mean + margin

    return mean, std, lower, upper


# ============================================================
# COHEN'S D
# ============================================================

def cohens_d_paired(
    fixed_values,
    adaptive_values
):

    differences = (
        np.array(adaptive_values)
        -
        np.array(fixed_values)
    )

    mean_difference = np.mean(
        differences
    )

    std_difference = np.std(
        differences,
        ddof=1
    )

    if std_difference == 0:
        return 0.0

    return (
        mean_difference
        /
        std_difference
    )


# ============================================================
# MAIN EXPERIMENT
# ============================================================

def main():

    print("=" * 100)

    print(
        "Q-SHIELD"
    )

    print(
        "PHASE 5H: DUAL-SIGNAL STATISTICAL "
        "SIGNIFICANCE ANALYSIS"
    )

    print("=" * 100)

    print()

    print(
        f"Independent Seeds: "
        f"{INDEPENDENT_SEEDS}"
    )

    print(
        f"Trials per Scenario: "
        f"{TRIALS_PER_SCENARIO}"
    )

    print(
        f"Quantum Shots: {SHOTS}"
    )

    print(
        f"Detection Threshold: "
        f"{DETECTION_THRESHOLD}"
    )

    print()

    mismatch_results = []

    dual_signal_results = []


    # ========================================================
    # INDEPENDENT SEED EXPERIMENTS
    # ========================================================

    print("-" * 100)

    print(
        "RUNNING INDEPENDENT "
        "DUAL-SIGNAL COMPARISON TRIALS"
    )

    print("-" * 100)

    for seed in range(
        1,
        INDEPENDENT_SEEDS + 1
    ):

        mismatch_metrics = (
            evaluate_detector(
                mismatch_weight=1.0,
                bell_weight=0.0,
                seed=seed
            )
        )

        dual_metrics = (
            evaluate_detector(
                mismatch_weight=0.7,
                bell_weight=0.3,
                seed=seed
            )
        )

        mismatch_metrics["seed"] = seed

        dual_metrics["seed"] = seed

        mismatch_results.append(
            mismatch_metrics
        )

        dual_signal_results.append(
            dual_metrics
        )

        print(

            f"Seed {seed:02d} | "

            f"Mismatch F1: "
            f"{mismatch_metrics['f1_score']:.4f} | "

            f"Dual F1: "
            f"{dual_metrics['f1_score']:.4f} | "

            f"Mismatch Acc: "
            f"{mismatch_metrics['accuracy']:.4f} | "

            f"Dual Acc: "
            f"{dual_metrics['accuracy']:.4f}"

        )


    # ========================================================
    # DATAFRAMES
    # ========================================================

    mismatch_df = pd.DataFrame(
        mismatch_results
    )

    dual_df = pd.DataFrame(
        dual_signal_results
    )


    # ========================================================
    # SAVE TRIAL RESULTS
    # ========================================================

    mismatch_df.to_csv(
        "experiments/mismatch_only_trials.csv",
        index=False
    )

    dual_df.to_csv(
        "experiments/dual_signal_trials.csv",
        index=False
    )


    # ========================================================
    # STATISTICAL ANALYSIS
    # ========================================================

    metrics = [

        "accuracy",
        "precision",
        "recall",
        "f1_score",
        "fpr"

    ]

    statistical_results = []

    print()

    print("=" * 100)

    print(
        "STATISTICAL SIGNIFICANCE RESULTS"
    )

    print("=" * 100)

    print()

    print(
        f"{'Metric':<15}"
        f"{'Mismatch Mean':<18}"
        f"{'Dual Mean':<18}"
        f"{'Difference':<15}"
        f"{'P-value':<15}"
        f"{'Cohen d':<15}"
        f"{'Result'}"
    )

    print("-" * 110)


    for metric in metrics:

        mismatch_values = (
            mismatch_df[metric].values
        )

        dual_values = (
            dual_df[metric].values
        )


        # ----------------------------------------------------
        # MEANS
        # ----------------------------------------------------

        mismatch_mean = np.mean(
            mismatch_values
        )

        dual_mean = np.mean(
            dual_values
        )

        difference = (
            dual_mean
            -
            mismatch_mean
        )


        # ----------------------------------------------------
        # PAIRED T TEST
        # ----------------------------------------------------

        t_statistic, p_value = (
            ttest_rel(
                dual_values,
                mismatch_values
            )
        )


        # ----------------------------------------------------
        # WILCOXON TEST
        # ----------------------------------------------------

        try:

            wilcoxon_statistic, wilcoxon_p = (
                wilcoxon(
                    dual_values,
                    mismatch_values
                )
            )

        except ValueError:

            wilcoxon_statistic = 0
            wilcoxon_p = 1.0


        # ----------------------------------------------------
        # EFFECT SIZE
        # ----------------------------------------------------

        effect_size = (
            cohens_d_paired(
                mismatch_values,
                dual_values
            )
        )


        # ----------------------------------------------------
        # CONFIDENCE INTERVALS
        # ----------------------------------------------------

        (
            mismatch_ci_mean,
            mismatch_std,
            mismatch_lower,
            mismatch_upper

        ) = confidence_interval(
            mismatch_values
        )

        (
            dual_ci_mean,
            dual_std,
            dual_lower,
            dual_upper

        ) = confidence_interval(
            dual_values
        )


        # ----------------------------------------------------
        # SIGNIFICANCE
        # ----------------------------------------------------

        if p_value < 0.001:

            result = (
                "HIGHLY SIGNIFICANT"
            )

        elif p_value < 0.05:

            result = (
                "SIGNIFICANT"
            )

        else:

            result = (
                "NOT SIGNIFICANT"
            )


        statistical_results.append({

            "metric": metric,

            "mismatch_mean":
            mismatch_mean,

            "mismatch_std":
            mismatch_std,

            "mismatch_ci_lower":
            mismatch_lower,

            "mismatch_ci_upper":
            mismatch_upper,

            "dual_mean":
            dual_mean,

            "dual_std":
            dual_std,

            "dual_ci_lower":
            dual_lower,

            "dual_ci_upper":
            dual_upper,

            "mean_difference":
            difference,

            "paired_t_p_value":
            p_value,

            "wilcoxon_p_value":
            wilcoxon_p,

            "cohens_d":
            effect_size,

            "result":
            result

        })


        print(

            f"{metric:<15}"

            f"{mismatch_mean:<18.4f}"

            f"{dual_mean:<18.4f}"

            f"{difference:<15.4f}"

            f"{p_value:<15.6f}"

            f"{effect_size:<15.4f}"

            f"{result}"

        )


    # ========================================================
    # SAVE STATISTICS
    # ========================================================

    statistics_df = pd.DataFrame(
        statistical_results
    )

    statistics_df.to_csv(

        "experiments/"
        "dual_signal_statistical_analysis.csv",

        index=False

    )


    # ========================================================
    # FINAL CONCLUSION
    # ========================================================

    print()

    print("=" * 100)

    print(
        "PHASE 5H CONCLUSION"
    )

    print("=" * 100)

    print()

    f1_row = statistics_df[
        statistics_df["metric"]
        == "f1_score"
    ].iloc[0]

    accuracy_row = statistics_df[
        statistics_df["metric"]
        == "accuracy"
    ].iloc[0]

    fpr_row = statistics_df[
        statistics_df["metric"]
        == "fpr"
    ].iloc[0]


    print(

        f"Accuracy Improvement: "
        f"{accuracy_row['mean_difference']:.4f}"

    )

    print(

        f"F1 Score Improvement: "
        f"{f1_row['mean_difference']:.4f}"

    )

    print(

        f"FPR Change: "
        f"{fpr_row['mean_difference']:.4f}"

    )

    print(

        f"F1 Score P-value: "
        f"{f1_row['paired_t_p_value']:.6f}"

    )

    print(

        f"F1 Score Effect Size "
        f"(Cohen's d): "
        f"{f1_row['cohens_d']:.4f}"

    )


    print()

    print(
        "Results saved:"
    )

    print(
        "1. experiments/mismatch_only_trials.csv"
    )

    print(
        "2. experiments/dual_signal_trials.csv"
    )

    print(
        "3. experiments/"
        "dual_signal_statistical_analysis.csv"
    )

    print()

    print("=" * 100)

    print(
        "PHASE 5H COMPLETED"
    )

    print("=" * 100)


if __name__ == "__main__":
    main()