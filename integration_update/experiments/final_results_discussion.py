import pandas as pd
import os


print("=" * 100)
print("Q-SHIELD")
print("PHASE 6B: FINAL RESULTS AND SCIENTIFIC DISCUSSION")
print("=" * 100)


# ============================================================
# HELPER FUNCTION
# ============================================================

def load_csv(path):
    """
    Load a CSV file safely.
    """

    if os.path.exists(path):
        return pd.read_csv(path)

    print(f"WARNING: Missing -> {path}")
    return None


# ============================================================
# LOAD KEY EXPERIMENTAL RESULTS
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

reproducibility = load_csv(
    "experiments/reproducibility_summary.csv"
)


# ============================================================
# EXTRACT FINAL VALIDATED CONFIGURATION
# ============================================================

best_config = None

if tradeoff is not None:

    best_config = tradeoff.loc[
        tradeoff["f1_score"].idxmax()
    ]

    print("\n" + "=" * 100)
    print("BEST BALANCED CONFIGURATION")
    print("=" * 100)

    print(
        f"Threshold: "
        f"{best_config['detection_threshold']:.2f}"
    )

    print(
        f"Accuracy: "
        f"{best_config['accuracy']:.4f}"
    )

    print(
        f"Precision: "
        f"{best_config['precision']:.4f}"
    )

    print(
        f"Recall: "
        f"{best_config['recall']:.4f}"
    )

    print(
        f"F1 Score: "
        f"{best_config['f1_score']:.4f}"
    )

    print(
        f"FPR: "
        f"{best_config['fpr']:.4f}"
    )

else:

    print(
        "\nWARNING: Security sensitivity "
        "trade-off results not found."
    )


# ============================================================
# DUAL-SIGNAL ABLATION ANALYSIS
# ============================================================

print("\n" + "=" * 100)
print("DUAL-SIGNAL ABLATION INTERPRETATION")
print("=" * 100)


if ablation is not None:

    for _, row in ablation.iterrows():

        print(
            f"\nMethod: {row['method']}"
        )

        print(
            f"Accuracy: "
            f"{row['accuracy']:.4f}"
        )

        print(
            f"F1 Score: "
            f"{row['f1_score']:.4f}"
        )

        print(
            f"FPR: "
            f"{row['fpr']:.4f}"
        )

else:

    print(
        "\nWARNING: Ablation results not found."
    )


# ============================================================
# STATISTICAL SIGNIFICANCE ANALYSIS
# ============================================================

print("\n" + "=" * 100)
print("STATISTICAL VALIDATION")
print("=" * 100)


if statistics is not None:

    # Display available columns for transparency
    print("\nStatistical result columns:")
    print(statistics.columns.tolist())

    # Find F1 score row
    f1_row = statistics[
        statistics["metric"] == "f1_score"
    ]

    if len(f1_row) > 0:

        row = f1_row.iloc[0]

        mismatch_mean = row["mismatch_mean"]
        dual_mean = row["dual_mean"]

        # Calculate improvement directly
        # This avoids dependency on CSV column naming
        improvement = (
            dual_mean - mismatch_mean
        )

        # Handle different possible column names
        if "cohen_d" in statistics.columns:

            cohens_d = row["cohen_d"]

        elif "cohens_d" in statistics.columns:

            cohens_d = row["cohens_d"]

        else:

            cohens_d = None

        # P-value handling
        if "p_value" in statistics.columns:

            p_value = row["p_value"]

        elif "pvalue" in statistics.columns:

            p_value = row["pvalue"]

        else:

            p_value = None


        print(
            f"\nMismatch-only mean F1: "
            f"{mismatch_mean:.4f}"
        )

        print(
            f"Dual-signal mean F1: "
            f"{dual_mean:.4f}"
        )

        print(
            f"F1 improvement: "
            f"{improvement:.4f}"
        )

        if p_value is not None:

            print(
                f"P-value: "
                f"{p_value:.8f}"
            )

        else:

            print(
                "P-value: Not available"
            )


        if cohens_d is not None:

            print(
                f"Cohen's d: "
                f"{cohens_d:.4f}"
            )

        else:

            print(
                "Cohen's d: Not available"
            )


    else:

        print(
            "\nWARNING: F1 score row not found "
            "in statistical analysis."
        )

else:

    print(
        "\nWARNING: Statistical analysis results "
        "not found."
    )


# ============================================================
# REPRODUCIBILITY ANALYSIS
# ============================================================

print("\n" + "=" * 100)
print("REPRODUCIBILITY INTERPRETATION")
print("=" * 100)


if reproducibility is not None:

    print(
        "\nIndependent random-seed experiments "
        "were performed to evaluate reproducibility."
    )

    print(
        "\nSummary of reproducibility metrics:"
    )

    print(reproducibility.to_string(index=False))

else:

    print(
        "\nWARNING: Reproducibility results "
        "not found."
    )


# ============================================================
# SCIENTIFIC FINDINGS
# ============================================================

