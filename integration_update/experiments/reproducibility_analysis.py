"""
Q-SHIELD
PHASE 5A: REPRODUCIBILITY ANALYSIS

Evaluates whether Fixed Threshold and Blind Adaptive Threshold
performance remains consistent across multiple independent random seeds.

Experimental protocol:
- Multiple random seeds
- Heterogeneous quantum noise
- Multiple attack types
- Fixed vs Blind Adaptive comparison
- Mean, standard deviation and 95% confidence intervals
"""

import csv
import random
import numpy as np

from scipy import stats

from qshield.quantum.teleportation import TeleportationEngine


# ================================================================
# CONFIGURATION
# ================================================================

NUM_SEEDS = 20
TRIALS_PER_SCENARIO = 10
SHOTS = 1024

FIXED_THRESHOLD = 0.26
BASE_THRESHOLD = 0.26
ADAPTATION_FACTOR = 0.4


NOISE_TYPES = [
    "bit_flip",
    "phase_flip",
    "bit_phase_flip",
    "depolarizing",
    "readout"
]

NOISE_LEVELS = [
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
# METRIC FUNCTIONS
# ================================================================

def calculate_metrics(tp, fp, tn, fn):

    total = tp + fp + tn + fn

    accuracy = (tp + tn) / total if total else 0

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
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "fpr": fpr
    }


# ================================================================
# BLIND NOISE ESTIMATION
# ================================================================

def estimate_noise(mismatch_rate):

    """
    Blind proxy for channel disturbance.

    Uses observed mismatch without access
    to the true simulator noise probability.
    """

    return min(
        mismatch_rate * 1.5,
        0.50
    )


def adaptive_threshold(mismatch_rate):

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
        0.46
    )


# ================================================================
# RUN SINGLE QUANTUM TRIAL
# ================================================================

def run_quantum_trial(
    engine,
    noise_type,
    noise_probability,
    attack_type
):

    basis = random.choice([
        "X",
        "Y",
        "Z"
    ])

    bit = random.choice([
        0,
        1
    ])

    result = engine.run(
        bit=bit,
        basis=basis,
        noise_type=noise_type,
        noise_probability=noise_probability,
        attack_type=attack_type
    )

    return result["mismatch_rate"]


# ================================================================
# RUN ONE SEED
# ================================================================

def run_seed(seed):

    random.seed(seed)
    np.random.seed(seed)

    engine = TeleportationEngine(
        shots=SHOTS
    )

    fixed_tp = 0
    fixed_fp = 0
    fixed_tn = 0
    fixed_fn = 0

    adaptive_tp = 0
    adaptive_fp = 0
    adaptive_tn = 0
    adaptive_fn = 0


    # ============================================================
    # NORMAL CHANNEL CONDITIONS
    # ============================================================

    for noise_type in NOISE_TYPES:

        for noise_level in NOISE_LEVELS:

            for _ in range(
                TRIALS_PER_SCENARIO
            ):

                mismatch = run_quantum_trial(
                    engine,
                    noise_type,
                    noise_level,
                    "none"
                )

                # -------------------------
                # FIXED THRESHOLD
                # -------------------------

                fixed_reject = (
                    mismatch > FIXED_THRESHOLD
                )

                if fixed_reject:
                    fixed_fp += 1
                else:
                    fixed_tn += 1


                # -------------------------
                # BLIND ADAPTIVE
                # -------------------------

                threshold = adaptive_threshold(
                    mismatch
                )

                adaptive_reject = (
                    mismatch > threshold
                )

                if adaptive_reject:
                    adaptive_fp += 1
                else:
                    adaptive_tn += 1


    # ============================================================
    # ATTACK CONDITIONS
    # ============================================================

    for noise_type in NOISE_TYPES:

        for attack_type in ATTACK_TYPES:

            for _ in range(
                TRIALS_PER_SCENARIO
            ):

                noise_level = random.choice(
                    NOISE_LEVELS
                )

                mismatch = run_quantum_trial(
                    engine,
                    noise_type,
                    noise_level,
                    attack_type
                )

                # -------------------------
                # FIXED
                # -------------------------

                fixed_reject = (
                    mismatch > FIXED_THRESHOLD
                )

                if fixed_reject:
                    fixed_tp += 1
                else:
                    fixed_fn += 1


                # -------------------------
                # ADAPTIVE
                # -------------------------

                threshold = adaptive_threshold(
                    mismatch
                )

                adaptive_reject = (
                    mismatch > threshold
                )

                if adaptive_reject:
                    adaptive_tp += 1
                else:
                    adaptive_fn += 1


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


    return (
        fixed_metrics,
        adaptive_metrics
    )


