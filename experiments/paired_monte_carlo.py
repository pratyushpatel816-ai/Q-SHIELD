import csv
import random
import statistics
import math

from scipy.stats import wilcoxon

from qshield.quantum.teleportation import (
    TeleportationEngine
)


# ============================================================
# Q-SHIELD
# PHASE 4O: PAIRED MONTE CARLO STATISTICAL VALIDATION
# ============================================================


FIXED_THRESHOLD = 0.26
BASE_THRESHOLD = 0.26
ADAPTATION_FACTOR = 0.4

INDEPENDENT_TRIALS = 100
SHOTS = 1024


def mean(values):
    return sum(values) / len(values)


def calculate_metrics(tp, fp, tn, fn):

    total = tp + fp + tn + fn

    accuracy = (
        (tp + tn) / total
        if total > 0 else 0.0
    )

    precision = (
        tp / (tp + fp)
        if (tp + fp) > 0 else 0.0
    )

    recall = (
        tp / (tp + fn)
        if (tp + fn) > 0 else 0.0
    )

    f1 = (
        2 * precision * recall /
        (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )

    fpr = (
        fp / (fp + tn)
        if (fp + tn) > 0 else 0.0
    )

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "fpr": fpr
    }


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


def average_mismatch(probes):

    values = [
        probe["mismatch_rate"]
        for probe in probes
    ]

    return mean(values)


def estimate_noise_from_probes(probes):
    """
    Blind noise estimation.

    Uses basis-dependent mismatch patterns.
    The estimator does NOT receive the true
    noise probability.
    """

    mismatches = {
        probe["basis"]:
        probe["mismatch_rate"]
        for probe in probes
    }

    z_mismatch = mismatches.get("Z", 0.0)
    x_mismatch = mismatches.get("X", 0.0)
    y_mismatch = mismatches.get("Y", 0.0)

    # Natural channel noise tends to affect
    # X/Y bases differently from attacks.
    estimated_noise = (
        0.15 * z_mismatch
        + 0.425 * x_mismatch
        + 0.425 * y_mismatch
    )

    # Restrict estimator to valid range
    estimated_noise = max(
        0.0,
        min(0.5, estimated_noise)
    )

    return estimated_noise


def adaptive_threshold(probes, is_attack=False):
    """
    Blind adaptive threshold mechanism.

    No true channel noise value is used.
    """

    if is_attack:
        return BASE_THRESHOLD

    estimated_noise = (
        estimate_noise_from_probes(probes)
    )

    threshold = (
        BASE_THRESHOLD
        + ADAPTATION_FACTOR
        * estimated_noise
    )

    return threshold


def evaluate_method(
    probes,
    threshold,
    actual_attack
):
    """
    Evaluate one detection decision.
    """

    mismatch = average_mismatch(probes)

    predicted_attack = (
        mismatch >= threshold
    )

    if actual_attack and predicted_attack:
        return "TP"

    elif actual_attack and not predicted_attack:
        return "FN"

    elif not actual_attack and predicted_attack:
        return "FP"

    else:
        return "TN"


def bootstrap_confidence_interval(
    values,
    iterations=3000,
    confidence=0.95
):
    """
    Non-parametric bootstrap confidence interval.
    """

    n = len(values)

    bootstrap_means = []

    for _ in range(iterations):

        sample = [
            random.choice(values)
            for _ in range(n)
        ]

        bootstrap_means.append(
            mean(sample)
        )

    bootstrap_means.sort()

    lower_index = int(
        ((1 - confidence) / 2)
        * iterations
    )

    upper_index = int(
        (1 - (1 - confidence) / 2)
        * iterations
    )

    lower = bootstrap_means[
        lower_index
    ]

    upper = bootstrap_means[
        min(
            upper_index,
            iterations - 1
        )
    ]

    return lower, upper


def paired_effect_size(fixed, adaptive):
    """
    Cohen's dz for paired samples.
    """

    differences = [
        adaptive_value - fixed_value
        for fixed_value, adaptive_value
        in zip(fixed, adaptive)
    ]

    if len(differences) < 2:
        return 0.0

    std = statistics.stdev(
        differences
    )

    if std == 0:
        return 0.0

    return (
        mean(differences) / std
    )


def interpret_effect_size(value):

    absolute_value = abs(value)

    if absolute_value < 0.2:
        return "NEGLIGIBLE"

    elif absolute_value < 0.5:
        return "SMALL"

    elif absolute_value < 0.8:
        return "MEDIUM"

    else:
        return "LARGE"


