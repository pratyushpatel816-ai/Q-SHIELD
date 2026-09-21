import csv
import os
import matplotlib.pyplot as plt


def read_csv(filename):
    with open(filename, "r") as file:
        return list(csv.DictReader(file))


def plot_threshold_optimization():

    filename = (
        "experiments/"
        "threshold_optimization_results.csv"
    )

    data = read_csv(filename)

    thresholds = [
        float(row["threshold"])
        for row in data
    ]

    tpr = [
        float(row["TPR"])
        for row in data
    ]

    fpr = [
        float(row["FPR"])
        for row in data
    ]

    accuracy = [
        float(row["accuracy"])
        for row in data
    ]

    plt.figure(figsize=(10, 6))

    plt.plot(
        thresholds,
        tpr,
        marker="o",
        label="True Positive Rate"
    )

    plt.plot(
        thresholds,
        fpr,
        marker="s",
        label="False Positive Rate"
    )

    plt.plot(
        thresholds,
        accuracy,
        marker="^",
        label="Accuracy"
    )

    # Optimal threshold discovered in Phase 4F
    plt.axvline(
        x=0.26,
        linestyle="--",
        label="Optimal Threshold = 0.26"
    )

    plt.xlabel("Rejection Threshold")
    plt.ylabel("Performance Metric")

    plt.title(
        "Q-SHIELD Threshold Optimization Performance"
    )

    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()

    output = (
        "experiments/"
        "threshold_optimization_graph.png"
    )

    plt.savefig(
        output,
        dpi=300
    )

    plt.close()

    return output


def plot_attack_vs_noise():

    filename = (
        "experiments/"
        "attack_vs_noise_results.csv"
    )

    data = read_csv(filename)

    scenarios = [
        row["scenario"]
        for row in data
    ]

    mismatch = [
        float(row["mean_mismatch"])
        for row in data
    ]

    fidelity = [
        float(row["mean_fidelity"])
        for row in data
    ]

    positions = list(
        range(len(scenarios))
    )

    plt.figure(figsize=(12, 6))

    plt.bar(
        positions,
        mismatch,
        label="Mean Mismatch Rate"
    )

    plt.plot(
        positions,
        fidelity,
        marker="o",
        linewidth=2,
        label="Mean Fidelity"
    )

    # Optimized rejection threshold
    plt.axhline(
        y=0.26,
        linestyle="--",
        linewidth=2,
        label="Optimized Threshold = 0.26"
    )

    plt.xticks(
        positions,
        scenarios,
        rotation=35,
        ha="right"
    )

    plt.xlabel("Experimental Scenario")
    plt.ylabel("Metric Value")

    plt.title(
        "Q-SHIELD: Attack vs Natural Noise Comparison"
    )

    plt.legend()

    plt.grid(
        axis="y",
        alpha=0.3
    )

    plt.tight_layout()

    output = (
        "experiments/"
        "attack_vs_noise_comparison.png"
    )

    plt.savefig(
        output,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    return output


def plot_confusion_matrix():

    # Results obtained from optimal threshold = 0.26
    matrix = [
        [4, 0],
        [0, 4]
    ]

    plt.figure(figsize=(6, 5))

    plt.imshow(matrix)

    plt.xticks(
        [0, 1],
        ["Predicted Normal", "Predicted Attack"]
    )

    plt.yticks(
        [0, 1],
        ["Actual Normal", "Actual Attack"]
    )

    for i in range(2):
        for j in range(2):

            plt.text(
                j,
                i,
                str(matrix[i][j]),
                ha="center",
                va="center",
                fontsize=18
            )

    plt.title(
        "Q-SHIELD Confusion Matrix\n"
        "Optimized Threshold = 0.26"
    )

    plt.xlabel("Predicted Class")
    plt.ylabel("Actual Class")

    plt.tight_layout()

    output = (
        "experiments/"
        "confusion_matrix.png"
    )

    plt.savefig(
        output,
        dpi=300
    )

    plt.close()

    return output


def run_visualization():

    print()
    print("=" * 80)
    print("Q-SHIELD")
    print("PHASE 4G: FINAL RESULTS VISUALIZATION")
    print("=" * 80)

    # Check required files
    required_files = [
        "experiments/threshold_optimization_results.csv",
        "experiments/attack_vs_noise_results.csv"
    ]

    for filename in required_files:

        if not os.path.exists(filename):

            raise FileNotFoundError(
                f"Required experiment file not found: "
                f"{filename}"
            )

    graph1 = plot_threshold_optimization()

    graph2 = plot_attack_vs_noise()

    graph3 = plot_confusion_matrix()

    print()
    print("Publication-quality graphs generated:")
    print(f"1. {graph1}")
    print(f"2. {graph2}")
    print(f"3. {graph3}")

    print()
    print("=" * 80)
    print("PHASE 4G COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    run_visualization()