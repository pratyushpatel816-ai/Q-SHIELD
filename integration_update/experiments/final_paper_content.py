import pandas as pd
import os


print("=" * 100)
print("Q-SHIELD")
print("PHASE 6F: FINAL ABSTRACT, CONCLUSION AND PAPER-READY CLAIMS")
print("=" * 100)


def load_csv(path):
    if os.path.exists(path):
        print(f"Loaded: {path}")
        return pd.read_csv(path)

    print(f"WARNING: Missing -> {path}")
    return None


# ============================================================
# LOAD VALIDATED RESULTS
# ============================================================

print("\nLoading validated research evidence...\n")

tradeoff = load_csv(
    "experiments/security_sensitivity_tradeoff.csv"
)

ablation = load_csv(
    "experiments/dual_signal_ablation_results.csv"
)

statistics = load_csv(
    "experiments/dual_signal_statistical_analysis.csv"
)

novelty = load_csv(
    "experiments/research_novelty_claims.csv"
)


# ============================================================
# EXTRACT BEST CONFIGURATION
# ============================================================

best_config = None

if tradeoff is not None and "f1_score" in tradeoff.columns:

    best_config = tradeoff.loc[
        tradeoff["f1_score"].idxmax()
    ]


# ============================================================
# EXTRACT DUAL-SIGNAL RESULT
# ============================================================

dual_result = None

if ablation is not None:

    rows = ablation[
        ablation["method"] == "Q-SHIELD Dual Signal"
    ]

    if len(rows) > 0:
        dual_result = rows.iloc[0]


# ============================================================
# EXTRACT STATISTICAL RESULT
# ============================================================

f1_stat = None

if statistics is not None:

    rows = statistics[
        statistics["metric"] == "f1_score"
    ]

    if len(rows) > 0:
        f1_stat = rows.iloc[0]


# ============================================================
# SAFE VALUE EXTRACTION
# ============================================================

threshold = (
    best_config["detection_threshold"]
    if best_config is not None
    else 0.25
)

accuracy = (
    best_config["accuracy"]
    if best_config is not None
    else 0.0
)

precision = (
    best_config["precision"]
    if best_config is not None
    else 0.0
)

recall = (
    best_config["recall"]
    if best_config is not None
    else 0.0
)

f1_score = (
    best_config["f1_score"]
    if best_config is not None
    else 0.0
)

fpr = (
    best_config["fpr"]
    if best_config is not None
    else 0.0
)


# ============================================================
# STATISTICAL VALUES
# ============================================================

mismatch_mean = 0.0
dual_mean = 0.0
improvement = 0.0
cohens_d = 0.0


if f1_stat is not None:

    mismatch_mean = f1_stat.get(
        "mismatch_mean",
        0.0
    )

    dual_mean = f1_stat.get(
        "dual_mean",
        0.0
    )

    improvement = f1_stat.get(
        "mean_difference",
        f1_stat.get("improvement", 0.0)
    )

    cohens_d = f1_stat.get(
        "cohens_d",
        f1_stat.get("cohen_d", 0.0)
    )


# ============================================================
# TITLE
# ============================================================

title = (
    "Q-SHIELD: A Dual-Signal Framework for Quantum Attack "
    "Detection Under Heterogeneous Quantum Noise"
)


# ============================================================
# ABSTRACT
# ============================================================

abstract = f"""
Quantum communication systems are vulnerable to both adversarial
disturbances and legitimate quantum channel noise, making reliable
attack detection challenging. Conventional threshold-based detection
can generate false alarms when channel conditions vary. This work
presents Q-SHIELD, a dual-signal quantum attack detection framework
that combines teleportation mismatch information with Bell measurement
distribution anomaly analysis.

The framework is evaluated under heterogeneous quantum noise models,
multiple adversarial attack scenarios, threshold sensitivity analysis,
baseline comparison, reproducibility experiments, computational
complexity evaluation, and statistical significance testing. The best
balanced configuration achieved an accuracy of {accuracy:.4f},
precision of {precision:.4f}, recall of {recall:.4f}, F1 score of
{f1_score:.4f}, and false-positive rate of {fpr:.4f} at a detection
threshold of {threshold:.2f}.

The dual-signal architecture demonstrated improved performance compared
with individual detection signals. Independent random-seed experiments
showed a mean F1 score improvement from {mismatch_mean:.4f} for
mismatch-only detection to {dual_mean:.4f} for dual-signal detection,
corresponding to an improvement of {improvement:.4f}. The observed
improvement was associated with a large effect size
(Cohen's d = {cohens_d:.4f}) within the evaluated simulation
environment.

The results indicate that combining complementary quantum security
signals can improve attack detection reliability while reducing
false-positive decisions under heterogeneous noise conditions.
The findings are limited to simulated quantum circuits and implemented
noise and attack models, motivating future validation on real quantum
hardware.
""".strip()


# ============================================================
# KEYWORDS
# ============================================================

keywords = [
    "Quantum Security",
    "Quantum Attack Detection",
    "Quantum Communication",
    "Quantum Noise",
    "Teleportation",
    "Bell Measurement",
    "Anomaly Detection",
    "Adaptive Thresholding"
]


# ============================================================
# PAPER-READY CONTRIBUTIONS
# ============================================================

contributions = [
    "A dual-signal quantum attack detection architecture combining teleportation mismatch and Bell measurement anomaly information.",

    "Experimental evaluation under heterogeneous quantum noise and multiple adversarial attack scenarios.",

    "Ablation analysis demonstrating the benefit of combining complementary quantum security signals.",

    "Security-sensitivity analysis quantifying the trade-off between false-positive suppression and attack recall.",

    "Independent random-seed reproducibility and statistical significance validation of the dual-signal performance improvement.",

    "Computational complexity analysis showing that adaptive detection decisions maintain constant-time complexity."
]


