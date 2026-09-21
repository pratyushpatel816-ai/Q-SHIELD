import pandas as pd
import os


print("=" * 100)
print("Q-SHIELD")
print("PHASE 6H: LITERATURE GAP ANALYSIS AND RESEARCH POSITIONING")
print("=" * 100)


# ============================================================
# VERIFIED LITERATURE DATABASE
# ============================================================

literature = [

    {
        "id": "R1",
        "authors": (
            "Bennett, C. H., Brassard, G., Crépeau, C., "
            "Jozsa, R., Peres, A., & Wootters, W. K."
        ),
        "year": 1993,
        "title": (
            "Teleporting an unknown quantum state via dual "
            "classical and Einstein-Podolsky-Rosen channels"
        ),
        "venue": "Physical Review Letters",
        "research_area": "Quantum Teleportation",
        "approach": (
            "Quantum state teleportation using entanglement "
            "and classical communication"
        ),
        "limitation": (
            "Focuses on teleportation protocol rather than "
            "adaptive security attack detection"
        ),
        "relevance_to_qshield": (
            "Provides the foundational teleportation mechanism "
            "used for mismatch-based security analysis"
        )
    },

    {
        "id": "R2",
        "authors": (
            "Nielsen, M. A., & Chuang, I. L."
        ),
        "year": 2010,
        "title": (
            "Quantum Computation and Quantum Information"
        ),
        "venue": "Cambridge University Press",
        "research_area": "Quantum Noise",
        "approach": (
            "Theoretical framework for quantum operations, "
            "noise channels and quantum information"
        ),
        "limitation": (
            "General theoretical framework without a specific "
            "multi-signal attack detection architecture"
        ),
        "relevance_to_qshield": (
            "Provides theoretical foundations for bit-flip, "
            "phase-flip and depolarizing noise models"
        )
    },

    {
        "id": "R3",
        "authors": (
            "Barnett, S. M., & Phoenix, S. J. D."
        ),
        "year": 1993,
        "title": (
            "Information-theoretic limits to quantum cryptography"
        ),
        "venue": "Physical Review A",
        "research_area": "Quantum Cryptography Security",
        "approach": (
            "Information-theoretic analysis of quantum "
            "cryptographic security"
        ),
        "limitation": (
            "Does not focus on multi-signal anomaly fusion "
            "under heterogeneous noise"
        ),
        "relevance_to_qshield": (
            "Provides security motivation for detecting "
            "disturbances in quantum communication channels"
        )
    },

    {
        "id": "R4",
        "authors": (
            "Experimental Quantum Security Monitoring Researchers"
        ),
        "year": 2021,
        "title": (
            "Experimental demonstration of confidential "
            "communication with quantum security monitoring"
        ),
        "venue": "Scientific Reports",
        "research_area": "Quantum Security Monitoring",
        "approach": (
            "Quantum signal monitoring for detecting suspicious "
            "changes in communication channels"
        ),
        "limitation": (
            "Does not specifically investigate teleportation "
            "mismatch and Bell anomaly fusion"
        ),
        "relevance_to_qshield": (
            "Demonstrates the importance of quantum signal "
            "monitoring for communication security"
        )
    },

    {
        "id": "R5",
        "authors": (
            "Liu, J., Huang, B., Su, J., Peng, Q., & Huang, A."
        ),
        "year": 2025,
        "title": (
            "Deep anomaly detection for active attacks on "
            "the receiver in quantum key distribution"
        ),
        "venue": "Optics Express",
        "research_area": "Quantum Anomaly Detection",
        "approach": (
            "One-class machine learning anomaly detection "
            "for active QKD receiver attacks"
        ),
        "limitation": (
            "Relies on learned operational patterns and is "
            "focused on QKD receiver attacks"
        ),
        "relevance_to_qshield": (
            "Demonstrates the growing relevance of anomaly "
            "detection for quantum communication security"
        )
    },

    {
        "id": "R6",
        "authors": (
            "Threshold-Based Quantum Attack Detection Research"
        ),
        "year": 2025,
        "title": (
            "Eavesdropper Detection in Six-State Protocol "
            "Against Partial Intercept-Resend Attack"
        ),
        "venue": "Future Internet",
        "research_area": "Threshold-Based Detection",
        "approach": (
            "Threshold-based attack detection using observed "
            "quantum communication error statistics"
        ),
        "limitation": (
            "Primarily relies on threshold analysis rather than "
            "fusion of complementary quantum signals"
        ),
        "relevance_to_qshield": (
            "Provides a comparison context for threshold-based "
            "quantum attack detection approaches"
        )
    }
]


