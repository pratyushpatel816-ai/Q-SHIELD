import csv
import math
import statistics

from scipy.stats import wilcoxon


# ============================================================
# Q-SHIELD
# PHASE 4N: STATISTICAL SIGNIFICANCE ANALYSIS
# ============================================================


def mean(values):
    return sum(values) / len(values)


def standard_deviation(values):
    if len(values) < 2:
        return 0.0

    return statistics.stdev(values)


def cohens_d(x, y):
    """
    Calculate Cohen's d effect size
    for two paired experimental samples.
    """

    differences = [
        a - b
        for a, b in zip(x, y)
    ]

    mean_difference = mean(differences)
    std_difference = standard_deviation(
        differences
    )

    if std_difference == 0:
        return 0.0

    return (
        mean_difference /
        std_difference
    )


def interpret_effect_size(d):

    absolute_d = abs(d)

    if absolute_d < 0.2:
        return "NEGLIGIBLE"

    elif absolute_d < 0.5:
        return "SMALL"

    elif absolute_d < 0.8:
        return "MEDIUM"

    else:
        return "LARGE"


def confidence_interval(values, confidence=0.95):
    """
    Approximate confidence interval
    using normal approximation.
    """

    n = len(values)

    avg = mean(values)

    if n < 2:
        return avg, avg

    std = standard_deviation(values)

    standard_error = (
        std / math.sqrt(n)
    )

    # 95% confidence multiplier
    z = 1.96

    margin = (
        z * standard_error
    )

    return (
        avg - margin,
        avg + margin
    )