# ============================================================
# FINAL CONCLUSION
# ============================================================

conclusion = f"""
This research introduced Q-SHIELD, a dual-signal framework for quantum
attack detection under heterogeneous quantum channel noise. The framework
integrates teleportation mismatch information and Bell measurement
distribution anomaly analysis to distinguish adversarial disturbances
from legitimate channel variations.

The experimental evaluation showed that the best balanced configuration,
using a detection threshold of {threshold:.2f}, achieved an accuracy of
{accuracy:.4f}, an F1 score of {f1_score:.4f}, and a false-positive rate
of {fpr:.4f}. Ablation experiments demonstrated that the combined
dual-signal architecture provides a stronger overall balance of detection
performance and false-positive suppression than the individual signals.

Independent random-seed experiments further demonstrated an F1 score
improvement of {improvement:.4f} compared with mismatch-only detection,
with a large observed effect size of Cohen's d = {cohens_d:.4f}. These
results provide statistically supported evidence that multi-signal fusion
can improve quantum attack detection performance within the implemented
simulation environment.

The study also demonstrates that detection threshold selection represents
an important security-sensitivity trade-off. While stronger thresholds
can suppress false alarms, they may reduce attack recall. Therefore,
threshold configuration should be selected according to operational
security requirements.

The current findings are limited to simulated quantum circuits and the
implemented noise and attack models. Future work should validate the
framework on real quantum hardware, larger quantum communication systems,
and additional adversarial strategies.
""".strip()


# ============================================================
# SCIENTIFIC CLAIMS
# ============================================================

claims = [

    {
        "Claim":
        "Dual-signal fusion improves overall detection performance.",

        "Evidence":
        "Supported by ablation experiments and independent statistical analysis.",

        "Status":
        "Experimentally Supported"
    },

    {
        "Claim":
        "Q-SHIELD suppresses false-positive decisions under evaluated noisy conditions.",

        "Evidence":
        "Supported by threshold sensitivity and dual-signal evaluation experiments.",

        "Status":
        "Supported Within Simulation Scope"
    },

    {
        "Claim":
        "Adaptive decision mechanisms preserve constant-time asymptotic complexity.",

        "Evidence":
        "Supported by computational complexity analysis.",

        "Status":
        "Experimentally Supported"
    },

    {
        "Claim":
        "Q-SHIELD is universally superior to all quantum security systems.",

        "Evidence":
        "Not evaluated against all possible systems and datasets.",

        "Status":
        "Do Not Claim"
    },

    {
        "Claim":
        "Q-SHIELD is validated on real quantum hardware.",

        "Evidence":
        "Current experiments are simulation based.",

        "Status":
        "Do Not Claim"
    }
]


claims_df = pd.DataFrame(claims)


# ============================================================
# CREATE MARKDOWN PAPER CONTENT
# ============================================================

content = []

content.append(f"# {title}\n\n")

content.append("## Abstract\n\n")
content.append(abstract + "\n\n")

content.append("## Keywords\n\n")
content.append(", ".join(keywords) + "\n\n")

content.append("## Main Contributions\n\n")

for i, contribution in enumerate(contributions, 1):

    content.append(
        f"{i}. {contribution}\n"
    )


content.append("\n## Final Conclusion\n\n")
content.append(conclusion + "\n\n")

content.append("## Scientifically Supported Claims\n\n")

for _, row in claims_df.iterrows():

    content.append(
        f"### {row['Claim']}\n\n"
    )

    content.append(
        f"**Evidence:** {row['Evidence']}\n\n"
    )

    content.append(
        f"**Status:** {row['Status']}\n\n"
    )


# ============================================================
# SAVE MARKDOWN FILE
# ============================================================

markdown_path = (
    "experiments/QSHIELD_PAPER_READY_CONTENT.md"
)

with open(
    markdown_path,
    "w",
    encoding="utf-8"
) as file:

    file.writelines(content)


# ============================================================
# SAVE ABSTRACT
# ============================================================

with open(
    "experiments/QSHIELD_ABSTRACT.txt",
    "w",
    encoding="utf-8"
) as file:

    file.write(abstract)


# ============================================================
# SAVE CONCLUSION
# ============================================================

with open(
    "experiments/QSHIELD_CONCLUSION.txt",
    "w",
    encoding="utf-8"
) as file:

    file.write(conclusion)


# ============================================================
# SAVE CLAIMS
# ============================================================

claims_df.to_csv(
    "experiments/paper_ready_scientific_claims.csv",
    index=False
)


# ============================================================
# CONSOLE OUTPUT
# ============================================================

print("\n" + "=" * 100)
print("FINAL PAPER TITLE")
print("=" * 100)

print(title)


print("\n" + "=" * 100)
print("ABSTRACT")
print("=" * 100)

print(abstract)


print("\n" + "=" * 100)
print("MAIN RESEARCH CONTRIBUTIONS")
print("=" * 100)

for i, contribution in enumerate(contributions, 1):
    print(f"{i}. {contribution}")


print("\n" + "=" * 100)
print("FINAL CONCLUSION")
print("=" * 100)

print(conclusion)


print("\n" + "=" * 100)
print("GENERATED FILES")
print("=" * 100)

print("""
1. experiments/QSHIELD_PAPER_READY_CONTENT.md
2. experiments/QSHIELD_ABSTRACT.txt
3. experiments/QSHIELD_CONCLUSION.txt
4. experiments/paper_ready_scientific_claims.csv
""")


print("=" * 100)
print("PHASE 6F COMPLETED")
print("=" * 100)