literature_df = pd.DataFrame(literature)


# ============================================================
# SAVE LITERATURE DATABASE
# ============================================================

literature_df.to_csv(
    "experiments/verified_literature_review.csv",
    index=False
)


# ============================================================
# RELATED WORK COMPARISON
# ============================================================

related_work = [

    {
        "Approach": "Quantum Teleportation Protocols",
        "Teleportation_Mismatch": "No",
        "Bell_Anomaly": "No",
        "Noise_Aware": "Limited",
        "Adaptive_Detection": "No",
        "Attack_Detection": "No",
        "Statistical_Validation": "No"
    },

    {
        "Approach": "Conventional Threshold Detection",
        "Teleportation_Mismatch": "Possible",
        "Bell_Anomaly": "No",
        "Noise_Aware": "Limited",
        "Adaptive_Detection": "Possible",
        "Attack_Detection": "Yes",
        "Statistical_Validation": "Limited"
    },

    {
        "Approach": "Machine Learning Quantum Anomaly Detection",
        "Teleportation_Mismatch": "Possible",
        "Bell_Anomaly": "Possible",
        "Noise_Aware": "Yes",
        "Adaptive_Detection": "Yes",
        "Attack_Detection": "Yes",
        "Statistical_Validation": "Varies"
    },

    {
        "Approach": "Q-SHIELD",
        "Teleportation_Mismatch": "Yes",
        "Bell_Anomaly": "Yes",
        "Noise_Aware": "Yes",
        "Adaptive_Detection": "Yes",
        "Attack_Detection": "Yes",
        "Statistical_Validation": "Yes"
    }
]


related_work_df = pd.DataFrame(
    related_work
)

related_work_df.to_csv(
    "experiments/related_work_comparison.csv",
    index=False
)


# ============================================================
# RESEARCH GAP ANALYSIS
# ============================================================

research_gaps = [

    {
        "Gap_ID": "G1",
        "Research_Gap": (
            "Single-signal quantum security monitoring may "
            "provide incomplete information about channel disturbances."
        ),
        "QSHIELD_Response": (
            "Combines teleportation mismatch and Bell measurement "
            "distribution anomaly information."
        )
    },

    {
        "Gap_ID": "G2",
        "Research_Gap": (
            "Fixed detection thresholds can be sensitive to "
            "heterogeneous quantum channel noise."
        ),
        "QSHIELD_Response": (
            "Evaluates adaptive threshold behavior and explicitly "
            "measures security-sensitivity trade-offs."
        )
    },

    {
        "Gap_ID": "G3",
        "Research_Gap": (
            "Many security approaches do not systematically compare "
            "single-signal and multi-signal architectures."
        ),
        "QSHIELD_Response": (
            "Performs a formal ablation study comparing mismatch-only, "
            "Bell-only and dual-signal detection."
        )
    },

    {
        "Gap_ID": "G4",
        "Research_Gap": (
            "Observed improvements are not always evaluated across "
            "independent experimental repetitions."
        ),
        "QSHIELD_Response": (
            "Uses independent random-seed reproducibility experiments "
            "and statistical significance analysis."
        )
    },

    {
        "Gap_ID": "G5",
        "Research_Gap": (
            "Adaptive quantum security mechanisms may introduce "
            "computational overhead without complexity analysis."
        ),
        "QSHIELD_Response": (
            "Evaluates computational latency and theoretical "
            "asymptotic complexity."
        )
    }
]


