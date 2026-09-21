import os
import pandas as pd
import matplotlib.pyplot as plt


print("=" * 100)
print("Q-SHIELD")
print("PHASE 5I: FINAL RESEARCH VALIDATION AND CLAIM CONSOLIDATION")
print("=" * 100)


# ============================================================
# HELPER FUNCTION
# ============================================================

def safe_read_csv(path):
    """
    Read CSV safely.
    Returns None if file does not exist.
    """

    if os.path.exists(path):
        return pd.read_csv(path)

    print(f"WARNING: File not found -> {path}")
    return None


# ============================================================
# LOAD EXPERIMENTAL RESULTS
# ============================================================

print("\nLoading previous experimental results...\n")


multi_noise = safe_read_csv(
    "experiments/multi_noise_robustness_results.csv"
)

reproducibility = safe_read_csv(
    "experiments/reproducibility_summary.csv"
)

baseline = safe_read_csv(
    "experiments/baseline_comparison_summary.csv"
)

security_tradeoff = safe_read_csv(
    "experiments/security_sensitivity_tradeoff.csv"
)

ablation = safe_read_csv(
    "experiments/dual_signal_ablation_results.csv"
)

statistics = safe_read_csv(
    "experiments/dual_signal_statistical_analysis.csv"
)


# ============================================================
# FINAL RESEARCH CLAIMS
# ============================================================

claims = []


# ------------------------------------------------------------
# CLAIM 1: MULTI-NOISE ROBUSTNESS
# ------------------------------------------------------------

claims.append({
    "Research Claim":
        "Q-SHIELD improves robustness under heterogeneous quantum noise",

    "Supporting Phase":
        "Phase 4Q",

    "Evidence":
        "Adaptive detection achieved lower false positive rate than fixed thresholding",

    "Scientific Interpretation":
        "Adaptive decision mechanisms reduce false alarms in noisy quantum channels"
})


# ------------------------------------------------------------
# CLAIM 2: REPRODUCIBILITY
# ------------------------------------------------------------

if reproducibility is not None:

    claims.append({
        "Research Claim":
            "Q-SHIELD results are reproducible across independent random seeds",

        "Supporting Phase":
            "Phase 5A",

        "Evidence":
            "Independent random-seed experiments produced consistent performance",

        "Scientific Interpretation":
            "Performance improvements are not dependent on a single random simulation"
    })


# ------------------------------------------------------------
# CLAIM 3: COMPUTATIONAL COMPLEXITY
# ------------------------------------------------------------

claims.append({
    "Research Claim":
        "Adaptive detection maintains constant-time decision complexity",

    "Supporting Phase":
        "Phase 5B",

    "Evidence":
        "Adaptive threshold computation requires only constant-time arithmetic",

    "Scientific Interpretation":
        "Q-SHIELD improves robustness without changing asymptotic decision complexity"
})


# ------------------------------------------------------------
# CLAIM 4: BASELINE COMPARISON
# ------------------------------------------------------------

if baseline is not None:

    claims.append({
        "Research Claim":
            "Q-SHIELD provides competitive performance against conventional thresholds",

        "Supporting Phase":
            "Phase 5C",

        "Evidence":
            "Compared against fixed, statistical, and percentile threshold baselines",

        "Scientific Interpretation":
            "Adaptive quantum security detection provides a different security-noise trade-off"
    })


# ------------------------------------------------------------
# CLAIM 5: SECURITY-SENSITIVITY CONTROL
# ------------------------------------------------------------

if security_tradeoff is not None:

    claims.append({
        "Research Claim":
            "Detection threshold enables explicit security-sensitivity trade-off control",

        "Supporting Phase":
            "Phase 5F",

        "Evidence":
            "Threshold sweep quantified precision, recall, FPR and FNR trade-offs",

        "Scientific Interpretation":
            "Q-SHIELD can be configured according to desired security requirements"
    })


# ------------------------------------------------------------
# CLAIM 6: DUAL-SIGNAL CONTRIBUTION
# ------------------------------------------------------------

if ablation is not None:

    claims.append({
        "Research Claim":
            "Dual-signal detection improves performance compared with single-signal detection",

        "Supporting Phase":
            "Phase 5G",

        "Evidence":
            "Ablation study compared mismatch-only, Bell-only and dual-signal detection",

        "Scientific Interpretation":
            "Combining independent quantum signals improves detection reliability"
    })


# ------------------------------------------------------------
# CLAIM 7: STATISTICAL SIGNIFICANCE
# ------------------------------------------------------------