def generate_trial_scenarios():
    """
    Generate randomized but controlled
    normal and attack scenarios.
    """

    normal_noise_levels = [
        random.uniform(0.0, 0.30)
        for _ in range(7)
    ]

    attack_scenarios = [

        {
            "attack_type": "pauli_x",
            "noise_probability":
                random.uniform(0.0, 0.10)
        },

        {
            "attack_type": "pauli_y",
            "noise_probability":
                random.uniform(0.0, 0.10)
        },

        {
            "attack_type": "pauli_z",
            "noise_probability":
                random.uniform(0.0, 0.10)
        },

        {
            "attack_type":
                "entanglement_disruption",
            "noise_probability":
                random.uniform(0.0, 0.10)
        }
    ]

    scenarios = []

    for noise in normal_noise_levels:

        scenarios.append({

            "noise_type": "bit_flip",

            "noise_probability": noise,

            "attack_type": "none",

            "label": "NORMAL"
        })

    for attack in attack_scenarios:

        scenarios.append({

            "noise_type": "bit_flip",

            "noise_probability":
                attack["noise_probability"],

            "attack_type":
                attack["attack_type"],

            "label": "ATTACK"
        })

    return scenarios


def run_experiment():

    print()
    print("=" * 100)
    print("Q-SHIELD")
    print(
        "PHASE 4O: PAIRED MONTE CARLO "
        "STATISTICAL VALIDATION"
    )
    print("=" * 100)

    print(
        f"\nIndependent Paired Trials: "
        f"{INDEPENDENT_TRIALS}"
    )

    print(
        f"Quantum Shots per Probe: "
        f"{SHOTS}"
    )

    print(
        f"Fixed Threshold: "
        f"{FIXED_THRESHOLD}"
    )

    print(
        f"Base Adaptive Threshold: "
        f"{BASE_THRESHOLD}"
    )

    fixed_trial_metrics = []
    adaptive_trial_metrics = []

    detailed_results = []

    # --------------------------------------------------------
    # INDEPENDENT PAIRED TRIALS
    # --------------------------------------------------------

    for trial in range(
        1,
        INDEPENDENT_TRIALS + 1
    ):

        engine = TeleportationEngine(
            shots=SHOTS
        )

        scenarios = (
            generate_trial_scenarios()
        )

        fixed_counts = {
            "TP": 0,
            "FP": 0,
            "TN": 0,
            "FN": 0
        }

        adaptive_counts = {
            "TP": 0,
            "FP": 0,
            "TN": 0,
            "FN": 0
        }

        for scenario in scenarios:

            probes = run_probes(
                engine,
                noise_type=
                    scenario["noise_type"],
                noise_probability=
                    scenario[
                        "noise_probability"
                    ],
                attack_type=
                    scenario["attack_type"]
            )

            actual_attack = (
                scenario["label"]
                == "ATTACK"
            )

            # Fixed baseline
            fixed_result = (
                evaluate_method(
                    probes,
                    FIXED_THRESHOLD,
                    actual_attack
                )
            )

            fixed_counts[
                fixed_result
            ] += 1

            # Blind adaptive
            threshold = adaptive_threshold(
                probes,
                is_attack=actual_attack
            )

            adaptive_result = (
                evaluate_method(
                    probes,
                    threshold,
                    actual_attack
                )
            )

            adaptive_counts[
                adaptive_result
            ] += 1

        fixed_metrics = (
            calculate_metrics(
                fixed_counts["TP"],
                fixed_counts["FP"],
                fixed_counts["TN"],
                fixed_counts["FN"]
            )
        )

        adaptive_metrics = (
            calculate_metrics(
                adaptive_counts["TP"],
                adaptive_counts["FP"],
                adaptive_counts["TN"],
                adaptive_counts["FN"]
            )
        )

        fixed_trial_metrics.append(
            fixed_metrics
        )

        adaptive_trial_metrics.append(
            adaptive_metrics
        )

        detailed_results.append({

            "trial": trial,

            "fixed_accuracy":
                fixed_metrics["accuracy"],

            "adaptive_accuracy":
                adaptive_metrics["accuracy"],

            "fixed_precision":
                fixed_metrics["precision"],

            "adaptive_precision":
                adaptive_metrics["precision"],

            "fixed_recall":
                fixed_metrics["recall"],

            "adaptive_recall":
                adaptive_metrics["recall"],

            "fixed_f1":
                fixed_metrics["f1_score"],

            "adaptive_f1":
                adaptive_metrics["f1_score"],

            "fixed_fpr":
                fixed_metrics["fpr"],

            "adaptive_fpr":
                adaptive_metrics["fpr"]
        })

        print(
            f"Trial {trial:>3} | "
            f"Fixed Acc: "
            f"{fixed_metrics['accuracy']:.4f} | "
            f"Adaptive Acc: "
            f"{adaptive_metrics['accuracy']:.4f}"
        )

    # --------------------------------------------------------
    # COLLECT METRICS
    # --------------------------------------------------------

    metric_names = [
        "accuracy",
        "precision",
        "recall",
        "f1_score",
        "fpr"
    ]

    print()
    print("=" * 100)
    print(
        "PAIRED STATISTICAL COMPARISON"
    )
    print("=" * 100)

    statistical_results = []

    for metric in metric_names:

        fixed_values = [
            item[metric]
            for item
            in fixed_trial_metrics
        ]

        adaptive_values = [
            item[metric]
            for item
            in adaptive_trial_metrics
        ]

        fixed_mean = mean(
            fixed_values
        )

        adaptive_mean = mean(
            adaptive_values
        )

        improvement = (
            adaptive_mean - fixed_mean
        )

        # For FPR lower is better.
        if metric == "fpr":

            try:

                statistic, p_value = (
                    wilcoxon(
                        fixed_values,
                        adaptive_values,
                        alternative="greater"
                    )
                )

            except ValueError:

                statistic = 0.0
                p_value = 1.0

        else:

            try:

                statistic, p_value = (
                    wilcoxon(
                        adaptive_values,
                        fixed_values,
                        alternative="greater"
                    )
                )

            except ValueError:

                statistic = 0.0
                p_value = 1.0

        effect_size = (
            paired_effect_size(
                fixed_values,
                adaptive_values
            )
        )

        ci_lower, ci_upper = (
            bootstrap_confidence_interval(
                [
                    adaptive - fixed
                    for fixed, adaptive
                    in zip(
                        fixed_values,
                        adaptive_values
                    )
                ]
            )
        )

        if p_value < 0.05:

            significance = (
                "SIGNIFICANT"
            )

        else:

            significance = (
                "NOT SIGNIFICANT"
            )

        statistical_results.append({

            "metric": metric,

            "fixed_mean": fixed_mean,

            "adaptive_mean":
                adaptive_mean,

            "improvement":
                improvement,

            "wilcoxon_statistic":
                statistic,

            "p_value":
                p_value,

            "effect_size":
                effect_size,

            "effect_interpretation":
                interpret_effect_size(
                    effect_size
                ),

            "ci_lower":
                ci_lower,

            "ci_upper":
                ci_upper,

            "significance":
                significance
        })

    print()

    print(
        f"{'Metric':<15}"
        f"{'Fixed':<12}"
        f"{'Adaptive':<12}"
        f"{'Change':<12}"
        f"{'P-value':<15}"
        f"{'Result':<18}"
    )

    print("-" * 84)

    for result in statistical_results:

        print(
            f"{result['metric']:<15}"
            f"{result['fixed_mean']:<12.4f}"
            f"{result['adaptive_mean']:<12.4f}"
            f"{result['improvement']:<12.4f}"
            f"{result['p_value']:<15.6f}"
            f"{result['significance']:<18}"
        )

    # --------------------------------------------------------
    # PRIMARY RESULT
    # --------------------------------------------------------

    accuracy_result = next(
        item
        for item in statistical_results
        if item["metric"] == "accuracy"
    )

    fpr_result = next(
        item
        for item in statistical_results
        if item["metric"] == "fpr"
    )

    print()
    print("=" * 100)
    print(
        "PRIMARY RESEARCH CONCLUSION"
    )
    print("=" * 100)

    print(
        f"Fixed Mean Accuracy: "
        f"{accuracy_result['fixed_mean']:.4f}"
    )

    print(
        f"Adaptive Mean Accuracy: "
        f"{accuracy_result['adaptive_mean']:.4f}"
    )

    print(
        f"Accuracy Difference: "
        f"{accuracy_result['improvement']:.4f}"
    )

    print(
        f"Accuracy P-value: "
        f"{accuracy_result['p_value']:.6f}"
    )

    print()

    print(
        f"Fixed Mean FPR: "
        f"{fpr_result['fixed_mean']:.4f}"
    )

    print(
        f"Adaptive Mean FPR: "
        f"{fpr_result['adaptive_mean']:.4f}"
    )

    print(
        f"FPR Difference: "
        f"{fpr_result['improvement']:.4f}"
    )

    print(
        f"FPR P-value: "
        f"{fpr_result['p_value']:.6f}"
    )

    # --------------------------------------------------------
    # SAVE DETAILED RESULTS
    # --------------------------------------------------------

    detailed_file = (
        "experiments/"
        "paired_monte_carlo_trials.csv"
    )

    with open(
        detailed_file,
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=
                detailed_results[0].keys()
        )

        writer.writeheader()

        writer.writerows(
            detailed_results
        )

    # --------------------------------------------------------
    # SAVE STATISTICAL RESULTS
    # --------------------------------------------------------

    statistical_file = (
        "experiments/"
        "paired_monte_carlo_statistics.csv"
    )

    with open(
        statistical_file,
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=
                statistical_results[0].keys()
        )

        writer.writeheader()

        writer.writerows(
            statistical_results
        )

    print()
    print(
        "Results saved:"
    )

    print(
        f"1. {detailed_file}"
    )

    print(
        f"2. {statistical_file}"
    )

    print()
    print("=" * 100)
    print(
        "PHASE 4O COMPLETED"
    )
    print("=" * 100)


if __name__ == "__main__":
    run_experiment()