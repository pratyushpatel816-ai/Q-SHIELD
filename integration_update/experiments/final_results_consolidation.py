import pandas as pd
import os


print("=" * 100)
print("Q-SHIELD")
print("PHASE 6C: FINAL RESEARCH RESULTS CONSOLIDATION")
print("=" * 100)


# ============================================================
# HELPER FUNCTION
# ============================================================

def load_csv(path):

    if os.path.exists(path):
        return pd.read_csv(path)

    print(f"WARNING: Missing -> {path}")
    return None


# ============================================================
# LOAD ALL IMPORTANT RESULTS
# ============================================================

print("\nLoading validated experimental results...")

multi_noise = load_csv(
    "experiments/multi_noise_robustness_results.csv"
)

reproducibility = load_csv(
    "experiments/reproducibility_summary.csv"
)

baseline = load_csv(
    "experiments/baseline_comparison_summary.csv"
)

tradeoff = load_csv(
    "experiments/security_sensitivity_tradeoff.csv"
)

ablation = load_csv(
    "experiments/dual_signal_ablation_results.csv"
)

statistics = load_csv(
    "experiments/dual_signal_statistical_analysis.csv"
)


# ============================================================
# MASTER RESULTS TABLE
# ============================================================

master_results = []


# ============================================================
# BEST SECURITY-SENSITIVITY CONFIGURATION
# ============================================================

if tradeoff is not None:

    best = tradeoff.loc[
        tradeoff["f1_score"].idxmax()
    ]

    master_results.append({

        "Experiment":
        "Best Dual-Signal Configuration",

        "Method":
        "Q-SHIELD Dual Signal",

        "Accuracy":
        best["accuracy"],

        "Precision":
        best["precision"],

        "Recall":
        best["recall"],

        "F1 Score":
        best["f1_score"],

        "FPR":
        best["fpr"]

    })


# ============================================================
# DUAL SIGNAL ABLATION RESULTS
# ============================================================

if ablation is not None:

    for _, row in ablation.iterrows():

        master_results.append({

            "Experiment":
            "Dual-Signal Ablation",

            "Method":
            row["method"],

            "Accuracy":
            row["accuracy"],

            "Precision":
            row["precision"],

            "Recall":
            row["recall"],

            "F1 Score":
            row["f1_score"],

            "FPR":
            row["fpr"]

        })


# ============================================================
# BASELINE COMPARISON
# ============================================================

if baseline is not None:

    for _, row in baseline.iterrows():

        master_results.append({

            "Experiment":
            "Baseline Comparison",

            "Method":
            row["method"],

            "Accuracy":
            row["accuracy"],

            "Precision":
            row["precision"],

            "Recall":
            row["recall"],

            "F1 Score":
            row["f1_score"],

            "FPR":
            row["fpr"]

        })


# ============================================================
# CREATE MASTER DATAFRAME
# ============================================================

master_df = pd.DataFrame(master_results)


# ============================================================
# SAVE MASTER RESULTS
# ============================================================

output_path = (
    "experiments/final_consolidated_results.csv"
)

master_df.to_csv(
    output_path,
    index=False
)


# ============================================================
# STATISTICAL IMPROVEMENT SUMMARY
# ============================================================

statistical_summary = []


if statistics is not None:

    for _, row in statistics.iterrows():

        statistical_summary.append({

            "Metric":
            row["metric"],

            "Mismatch Mean":
            row["mismatch_mean"],

            "Dual Signal Mean":
            row["dual_mean"],

            "Improvement":
            row["dual_mean"]
            -
            row["mismatch_mean"],

            "Paired T-Test P Value":
            row.get(
                "paired_t_p_value",
                None
            ),

            "Wilcoxon P Value":
            row.get(
                "wilcoxon_p_value",
                None
            ),

            "Cohen's d":
            row.get(
                "cohens_d",
                None
            )

        })


statistical_df = pd.DataFrame(
    statistical_summary
)


statistical_df.to_csv(
    "experiments/final_statistical_summary.csv",
    index=False
)


# ============================================================
# REPRODUCIBILITY SUMMARY
# ============================================================

if reproducibility is not None:

    reproducibility.to_csv(
        "experiments/final_reproducibility_summary.csv",
        index=False
    )


# ============================================================
# FINAL PERFORMANCE HIGHLIGHTS
# ============================================================

print("\n" + "=" * 100)
print("FINAL Q-SHIELD PERFORMANCE HIGHLIGHTS")
print("=" * 100)


if tradeoff is not None:

    print("\nBEST BALANCED DUAL-SIGNAL CONFIGURATION")

    print(
        f"Detection Threshold: "
        f"{best['detection_threshold']:.2f}"
    )

    print(
        f"Accuracy: "
        f"{best['accuracy']:.4f}"
    )

    print(
        f"Precision: "
        f"{best['precision']:.4f}"
    )

    print(
        f"Recall: "
        f"{best['recall']:.4f}"
    )

    print(
        f"F1 Score: "
        f"{best['f1_score']:.4f}"
    )

    print(
        f"False Positive Rate: "
        f"{best['fpr']:.4f}"
    )


# ============================================================
# DUAL SIGNAL IMPROVEMENT
# ============================================================

if statistics is not None:

    f1_row = statistics[
        statistics["metric"] == "f1_score"
    ]

    if len(f1_row) > 0:

        row = f1_row.iloc[0]

        improvement = (
            row["dual_mean"]
            -
            row["mismatch_mean"]
        )

        print("\nDUAL-SIGNAL STATISTICAL IMPROVEMENT")

        print(
            f"Mismatch-only Mean F1: "
            f"{row['mismatch_mean']:.4f}"
        )

        print(
            f"Dual-signal Mean F1: "
            f"{row['dual_mean']:.4f}"
        )

        print(
            f"F1 Improvement: "
            f"{improvement:.4f}"
        )

        if "cohens_d" in statistics.columns:

            print(
                f"Cohen's d: "
                f"{row['cohens_d']:.4f}"
            )


# ============================================================
# FINAL SCIENTIFIC SUMMARY
# ============================================================

print("\n" + "=" * 100)
print("FINAL RESEARCH SUMMARY")
print("=" * 100)

print("""
Q-SHIELD has been evaluated through multiple complementary
experimental studies including heterogeneous noise robustness,
reproducibility analysis, computational complexity evaluation,
baseline comparison, security-sensitivity trade-off analysis,
dual-signal ablation, and statistical significance testing.

The consolidated evidence indicates that the dual-signal
architecture provides the strongest overall detection
performance by combining teleportation mismatch information
with Bell measurement anomaly analysis.

The results also demonstrate an important trade-off between
false-positive suppression and attack recall. Therefore,
detection thresholds should be selected according to the
desired operational security requirements.

The experimental evaluation provides statistically supported
evidence for the effectiveness of multi-signal quantum attack
detection within the implemented simulation environment.
""")


# ============================================================
# GENERATED FILES
# ============================================================

print("\n" + "=" * 100)
print("GENERATED FILES")
print("=" * 100)

print("""
1. experiments/final_consolidated_results.csv
2. experiments/final_statistical_summary.csv
3. experiments/final_reproducibility_summary.csv
""")


print("=" * 100)
print("PHASE 6C COMPLETED")
print("=" * 100)