# ================================================================
# CONFIDENCE INTERVAL
# ================================================================

def confidence_interval(values):

    values = np.array(values)

    mean = np.mean(values)

    if len(values) < 2:
        return mean, mean

    sem = stats.sem(values)

    interval = stats.t.interval(
        confidence=0.95,
        df=len(values) - 1,
        loc=mean,
        scale=sem
    )

    return interval


# ================================================================
# MAIN EXPERIMENT
# ================================================================

def main():

    print()
    print("=" * 100)
    print("Q-SHIELD")
    print("PHASE 5A: REPRODUCIBILITY ANALYSIS")
    print("=" * 100)

    print()
    print(f"Independent Random Seeds: {NUM_SEEDS}")
    print(f"Trials per Scenario: {TRIALS_PER_SCENARIO}")
    print(f"Quantum Shots: {SHOTS}")

    print()
    print("-" * 100)
    print("RUNNING INDEPENDENT REPRODUCIBILITY TRIALS")
    print("-" * 100)


    fixed_results = []
    adaptive_results = []

    for seed in range(
        1,
        NUM_SEEDS + 1
    ):

        fixed_metrics, adaptive_metrics = (
            run_seed(seed)
        )

        fixed_results.append(
            fixed_metrics
        )

        adaptive_results.append(
            adaptive_metrics
        )

        print(
            f"Seed {seed:02d} | "
            f"Fixed Acc: {fixed_metrics['accuracy']:.4f} | "
            f"Adaptive Acc: {adaptive_metrics['accuracy']:.4f} | "
            f"Fixed F1: {fixed_metrics['f1_score']:.4f} | "
            f"Adaptive F1: {adaptive_metrics['f1_score']:.4f}"
        )


    # ============================================================
    # SUMMARY
    # ============================================================

    metrics = [
        "accuracy",
        "precision",
        "recall",
        "f1_score",
        "fpr"
    ]


    print()
    print("=" * 100)
    print("REPRODUCIBILITY SUMMARY")
    print("=" * 100)

    print()
    print(
        f"{'Metric':<15}"
        f"{'Method':<18}"
        f"{'Mean':<12}"
        f"{'Std Dev':<12}"
        f"{'95% CI':<25}"
    )

    print("-" * 82)


    summary_rows = []


    for metric in metrics:

        for method, results in [

            ("Fixed", fixed_results),

            ("Blind Adaptive", adaptive_results)

        ]:

            values = [
                result[metric]
                for result in results
            ]

            mean = np.mean(values)

            std = np.std(
                values,
                ddof=1
            )

            ci_low, ci_high = (
                confidence_interval(values)
            )

            print(
                f"{metric:<15}"
                f"{method:<18}"
                f"{mean:<12.4f}"
                f"{std:<12.4f}"
                f"[{ci_low:.4f}, {ci_high:.4f}]"
            )

            summary_rows.append({

                "metric": metric,

                "method": method,

                "mean": mean,

                "std_dev": std,

                "ci_lower": ci_low,

                "ci_upper": ci_high

            })


    # ============================================================
    # PAIRED STATISTICAL TEST
    # ============================================================

    print()
    print("=" * 100)
    print("PAIRED REPRODUCIBILITY STATISTICAL TEST")
    print("=" * 100)

    print()

    print(
        f"{'Metric':<15}"
        f"{'Fixed Mean':<15}"
        f"{'Adaptive Mean':<18}"
        f"{'Difference':<15}"
        f"{'P-value':<15}"
        f"{'Result':<20}"
    )

    print("-" * 98)


    statistical_rows = []


    for metric in metrics:

        fixed_values = np.array([
            result[metric]
            for result in fixed_results
        ])

        adaptive_values = np.array([
            result[metric]
            for result in adaptive_results
        ])

        difference = (
            np.mean(adaptive_values)
            - np.mean(fixed_values)
        )

        differences = (
            adaptive_values
            - fixed_values
        )


        if np.allclose(
            differences,
            0
        ):

            p_value = 1.0

        else:

            try:

                _, p_value = stats.wilcoxon(
                    adaptive_values,
                    fixed_values
                )

            except ValueError:

                p_value = 1.0


        result_text = (
            "SIGNIFICANT"
            if p_value < 0.05
            else "NOT SIGNIFICANT"
        )


        print(
            f"{metric:<15}"
            f"{np.mean(fixed_values):<15.4f}"
            f"{np.mean(adaptive_values):<18.4f}"
            f"{difference:<15.4f}"
            f"{p_value:<15.6f}"
            f"{result_text:<20}"
        )


        statistical_rows.append({

            "metric": metric,

            "fixed_mean":
                np.mean(fixed_values),

            "adaptive_mean":
                np.mean(adaptive_values),

            "difference":
                difference,

            "p_value":
                p_value,

            "significant":
                p_value < 0.05

        })


    # ============================================================
    # SAVE TRIAL RESULTS
    # ============================================================

    with open(
        "experiments/reproducibility_trials.csv",
        "w",
        newline=""
    ) as file:

        fieldnames = [
            "seed",
            "method",
            "accuracy",
            "precision",
            "recall",
            "f1_score",
            "fpr"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for index in range(NUM_SEEDS):

            fixed_row = {

                "seed": index + 1,

                "method": "Fixed",

                **fixed_results[index]

            }

            adaptive_row = {

                "seed": index + 1,

                "method": "Blind Adaptive",

                **adaptive_results[index]

            }

            writer.writerow(
                fixed_row
            )

            writer.writerow(
                adaptive_row
            )


    # ============================================================
    # SAVE SUMMARY
    # ============================================================

    with open(
        "experiments/reproducibility_summary.csv",
        "w",
        newline=""
    ) as file:

        fieldnames = [

            "metric",

            "method",

            "mean",

            "std_dev",

            "ci_lower",

            "ci_upper"

        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(
            summary_rows
        )


    # ============================================================
    # SAVE STATISTICS
    # ============================================================

    with open(
        "experiments/reproducibility_statistics.csv",
        "w",
        newline=""
    ) as file:

        fieldnames = [

            "metric",

            "fixed_mean",

            "adaptive_mean",

            "difference",

            "p_value",

            "significant"

        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(
            statistical_rows
        )


    # ============================================================
    # FINAL CONCLUSION
    # ============================================================

    print()
    print("=" * 100)
    print("REPRODUCIBILITY CONCLUSION")
    print("=" * 100)

    fixed_accuracy = np.mean([
        x["accuracy"]
        for x in fixed_results
    ])

    adaptive_accuracy = np.mean([
        x["accuracy"]
        for x in adaptive_results
    ])

    improvement = (
        adaptive_accuracy
        - fixed_accuracy
    )

    print()
    print(
        f"Fixed Mean Accuracy: "
        f"{fixed_accuracy:.4f}"
    )

    print(
        f"Adaptive Mean Accuracy: "
        f"{adaptive_accuracy:.4f}"
    )

    print(
        f"Mean Accuracy Improvement: "
        f"{improvement:.4f}"
    )

    print()
    print(
        "Independent random-seed evaluation completed."
    )

    print()
    print("Results saved:")
    print(
        "1. experiments/reproducibility_trials.csv"
    )
    print(
        "2. experiments/reproducibility_summary.csv"
    )
    print(
        "3. experiments/reproducibility_statistics.csv"
    )

    print()
    print("=" * 100)
    print("PHASE 5A COMPLETED")
    print("=" * 100)


if __name__ == "__main__":
    main()