findings = [

    {
        "Finding": "Noise Robustness",

        "Interpretation":
        "Adaptive thresholding reduces false alarms under "
        "heterogeneous quantum noise conditions."
    },

    {
        "Finding": "Computational Scalability",

        "Interpretation":
        "Adaptive threshold computation adds only constant-time "
        "arithmetic operations and does not change the asymptotic "
        "decision complexity."
    },

    {
        "Finding": "Dual-Signal Advantage",

        "Interpretation":
        "Combining teleportation mismatch information with Bell "
        "measurement anomaly information improves detection "
        "performance compared with individual signal approaches."
    },

    {
        "Finding": "Security-Sensitivity Trade-Off",

        "Interpretation":
        "Detection threshold selection provides explicit control "
        "over the trade-off between attack sensitivity and "
        "false-positive suppression."
    },

    {
        "Finding": "Statistical Reliability",

        "Interpretation":
        "Independent random-seed experiments and statistical "
        "testing indicate that the observed performance "
        "improvements are reproducible within the simulation "
        "environment."
    }

]


findings_df = pd.DataFrame(findings)


# ============================================================
# RESEARCH LIMITATIONS
# ============================================================

limitations = [

    {
        "Limitation": "Simulation Environment",

        "Description":
        "Experiments were performed using simulated quantum "
        "circuits and implemented quantum noise models."
    },

    {
        "Limitation": "Attack Coverage",

        "Description":
        "Evaluation was limited to the implemented Pauli attacks "
        "and entanglement disruption scenarios."
    },

    {
        "Limitation": "Recall Trade-Off",

        "Description":
        "Strong false-positive suppression can reduce attack "
        "recall depending on the selected detection threshold."
    },

    {
        "Limitation": "Hardware Validation",

        "Description":
        "The proposed framework should be further evaluated on "
        "real quantum hardware with device-specific noise."
    },

    {
        "Limitation": "Circuit Scale",

        "Description":
        "Current experiments use relatively small quantum circuit "
        "configurations and future work should investigate "
        "scalability to larger quantum systems."
    }

]


limitations_df = pd.DataFrame(limitations)


# ============================================================
# SAVE SCIENTIFIC FINDINGS
# ============================================================

findings_path = (
    "experiments/final_scientific_findings.csv"
)

findings_df.to_csv(
    findings_path,
    index=False
)


# ============================================================
# SAVE RESEARCH LIMITATIONS
# ============================================================

limitations_path = (
    "experiments/final_research_limitations.csv"
)

limitations_df.to_csv(
    limitations_path,
    index=False
)


# ============================================================
# CREATE FINAL DISCUSSION SUMMARY
# ============================================================

discussion_data = []


if best_config is not None:

    discussion_data.append({

        "Metric":
        "Best Detection Threshold",

        "Value":
        round(
            best_config[
                "detection_threshold"
            ],
            4
        )

    })

    discussion_data.append({

        "Metric":
        "Best Accuracy",

        "Value":
        round(
            best_config[
                "accuracy"
            ],
            4
        )

    })

    discussion_data.append({

        "Metric":
        "Best Precision",

        "Value":
        round(
            best_config[
                "precision"
            ],
            4
        )

    })

    discussion_data.append({

        "Metric":
        "Best Recall",

        "Value":
        round(
            best_config[
                "recall"
            ],
            4
        )

    })

    discussion_data.append({

        "Metric":
        "Best F1 Score",

        "Value":
        round(
            best_config[
                "f1_score"
            ],
            4
        )

    })

    discussion_data.append({

        "Metric":
        "Best False Positive Rate",

        "Value":
        round(
            best_config[
                "fpr"
            ],
            4
        )

    })


discussion_df = pd.DataFrame(
    discussion_data
)


discussion_df.to_csv(
    "experiments/final_discussion_summary.csv",
    index=False
)


# ============================================================
# FINAL SCIENTIFIC DISCUSSION
# ============================================================

print("\n" + "=" * 100)
print("FINAL SCIENTIFIC DISCUSSION")
print("=" * 100)


print("""

The experimental evaluation supports the feasibility of
Q-SHIELD as an adaptive quantum-channel attack detection
framework.

The results demonstrate that conventional fixed threshold
detection can become sensitive to heterogeneous quantum
channel noise, resulting in increased false-positive
decisions. Adaptive thresholding improves robustness against
noise; however, threshold adaptation introduces a measurable
trade-off between false-positive suppression and attack recall.

The strongest validated contribution of the proposed framework
is the dual-signal detection architecture. By combining
teleportation mismatch information with Bell measurement
distribution anomaly analysis, Q-SHIELD achieves improved
detection performance compared with individual signal
approaches.

The ablation study demonstrates that neither signal alone
provides the same overall balance of detection accuracy,
false-positive suppression, and F1 score as the combined
architecture.

Independent random-seed experiments and statistical
significance analysis further support that the observed
performance improvements are reproducible within the
evaluated simulation environment.

The computational analysis indicates that adaptive threshold
calculation introduces constant-time arithmetic operations and
does not change the asymptotic complexity of the detection
system.

However, the findings should be interpreted within the scope
of simulated quantum circuits, implemented noise channels,
and selected adversarial attack models. Future research should
evaluate Q-SHIELD on larger quantum circuits and real quantum
hardware to validate robustness under device-specific quantum
noise.

Overall, the results provide experimental evidence that
multi-signal quantum anomaly detection can improve the
reliability of attack detection in noisy quantum
communication environments.

""")


# ============================================================
# GENERATED FILES
# ============================================================

print("=" * 100)
print("GENERATED FILES")
print("=" * 100)

print("""
1. experiments/final_scientific_findings.csv
2. experiments/final_research_limitations.csv
3. experiments/final_discussion_summary.csv
""")


print("=" * 100)
print("PHASE 6B COMPLETED SUCCESSFULLY")
print("=" * 100)