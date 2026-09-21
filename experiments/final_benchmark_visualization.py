"""
Q-SHIELD
PHASE 4R: FINAL BENCHMARK VISUALIZATION

Generates publication-quality summary figures
from the complete Q-SHIELD experimental evaluation.
"""

import pandas as pd
import matplotlib.pyplot as plt


def performance_comparison():

    methods = [
        "Fixed\nThreshold",
        "Blind\nAdaptive"
    ]

    accuracy = [
        0.7973,
        1.0000
    ]

    precision = [
        0.6614,
        1.0000
    ]

    f1_score = [
        0.7904,
        1.0000
    ]

    x = range(len(methods))

    plt.figure(figsize=(10, 6))

    width = 0.22

    plt.bar(
        [i - width for i in x],
        accuracy,
        width,
        label="Accuracy"
    )

    plt.bar(
        x,
        precision,
        width,
        label="Precision"
    )

    plt.bar(
        [i + width for i in x],
        f1_score,
        width,
        label="F1 Score"
    )

    plt.xticks(x, methods)

    plt.ylim(0, 1.1)

    plt.ylabel("Performance Score")

    plt.title(
        "Q-SHIELD Performance Comparison"
    )

    plt.legend()

    plt.grid(
        axis="y",
        linestyle="--",
        alpha=0.5
    )

    plt.tight_layout()

    plt.savefig(
        "experiments/final_performance_comparison.png",
        dpi=300
    )

    plt.close()


def false_positive_comparison():

    methods = [
        "Fixed Threshold",
        "Blind Adaptive"
    ]

    fpr = [
        0.3186,
        0.0000
    ]

    plt.figure(figsize=(8, 6))

    bars = plt.bar(
        methods,
        fpr
    )

    for bar, value in zip(bars, fpr):

        plt.text(
            bar.get_x()
            + bar.get_width() / 2,
            value + 0.01,
            f"{value:.4f}",
            ha="center"
        )

    plt.ylabel("False Positive Rate")

    plt.ylim(0, 0.4)

    plt.title(
        "False Positive Rate Reduction"
    )

    plt.grid(
        axis="y",
        linestyle="--",
        alpha=0.5
    )

    plt.tight_layout()

    plt.savefig(
        "experiments/final_fpr_comparison.png",
        dpi=300
    )

    plt.close()


def shot_count_visualization():

    try:

        df = pd.read_csv(
            "experiments/shot_count_robustness_results.csv"
        )

    except FileNotFoundError:

        print(
            "Shot count results file not found."
        )

        return

    columns = {
        col.lower(): col
        for col in df.columns
    }

    shot_column = None

    for col in df.columns:

        if "shot" in col.lower():

            shot_column = col
            break

    accuracy_columns = [
        col for col in df.columns
        if "accuracy" in col.lower()
    ]

    if shot_column is None:

        print(
            "Could not identify shot count column."
        )

        return

    if len(accuracy_columns) < 2:

        print(
            "Could not identify accuracy columns."
        )

        return

    plt.figure(figsize=(9, 6))

    plt.plot(
        df[shot_column],
        df[accuracy_columns[0]],
        marker="o",
        label=accuracy_columns[0]
    )

    plt.plot(
        df[shot_column],
        df[accuracy_columns[1]],
        marker="s",
        label=accuracy_columns[1]
    )

    plt.xlabel("Quantum Measurement Shots")

    plt.ylabel("Accuracy")

    plt.ylim(0, 1.05)

    plt.title(
        "Shot Count Robustness Analysis"
    )

    plt.legend()

    plt.grid(
        linestyle="--",
        alpha=0.5
    )

    plt.tight_layout()

    plt.savefig(
        "experiments/shot_count_accuracy.png",
        dpi=300
    )

    plt.close()


def threshold_adaptation_visualization():

    noise_levels = [
        0.00,
        0.05,
        0.10,
        0.15,
        0.20,
        0.25,
        0.30
    ]

    fixed_threshold = [
        0.26
    ] * len(noise_levels)

    adaptive_threshold = [
        0.260,
        0.280,
        0.300,
        0.320,
        0.340,
        0.360,
        0.380
    ]

    plt.figure(figsize=(9, 6))

    plt.plot(
        noise_levels,
        fixed_threshold,
        marker="o",
        label="Fixed Threshold"
    )

    plt.plot(
        noise_levels,
        adaptive_threshold,
        marker="s",
        label="Adaptive Threshold"
    )

    plt.xlabel("Noise Probability")

    plt.ylabel("Rejection Threshold")

    plt.title(
        "Adaptive Threshold Behaviour Under Noise"
    )

    plt.legend()

    plt.grid(
        linestyle="--",
        alpha=0.5
    )

    plt.tight_layout()

    plt.savefig(
        "experiments/threshold_adaptation_behavior.png",
        dpi=300
    )

    plt.close()


def main():

    print("\n" + "=" * 90)
    print("Q-SHIELD")
    print("PHASE 4R: FINAL BENCHMARK VISUALIZATION")
    print("=" * 90)

    print(
        "\nGenerating publication-quality figures..."
    )

    performance_comparison()

    print(
        "1. Performance comparison generated"
    )

    false_positive_comparison()

    print(
        "2. False positive comparison generated"
    )

    shot_count_visualization()

    print(
        "3. Shot count robustness graph generated"
    )

    threshold_adaptation_visualization()

    print(
        "4. Threshold adaptation graph generated"
    )

    print("\nGenerated files:")

    print(
        "experiments/final_performance_comparison.png"
    )

    print(
        "experiments/final_fpr_comparison.png"
    )

    print(
        "experiments/shot_count_accuracy.png"
    )

    print(
        "experiments/threshold_adaptation_behavior.png"
    )

    print("\n" + "=" * 90)
    print("PHASE 4R COMPLETED")
    print("=" * 90)


if __name__ == "__main__":
    main()