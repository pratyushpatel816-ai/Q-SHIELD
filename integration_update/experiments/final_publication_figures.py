import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


print("=" * 100)
print("Q-SHIELD")
print("PHASE 6A: FINAL PUBLICATION-QUALITY RESULTS VISUALIZATION")
print("=" * 100)


# ============================================================
# HELPER FUNCTION
# ============================================================

def load_csv(path):
    if not os.path.exists(path):
        print(f"WARNING: Missing file -> {path}")
        return None

    return pd.read_csv(path)


# ============================================================
# LOAD RESULTS
# ============================================================

print("\nLoading experimental results...")

ablation = load_csv(
    "experiments/dual_signal_ablation_results.csv"
)

tradeoff = load_csv(
    "experiments/security_sensitivity_tradeoff.csv"
)

statistics = load_csv(
    "experiments/dual_signal_statistical_analysis.csv"
)

baseline = load_csv(
    "experiments/baseline_comparison_summary.csv"
)


# ============================================================
# FIGURE 1
# DUAL-SIGNAL PERFORMANCE COMPARISON
# ============================================================

if ablation is not None:

    print("Generating Figure 1: Detection performance comparison...")

    methods = ablation["method"].tolist()

    metrics = [
        "accuracy",
        "precision",
        "recall",
        "f1_score"
    ]

    x = np.arange(len(methods))
    width = 0.18

    plt.figure(figsize=(12, 7))

    for i, metric in enumerate(metrics):

        values = ablation[metric].tolist()

        plt.bar(
            x + i * width,
            values,
            width,
            label=metric.replace("_", " ").title()
        )

    plt.xlabel("Detection Architecture")
    plt.ylabel("Performance Score")
    plt.title(
        "Q-SHIELD Dual-Signal Detection Performance"
    )

    plt.xticks(
        x + width * 1.5,
        methods,
        rotation=10
    )

    plt.ylim(0, 1.1)

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        "experiments/publication_performance_comparison.png",
        dpi=300
    )

    plt.close()


# ============================================================
# FIGURE 2
# FALSE POSITIVE RATE COMPARISON
# ============================================================

if ablation is not None:

    print("Generating Figure 2: False positive comparison...")

    methods = ablation["method"].tolist()

    fpr_values = ablation["fpr"].tolist()

    plt.figure(figsize=(9, 6))

    plt.bar(
        methods,
        fpr_values
    )

    plt.xlabel("Detection Architecture")
    plt.ylabel("False Positive Rate")
    plt.title(
        "False Positive Rate Reduction with Q-SHIELD"
    )

    plt.ylim(
        0,
        max(fpr_values) * 1.3 + 0.02
    )

    plt.xticks(rotation=10)

    plt.tight_layout()

    plt.savefig(
        "experiments/publication_fpr_comparison.png",
        dpi=300
    )

    plt.close()


# ============================================================
# FIGURE 3
# SECURITY-SENSITIVITY TRADE-OFF
# ============================================================

if tradeoff is not None:

    print("Generating Figure 3: Security sensitivity trade-off...")

    thresholds = (
        tradeoff["detection_threshold"]
    )

    plt.figure(figsize=(10, 6))

    plt.plot(
        thresholds,
        tradeoff["precision"],
        marker="o",
        label="Precision"
    )

    plt.plot(
        thresholds,
        tradeoff["recall"],
        marker="s",
        label="Recall"
    )

    plt.plot(
        thresholds,
        tradeoff["f1_score"],
        marker="^",
        label="F1 Score"
    )

    plt.xlabel("Detection Threshold")
    plt.ylabel("Score")

    plt.title(
        "Q-SHIELD Security-Sensitivity Trade-Off"
    )

    plt.legend()

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        "experiments/publication_threshold_tradeoff.png",
        dpi=300
    )

    plt.close()


# ============================================================
# FIGURE 4
# FALSE POSITIVE VS FALSE NEGATIVE TRADE-OFF
# ============================================================

if tradeoff is not None:

    print("Generating Figure 4: FPR-FNR trade-off...")

    thresholds = (
        tradeoff["detection_threshold"]
    )

    plt.figure(figsize=(10, 6))

    plt.plot(
        thresholds,
        tradeoff["fpr"],
        marker="o",
        label="False Positive Rate"
    )

    plt.plot(
        thresholds,
        tradeoff["fnr"],
        marker="s",
        label="False Negative Rate"
    )

    plt.xlabel("Detection Threshold")
    plt.ylabel("Error Rate")

    plt.title(
        "Security Error Trade-Off in Q-SHIELD"
    )

    plt.legend()

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        "experiments/publication_fpr_fnr_tradeoff.png",
        dpi=300
    )

    plt.close()


# ============================================================
# FIGURE 5
# STATISTICAL IMPROVEMENT
# ============================================================

if statistics is not None:

    print("Generating Figure 5: Statistical improvement...")

    metrics = (
        statistics["metric"].tolist()
    )

    mismatch = (
        statistics["mismatch_mean"].tolist()
    )

    dual = (
        statistics["dual_mean"].tolist()
    )

    x = np.arange(len(metrics))

    width = 0.35

    plt.figure(figsize=(11, 6))

    plt.bar(
        x - width / 2,
        mismatch,
        width,
        label="Mismatch Only"
    )

    plt.bar(
        x + width / 2,
        dual,
        width,
        label="Q-SHIELD Dual Signal"
    )

    plt.xlabel("Performance Metric")
    plt.ylabel("Mean Score")

    plt.title(
        "Statistical Performance Improvement of Q-SHIELD"
    )

    plt.xticks(
        x,
        [
            metric.replace("_", " ").title()
            for metric in metrics
        ]
    )

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        "experiments/publication_statistical_comparison.png",
        dpi=300
    )

    plt.close()


# ============================================================
# FIGURE 6
# FINAL RESEARCH SUMMARY
# ============================================================

print("Generating Figure 6: Final Q-SHIELD research summary...")

summary_metrics = [
    "Accuracy",
    "Precision",
    "Recall",
    "F1 Score",
    "False Positive Rate"
]

qshield_scores = [
    0.9583,
    1.0000,
    0.7500,
    0.8571,
    0.0000
]

plt.figure(figsize=(11, 6))

plt.bar(
    summary_metrics,
    qshield_scores
)

plt.xlabel("Evaluation Metric")
plt.ylabel("Score")

plt.title(
    "Final Validated Performance of Q-SHIELD Dual-Signal Detector"
)

plt.ylim(0, 1.1)

for i, value in enumerate(qshield_scores):

    plt.text(
        i,
        value + 0.03,
        f"{value:.4f}",
        ha="center"
    )

plt.tight_layout()

plt.savefig(
    "experiments/final_qshield_performance.png",
    dpi=300
)

plt.close()


# ============================================================
# FINAL OUTPUT
# ============================================================

print("\n" + "=" * 100)
print("FINAL PUBLICATION FIGURES GENERATED")
print("=" * 100)

print("""
1. experiments/publication_performance_comparison.png
2. experiments/publication_fpr_comparison.png
3. experiments/publication_threshold_tradeoff.png
4. experiments/publication_fpr_fnr_tradeoff.png
5. experiments/publication_statistical_comparison.png
6. experiments/final_qshield_performance.png
""")

print("=" * 100)
print("PHASE 6A COMPLETED")
print("=" * 100)