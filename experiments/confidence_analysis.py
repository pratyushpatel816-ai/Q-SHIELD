import csv
import math
import statistics


INPUT_FILE = (
    "experiments/"
    "cross_validation_results.csv"
)


def confidence_interval(values, confidence=0.95):
    """
    Calculate approximate 95% confidence interval
    using the normal approximation.
    """

    n = len(values)

    mean_value = statistics.mean(values)

    if n <= 1:
        return (
            mean_value,
            mean_value,
            mean_value,
            0.0
        )

    std_dev = statistics.stdev(values)

    standard_error = (
        std_dev / math.sqrt(n)
    )

    # 95% confidence level
    z_score = 1.96

    margin_error = (
        z_score * standard_error
    )

    lower_bound = (
        mean_value - margin_error
    )

    upper_bound = (
        mean_value + margin_error
    )

    return (
        mean_value,
        lower_bound,
        upper_bound,
        margin_error
    )


def run_analysis():

    print()
    print("=" * 90)
    print("Q-SHIELD")
    print("PHASE 4I: STATISTICAL CONFIDENCE ANALYSIS")
    print("=" * 90)

    data = []

    with open(
        INPUT_FILE,
        "r"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            data.append(row)

    metrics = [
        "accuracy",
        "precision",
        "recall",
        "f1_score",
        "fpr"
    ]

    print(
        f"\nTotal Independent Trials: "
        f"{len(data)}"
    )

    print()
    print(
        f"{'Metric':<18}"
        f"{'Mean':<14}"
        f"{'95% CI Lower':<18}"
        f"{'95% CI Upper':<18}"
        f"{'Margin Error':<16}"
    )

    print("-" * 84)

    results = []

    for metric in metrics:

        values = [
            float(row[metric])
            for row in data
        ]

        (
            mean_value,
            lower,
            upper,
            margin
        ) = confidence_interval(values)

        result = {
            "metric": metric,
            "mean": mean_value,
            "ci_lower": lower,
            "ci_upper": upper,
            "margin_error": margin
        }

        results.append(result)

        print(
            f"{metric:<18}"
            f"{mean_value:<14.4f}"
            f"{lower:<18.4f}"
            f"{upper:<18.4f}"
            f"{margin:<16.4f}"
        )

    # Save results

    OUTPUT_FILE = (
        "experiments/"
        "confidence_interval_results.csv"
    )

    with open(
        OUTPUT_FILE,
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "metric",
                "mean",
                "ci_lower",
                "ci_upper",
                "margin_error"
            ]
        )

        writer.writeheader()

        writer.writerows(
            results
        )

    print()
    print("=" * 90)
    print("STATISTICAL INTERPRETATION")
    print("=" * 90)

    for result in results:

        print(
            f"{result['metric'].upper()}: "
            f"{result['mean']:.4f} "
            f"(95% CI: "
            f"{result['ci_lower']:.4f} - "
            f"{result['ci_upper']:.4f})"
        )

    print()
    print(
        "Confidence interval results saved to:"
    )

    print(
        OUTPUT_FILE
    )

    print("=" * 90)
    print("PHASE 4I COMPLETED")
    print("=" * 90)


if __name__ == "__main__":
    run_analysis()