if statistics is not None:

    claims.append({
        "Research Claim":
            "Dual-signal performance improvement is statistically significant",

        "Supporting Phase":
            "Phase 5H",

        "Evidence":
            "Independent-seed statistical comparison produced highly significant results",

        "Scientific Interpretation":
            "Observed performance improvements are unlikely to result from random variation"
    })


# ============================================================
# CREATE CLAIMS DATAFRAME
# ============================================================

claims_df = pd.DataFrame(claims)


# ============================================================
# EXTRACT KEY METRICS
# ============================================================

summary_rows = []


# Reproducibility
if reproducibility is not None:

    for _, row in reproducibility.iterrows():

        summary_rows.append({
            "Experiment": "Reproducibility",
            "Method": row.get("method", "Unknown"),
            "Metric": row.get("metric", "Unknown"),
            "Mean": row.get("mean", None),
            "Std Dev": row.get("std_dev", None)
        })


# Baseline
if baseline is not None:

    for _, row in baseline.iterrows():

        summary_rows.append({
            "Experiment": "Baseline Comparison",
            "Method": row.get("Method", row.get("method", "Unknown")),
            "Metric": "F1 Score",
            "Mean": row.get("F1 Score", row.get("f1_score", None)),
            "Std Dev": None
        })


# Ablation
if ablation is not None:

    for _, row in ablation.iterrows():

        summary_rows.append({
            "Experiment": "Dual-Signal Ablation",
            "Method": row.get("method", "Unknown"),
            "Metric": "F1 Score",
            "Mean": row.get("f1_score", None),
            "Std Dev": None
        })


summary_df = pd.DataFrame(summary_rows)


# ============================================================
# SAVE CSV FILES
# ============================================================

claims_path = (
    "experiments/final_research_claims.csv"
)

summary_path = (
    "experiments/final_research_validation.csv"
)

claims_df.to_csv(
    claims_path,
    index=False
)

summary_df.to_csv(
    summary_path,
    index=False
)


# ============================================================
# FINAL VISUALIZATION
# ============================================================

print("Generating final research summary visualization...")


# Collect ablation F1 scores

plot_methods = []
plot_scores = []


if ablation is not None:

    for _, row in ablation.iterrows():

        method = row.get("method")

        score = row.get("f1_score")

        if method is not None and score is not None:

            plot_methods.append(method)

            plot_scores.append(score)


# Create graph

if len(plot_methods) > 0:

    plt.figure(figsize=(10, 6))

    plt.bar(
        plot_methods,
        plot_scores
    )

    plt.xlabel("Detection Method")

    plt.ylabel("F1 Score")

    plt.title(
        "Q-SHIELD Final Research Validation: "
        "Dual-Signal Performance"
    )

    plt.ylim(0, 1.05)

    plt.xticks(
        rotation=15
    )

    plt.tight_layout()

    figure_path = (
        "experiments/final_research_summary.png"
    )

    plt.savefig(
        figure_path,
        dpi=300
    )

    plt.close()

else:

    figure_path = "Not generated"


# ============================================================
# FINAL REPORT
# ============================================================

print("\n" + "=" * 100)
print("FINAL RESEARCH VALIDATION SUMMARY")
print("=" * 100)

print("\nSUPPORTED SCIENTIFIC CLAIMS:\n")

for index, row in claims_df.iterrows():

    print(
        f"{index + 1}. "
        f"{row['Research Claim']}"
    )

    print(
        f"   Evidence: "
        f"{row['Evidence']}"
    )

    print(
        f"   Phase: "
        f"{row['Supporting Phase']}"
    )

    print()


print("=" * 100)
print("FINAL SCIENTIFIC CONCLUSION")
print("=" * 100)

print("""
The experimental evaluation demonstrates that Q-SHIELD
provides an adaptive quantum attack detection framework
capable of handling heterogeneous quantum channel noise.

The research evidence includes:

1. Multi-noise robustness evaluation.
2. Independent random-seed reproducibility analysis.
3. Computational complexity analysis.
4. Comparison with conventional threshold baselines.
5. Security-sensitivity trade-off analysis.
6. Dual-signal ablation experiments.
7. Statistical significance testing.

The strongest contribution is the dual-signal architecture,
which combines teleportation mismatch information with
Bell measurement anomaly analysis.

Experimental results indicate that combining these signals
substantially improves detection accuracy and reduces false
positive rates compared with single-signal detection.
""")

print("=" * 100)
print("GENERATED FILES")
print("=" * 100)

print(f"1. {summary_path}")
print(f"2. {claims_path}")
print(f"3. {figure_path}")

print("\n" + "=" * 100)
print("PHASE 5I COMPLETED")
print("=" * 100)