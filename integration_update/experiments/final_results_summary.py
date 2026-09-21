"""
Q-SHIELD
PHASE 4S: FINAL COMPREHENSIVE RESULTS SUMMARY

Consolidates major experimental findings from
the complete Q-SHIELD evaluation pipeline.
"""

import pandas as pd
import matplotlib.pyplot as plt


def print_header(title):

    print("\n" + "=" * 100)
    print(title)
    print("=" * 100)


def main():

    print_header(
        "Q-SHIELD | PHASE 4S: FINAL COMPREHENSIVE RESULTS SUMMARY"
    )

    # ---------------------------------------------------------
    # MASTER RESULTS
    # ---------------------------------------------------------

    results = [

        {
            "Experiment": "Cross-Trial Validation",
            "Method": "Fixed Threshold",
            "Accuracy": 0.9375,
            "Precision": 0.9000,
            "Recall": 1.0000,
            "F1 Score": 0.9444,
            "FPR": 0.1250
        },

        {
            "Experiment": "Expanded Robustness",
            "Method": "Fixed Threshold",
            "Accuracy": 0.8913,
            "Precision": 0.8276,
            "Recall": 1.0000,
            "F1 Score": 0.9057,
            "FPR": 0.2273
        },

        {
            "Experiment": "Adaptive Threshold",
            "Method": "Adaptive",
            "Accuracy": 1.0000,
            "Precision": 1.0000,
            "Recall": 1.0000,
            "F1 Score": 1.0000,
            "FPR": 0.0000
        },

        {
            "Experiment": "Blind Adaptive Validation",
            "Method": "Blind Adaptive",
            "Accuracy": 1.0000,
            "Precision": 1.0000,
            "Recall": 1.0000,
            "F1 Score": 1.0000,
            "FPR": 0.0000
        },

        {
            "Experiment": "Adaptive Ablation",
            "Method": "Blind Adaptive",
            "Accuracy": 0.9300,
            "Precision": 0.8840,
            "Recall": 1.0000,
            "F1 Score": 0.9384,
            "FPR": 0.1500
        },

        {
            "Experiment": "Paired Monte Carlo",
            "Method": "Fixed Threshold",
            "Accuracy": 0.7973,
            "Precision": 0.6614,
            "Recall": 1.0000,
            "F1 Score": 0.7904,
            "FPR": 0.3186
        },

        {
            "Experiment": "Paired Monte Carlo",
            "Method": "Blind Adaptive",
            "Accuracy": 1.0000,
            "Precision": 1.0000,
            "Recall": 1.0000,
            "F1 Score": 1.0000,
            "FPR": 0.0000
        },

        {
            "Experiment": "Multi-Noise Robustness",
            "Method": "Fixed Threshold",
            "Accuracy": 0.7311,
            "Precision": 0.6681,
            "Recall": 0.7850,
            "F1 Score": 0.7218,
            "FPR": 0.3120
        },

        {
            "Experiment": "Multi-Noise Robustness",
            "Method": "Blind Adaptive",
            "Accuracy": 0.8467,
            "Precision": 0.9888,
            "Recall": 0.6625,
            "F1 Score": 0.7934,
            "FPR": 0.0060
        }

    ]

    df = pd.DataFrame(results)

    print("\nMASTER EXPERIMENTAL RESULTS\n")

    print(
        df.to_string(
            index=False
        )
    )

    # ---------------------------------------------------------
    # SAVE MASTER TABLE
    # ---------------------------------------------------------

    df.to_csv(
        "experiments/final_master_results.csv",
        index=False
    )

    # ---------------------------------------------------------
    # MULTI-NOISE IMPROVEMENT ANALYSIS
    # ---------------------------------------------------------

    print_header(
        "KEY MULTI-NOISE ROBUSTNESS FINDINGS"
    )

    fixed = df[
        (
            df["Experiment"]
            == "Multi-Noise Robustness"
        )
        &
        (
            df["Method"]
            == "Fixed Threshold"
        )
    ].iloc[0]

    adaptive = df[
        (
            df["Experiment"]
            == "Multi-Noise Robustness"
        )
        &
        (
            df["Method"]
            == "Blind Adaptive"
        )
    ].iloc[0]

    accuracy_improvement = (
        adaptive["Accuracy"]
        - fixed["Accuracy"]
    )

    precision_improvement = (
        adaptive["Precision"]
        - fixed["Precision"]
    )

    f1_improvement = (
        adaptive["F1 Score"]
        - fixed["F1 Score"]
    )

    fpr_reduction = (
        fixed["FPR"]
        - adaptive["FPR"]
    )

    recall_change = (
        adaptive["Recall"]
        - fixed["Recall"]
    )

    print(
        f"\nAccuracy Improvement: "
        f"{accuracy_improvement:.4f}"
    )

    print(
        f"Precision Improvement: "
        f"{precision_improvement:.4f}"
    )

    print(
        f"F1 Score Improvement: "
        f"{f1_improvement:.4f}"
    )

    print(
        f"False Positive Rate Reduction: "
        f"{fpr_reduction:.4f}"
    )

    print(
        f"Recall Change: "
        f"{recall_change:.4f}"
    )

    # ---------------------------------------------------------
    # SCIENTIFIC INTERPRETATION
    # ---------------------------------------------------------

    print_header(
        "FINAL SCIENTIFIC INTERPRETATION"
    )

    print(
        """
1. Fixed thresholding is highly sensitive to quantum channel noise.

2. Blind adaptive thresholding substantially reduces false
   positives across heterogeneous noise channels.

3. Multi-noise evaluation demonstrates a trade-off between
   false-positive suppression and attack recall.

4. The adaptive method improves overall accuracy and F1 score
   under heterogeneous quantum noise.

5. Results indicate that threshold adaptation is particularly
   valuable for reducing false alarms in noisy quantum channels.

6. The perfect results observed in controlled experiments should
   not be generalized to all noise conditions.

7. Multi-noise robustness evaluation provides a more realistic
   estimate of system performance.
"""
    )

    # ---------------------------------------------------------
    # FINAL COMPARISON GRAPH
    # ---------------------------------------------------------

    metrics = [
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score"
    ]

    fixed_values = [
        fixed["Accuracy"],
        fixed["Precision"],
        fixed["Recall"],
        fixed["F1 Score"]
    ]

    adaptive_values = [
        adaptive["Accuracy"],
        adaptive["Precision"],
        adaptive["Recall"],
        adaptive["F1 Score"]
    ]

    x = range(len(metrics))

    width = 0.35

    plt.figure(figsize=(10, 6))

    plt.bar(
        [i - width / 2 for i in x],
        fixed_values,
        width,
        label="Fixed Threshold"
    )

    plt.bar(
        [i + width / 2 for i in x],
        adaptive_values,
        width,
        label="Blind Adaptive"
    )

    plt.xticks(
        x,
        metrics
    )

    plt.ylabel(
        "Performance Score"
    )

    plt.ylim(
        0,
        1.1
    )

    plt.title(
        "Q-SHIELD Multi-Noise Performance Comparison"
    )

    plt.legend()

    plt.grid(
        axis="y",
        linestyle="--",
        alpha=0.5
    )

    plt.tight_layout()

    plt.savefig(
        "experiments/final_multi_noise_comparison.png",
        dpi=300
    )

    plt.close()

    # ---------------------------------------------------------
    # FPR GRAPH
    # ---------------------------------------------------------

    plt.figure(figsize=(7, 6))

    methods = [
        "Fixed Threshold",
        "Blind Adaptive"
    ]

    fpr_values = [
        fixed["FPR"],
        adaptive["FPR"]
    ]

    bars = plt.bar(
        methods,
        fpr_values
    )

    for bar, value in zip(
        bars,
        fpr_values
    ):

        plt.text(
            bar.get_x()
            + bar.get_width() / 2,
            value + 0.01,
            f"{value:.4f}",
            ha="center"
        )

    plt.ylabel(
        "False Positive Rate"
    )

    plt.title(
        "False Positive Reduction Under Multiple Noise Channels"
    )

    plt.grid(
        axis="y",
        linestyle="--",
        alpha=0.5
    )

    plt.tight_layout()

    plt.savefig(
        "experiments/final_multi_noise_fpr.png",
        dpi=300
    )

    plt.close()

    # ---------------------------------------------------------
    # COMPLETION
    # ---------------------------------------------------------

    print_header(
        "FINAL OUTPUT FILES"
    )

    print(
        "1. experiments/final_master_results.csv"
    )

    print(
        "2. experiments/final_multi_noise_comparison.png"
    )

    print(
        "3. experiments/final_multi_noise_fpr.png"
    )

    print_header(
        "PHASE 4S COMPLETED — EXPERIMENTAL EVALUATION COMPLETE"
    )


if __name__ == "__main__":
    main()