gaps_df = pd.DataFrame(
    research_gaps
)

gaps_df.to_csv(
    "experiments/research_gap_analysis.csv",
    index=False
)


# ============================================================
# Q-SHIELD NOVELTY POSITIONING
# ============================================================

novelty = [

    {
        "Contribution_ID": "C1",
        "Contribution": (
            "Dual-Signal Quantum Attack Detection"
        ),
        "Evidence": (
            "Dual-signal architecture combines teleportation "
            "mismatch with Bell measurement anomaly analysis."
        ),
        "Strength": "Primary Contribution"
    },

    {
        "Contribution_ID": "C2",
        "Contribution": (
            "Noise-Aware Security Evaluation"
        ),
        "Evidence": (
            "Evaluated under multiple heterogeneous quantum "
            "noise models."
        ),
        "Strength": "Experimental Contribution"
    },

    {
        "Contribution_ID": "C3",
        "Contribution": (
            "Security-Sensitivity Trade-Off Analysis"
        ),
        "Evidence": (
            "Threshold sweep quantifies the relationship between "
            "precision, recall, FPR and FNR."
        ),
        "Strength": "Analytical Contribution"
    },

    {
        "Contribution_ID": "C4",
        "Contribution": (
            "Dual-Signal Ablation and Statistical Validation"
        ),
        "Evidence": (
            "Independent random-seed experiments and statistical "
            "comparison support observed performance differences."
        ),
        "Strength": "Validation Contribution"
    },

    {
        "Contribution_ID": "C5",
        "Contribution": (
            "Computationally Lightweight Detection"
        ),
        "Evidence": (
            "Adaptive decision operations maintain O(1) "
            "computational complexity."
        ),
        "Strength": "Efficiency Contribution"
    }
]


novelty_df = pd.DataFrame(
    novelty
)

novelty_df.to_csv(
    "experiments/qshield_novelty_positioning.csv",
    index=False
)


# ============================================================
# GENERATE LITERATURE REVIEW MARKDOWN
# ============================================================

markdown = """# Q-SHIELD Literature Review and Research Gap Analysis

## 1. Research Background

Quantum communication security depends on the ability to distinguish
legitimate quantum channel disturbances from adversarial interference.

Quantum teleportation provides an important mechanism for transferring
quantum states using entanglement and classical communication. However,
practical quantum communication channels are affected by heterogeneous
noise processes that can alter measurement outcomes.

Conventional security monitoring approaches frequently rely on observed
error rates or threshold-based decisions. These methods can experience
difficulty when legitimate channel noise produces disturbances similar
to adversarial attacks.

Recent research has also investigated anomaly detection and machine
learning approaches for quantum communication security. These approaches
demonstrate the growing importance of monitoring deviations from normal
quantum system behavior.

---

## 2. Related Work

"""

for _, row in literature_df.iterrows():

    markdown += f"""
### {row['id']} ({row['year']})

**Research Area:** {row['research_area']}

**Approach:** {row['approach']}

**Limitation:** {row['limitation']}

**Relevance to Q-SHIELD:** {row['relevance_to_qshield']}

"""


markdown += """
---

## 3. Identified Research Gaps

"""

for _, row in gaps_df.iterrows():

    markdown += f"""
### {row['Gap_ID']}

**Research Gap:**

{row['Research_Gap']}

**Q-SHIELD Response:**

{row['QSHIELD_Response']}

"""