def load_results():

    filename = (
        "experiments/"
        "adaptive_ablation_detailed.csv"
    )

    fixed_results = {}
    blind_results = {}

    with open(
        filename,
        "r",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            scenario = row["scenario"]
            variant = row["variant"]

            rejection_rate = float(
                row["rejection_rate"]
            )

            # Performance proxy:
            # Normal scenario -> success when NOT rejected
            # Attack scenario -> success when rejected

            label = row.get(
                "label",
                ""
            )

            if not label:

                if (
                    "Noise_" in scenario
                    or scenario == "Clean_Channel"
                ):
                    label = "NORMAL"

                else:
                    label = "ATTACK"

            if label == "NORMAL":

                performance = (
                    1.0 - rejection_rate
                )

            else:

                performance = rejection_rate

            if variant == "Fixed":

                fixed_results[
                    scenario
                ] = performance

            elif variant == "Blind_Adaptive":

                blind_results[
                    scenario
                ] = performance

    return (
        fixed_results,
        blind_results
    )


def run_experiment():

    print()
    print("=" * 100)
    print("Q-SHIELD")
    print(
        "PHASE 4N: STATISTICAL SIGNIFICANCE "
        "ANALYSIS"
    )
    print("=" * 100)

    (
        fixed_results,
        blind_results
    ) = load_results()

    common_scenarios = sorted(
        set(fixed_results.keys())
        &
        set(blind_results.keys())
    )

    fixed_scores = []
    blind_scores = []

    print()
    print(
        f"{'Scenario':<30}"
        f"{'Fixed':<15}"
        f"{'Blind Adaptive':<20}"
        f"{'Improvement':<15}"
    )

    print("-" * 80)

    for scenario in common_scenarios:

        fixed = fixed_results[
            scenario
        ]

        blind = blind_results[
            scenario
        ]

        improvement = (
            blind - fixed
        )

        fixed_scores.append(
            fixed
        )

        blind_scores.append(
            blind
        )

        print(
            f"{scenario:<30}"
            f"{fixed:<15.4f}"
            f"{blind:<20.4f}"
            f"{improvement:<15.4f}"
        )

    # --------------------------------------------------------
    # DESCRIPTIVE STATISTICS
    # --------------------------------------------------------

    fixed_mean = mean(
        fixed_scores
    )

    blind_mean = mean(
        blind_scores
    )

    improvement_mean = (
        blind_mean - fixed_mean
    )

    # --------------------------------------------------------
    # WILCOXON SIGNED-RANK TEST
    # --------------------------------------------------------

    try:

        statistic, p_value = wilcoxon(
            blind_scores,
            fixed_scores,
            alternative="greater"
        )

    except ValueError:

        statistic = 0.0
        p_value = 1.0

    # --------------------------------------------------------
    # EFFECT SIZE
    # --------------------------------------------------------

    effect_size = cohens_d(
        blind_scores,
        fixed_scores
    )

    effect_interpretation = (
        interpret_effect_size(
            effect_size
        )
    )

    # --------------------------------------------------------
    # CONFIDENCE INTERVALS
    # --------------------------------------------------------

    fixed_ci_lower, fixed_ci_upper = (
        confidence_interval(
            fixed_scores
        )
    )

    blind_ci_lower, blind_ci_upper = (
        confidence_interval(
            blind_scores
        )
    )

    improvements = [

        blind - fixed

        for blind, fixed in zip(
            blind_scores,
            fixed_scores
        )
    ]

    improvement_ci_lower, improvement_ci_upper = (
        confidence_interval(
            improvements
        )
    )

    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------

    print()
    print("=" * 100)
    print(
        "DESCRIPTIVE PERFORMANCE COMPARISON"
    )
    print("=" * 100)

    print(
        f"Number of paired scenarios: "
        f"{len(common_scenarios)}"
    )

    print()

    print(
        f"{'Metric':<25}"
        f"{'Fixed':<20}"
        f"{'Blind Adaptive':<20}"
    )

    print("-" * 65)

    print(
        f"{'Mean Performance':<25}"
        f"{fixed_mean:<20.4f}"
        f"{blind_mean:<20.4f}"
    )

    print(
        f"{'95% CI Lower':<25}"
        f"{fixed_ci_lower:<20.4f}"
        f"{blind_ci_lower:<20.4f}"
    )

    print(
        f"{'95% CI Upper':<25}"
        f"{fixed_ci_upper:<20.4f}"
        f"{blind_ci_upper:<20.4f}"
    )

    # --------------------------------------------------------
    # STATISTICAL TEST
    # --------------------------------------------------------

    print()
    print("=" * 100)
    print(
        "WILCOXON SIGNED-RANK TEST"
    )
    print("=" * 100)

    print(
        "Null Hypothesis (H0): "
        "Blind Adaptive Thresholding does not "
        "improve performance over Fixed Thresholding."
    )

    print()

    print(
        "Alternative Hypothesis (H1): "
        "Blind Adaptive Thresholding improves "
        "performance over Fixed Thresholding."
    )

    print()

    print(
        f"Wilcoxon Statistic: "
        f"{statistic:.4f}"
    )

    print(
        f"P-value: "
        f"{p_value:.6f}"
    )

    significance_level = 0.05

    if p_value < significance_level:

        conclusion = (
            "STATISTICALLY SIGNIFICANT"
        )

        hypothesis_result = (
            "REJECT NULL HYPOTHESIS"
        )

    else:

        conclusion = (
            "NOT STATISTICALLY SIGNIFICANT"
        )

        hypothesis_result = (
            "FAIL TO REJECT NULL HYPOTHESIS"
        )

    print(
        f"Significance Level: "
        f"{significance_level}"
    )

    print(
        f"Conclusion: "
        f"{conclusion}"
    )

    print(
        f"Hypothesis Decision: "
        f"{hypothesis_result}"
    )

    # --------------------------------------------------------
    # EFFECT SIZE
    # --------------------------------------------------------

    print()
    print("=" * 100)
    print(
        "EFFECT SIZE ANALYSIS"
    )
    print("=" * 100)

    print(
        f"Cohen's d: "
        f"{effect_size:.4f}"
    )

    print(
        f"Effect Magnitude: "
        f"{effect_interpretation}"
    )

    print(
        f"Mean Performance Improvement: "
        f"{improvement_mean:.4f}"
    )

    print(
        f"95% CI for Improvement: "
        f"[{improvement_ci_lower:.4f}, "
        f"{improvement_ci_upper:.4f}]"
    )

    # --------------------------------------------------------
    # FINAL RESEARCH INTERPRETATION
    # --------------------------------------------------------

    print()
    print("=" * 100)
    print(
        "RESEARCH INTERPRETATION"
    )
    print("=" * 100)

    if p_value < significance_level:

        print(
            "The Blind Adaptive Threshold mechanism "
            "demonstrates a statistically significant "
            "performance improvement over the Fixed "
            "Threshold baseline."
        )

        print()

        print(
            "This supports the hypothesis that "
            "noise-aware adaptive calibration improves "
            "the robustness of quantum anomaly detection "
            "under varying channel conditions."
        )

    else:

        print(
            "The observed improvement does not reach "
            "statistical significance at the selected "
            "significance level."
        )

    # --------------------------------------------------------
    # SAVE RESULTS
    # --------------------------------------------------------

    output_file = (
        "experiments/"
        "statistical_significance_results.csv"
    )

    with open(
        output_file,
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "metric",
            "value"
        ])

        writer.writerow([
            "fixed_mean_performance",
            fixed_mean
        ])

        writer.writerow([
            "blind_adaptive_mean_performance",
            blind_mean
        ])

        writer.writerow([
            "mean_improvement",
            improvement_mean
        ])

        writer.writerow([
            "wilcoxon_statistic",
            statistic
        ])

        writer.writerow([
            "p_value",
            p_value
        ])

        writer.writerow([
            "cohens_d",
            effect_size
        ])

        writer.writerow([
            "effect_magnitude",
            effect_interpretation
        ])

        writer.writerow([
            "improvement_ci_lower",
            improvement_ci_lower
        ])

        writer.writerow([
            "improvement_ci_upper",
            improvement_ci_upper
        ])

        writer.writerow([
            "statistical_conclusion",
            conclusion
        ])

    print()
    print(
        "Results saved to:"
    )
    print(output_file)

    print("=" * 100)
    print(
        "PHASE 4N COMPLETED"
    )
    print("=" * 100)


if __name__ == "__main__":
    run_experiment()