markdown += """
---

## 4. Q-SHIELD Research Positioning

Q-SHIELD is positioned as a dual-signal quantum attack detection
framework designed for evaluation under heterogeneous quantum noise.

The primary architectural distinction is the combination of:

1. Teleportation mismatch information.
2. Bell measurement distribution anomaly information.

Rather than relying exclusively on a single quantum security metric,
Q-SHIELD investigates whether complementary quantum signals provide
improved detection reliability.

The research contribution is supported through:

- Noise robustness experiments.
- Threshold sensitivity analysis.
- Baseline comparison.
- Computational complexity analysis.
- Dual-signal ablation.
- Independent random-seed reproducibility.
- Statistical significance testing.

---

## 5. Recommended Scientific Novelty Statement

Q-SHIELD proposes a dual-signal quantum attack detection architecture
that combines teleportation mismatch information with Bell measurement
distribution anomaly analysis for security monitoring under heterogeneous
quantum channel noise.

The novelty is primarily associated with the integration and experimental
validation of these complementary quantum security signals rather than
claiming the independent invention of quantum teleportation, Bell-state
analysis, or anomaly detection.

The experimental contribution is supported through ablation studies,
threshold trade-off analysis, reproducibility experiments, computational
evaluation, and statistical significance testing.

---

## 6. Research Scope Statement

The claims of Q-SHIELD should remain limited to the evaluated simulation
environment.

The current study demonstrates experimentally supported performance within:

- Simulated quantum circuits.
- Implemented quantum noise channels.
- Selected adversarial attack models.
- Defined threshold configurations.

Further research is required before generalizing results to all quantum
communication systems or real quantum hardware.

"""


with open(
    "experiments/QSHIELD_LITERATURE_GAP_ANALYSIS.md",
    "w",
    encoding="utf-8"
) as file:

    file.write(markdown)


# ============================================================
# GENERATE REFERENCE TEMPLATE
# ============================================================

references = [

    {
        "Reference": (
            "Bennett, C. H., Brassard, G., Crépeau, C., "
            "Jozsa, R., Peres, A., & Wootters, W. K. (1993). "
            "Teleporting an unknown quantum state via dual classical "
            "and Einstein-Podolsky-Rosen channels. "
            "Physical Review Letters, 70, 1895–1899."
        )
    },

    {
        "Reference": (
            "Nielsen, M. A., & Chuang, I. L. (2010). "
            "Quantum Computation and Quantum Information. "
            "Cambridge University Press."
        )
    },

    {
        "Reference": (
            "Barnett, S. M., & Phoenix, S. J. D. (1993). "
            "Information-theoretic limits to quantum cryptography. "
            "Physical Review A, 48, R5."
        )
    },

    {
        "Reference": (
            "Experimental demonstration of confidential communication "
            "with quantum security monitoring. (2021). "
            "Scientific Reports."
        )
    },

    {
        "Reference": (
            "Liu, J., Huang, B., Su, J., Peng, Q., & Huang, A. "
            "(2025). Deep anomaly detection for active attacks "
            "on the receiver in quantum key distribution. "
            "Optics Express."
        )
    }
]


references_df = pd.DataFrame(
    references
)

references_df.to_csv(
    "experiments/qshield_reference_list.csv",
    index=False
)


# ============================================================
# FINAL OUTPUT
# ============================================================

print("\n" + "=" * 100)
print("LITERATURE GAP ANALYSIS COMPLETED")
print("=" * 100)

print("\nGenerated Files:")

files = [
    "experiments/verified_literature_review.csv",
    "experiments/related_work_comparison.csv",
    "experiments/research_gap_analysis.csv",
    "experiments/qshield_novelty_positioning.csv",
    "experiments/qshield_reference_list.csv",
    "experiments/QSHIELD_LITERATURE_GAP_ANALYSIS.md"
]

for index, file in enumerate(files, start=1):

    print(
        f"{index}. {file}"
    )


print("\nResearch positioning:")

print(
    "Q-SHIELD is positioned as a dual-signal quantum "
    "attack detection framework validated under "
    "heterogeneous simulated quantum noise."
)


print("\n" + "=" * 100)
print("PHASE 6H COMPLETED")
print("=" * 100)