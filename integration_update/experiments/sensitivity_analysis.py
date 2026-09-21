import os
import random
import numpy as np
import pandas as pd

from qshield.quantum.teleportation import TeleportationEngine
from qshield.detection.detector import FixedThresholdDetector
from qshield.detection.adaptive_detector import BlindAdaptiveDetector


# ============================================================
# Q-SHIELD
# PHASE 5E: PARAMETER SENSITIVITY ANALYSIS
# ============================================================

SHOTS = 1024
TRIALS_PER_SCENARIO = 10

BASE_THRESHOLDS = [
    0.18,
    0.22,
    0.26,
    0.30,
    0.34
]

ADAPTATION_FACTORS = [
    0.1,
    0.2,
    0.4,
    0.6,
    0.8
]

NORMAL_SCENARIOS = [
    ("bit_flip", 0.05),
    ("bit_flip", 0.10),
    ("bit_flip", 0.15),
    ("phase_flip", 0.05),
    ("phase_flip", 0.10),
    ("phase_flip", 0.15),
    ("bit_phase_flip", 0.05),
    ("bit_phase_flip", 0.10),
    ("bit_phase_flip", 0.15),
    ("depolarizing", 0.05),
    ("depolarizing", 0.10),
    ("depolarizing", 0.15),
    ("readout", 0.05),
    ("readout", 0.10),
    ("readout", 0.15)
]

ATTACK_SCENARIOS = [
    ("pauli_x", "bit_flip", 0.05),
    ("pauli_y", "bit_flip", 0.05),
    ("pauli_z", "phase_flip", 0.05),
    ("entanglement_disruption", "depolarizing", 0.05),

    ("pauli_x", "bit_flip", 0.10),
    ("pauli_y", "phase_flip", 0.10),
    ("pauli_z", "depolarizing", 0.10),
    ("entanglement_disruption", "readout", 0.10)
]


# ============================================================
# METRIC CALCULATION
# ============================================================

def calculate_metrics(tp, fp, tn, fn):

    accuracy = (tp + tn) / max(tp + fp + tn + fn, 1)

    precision = tp / max(tp + fp, 1)

    recall = tp / max(tp + fn, 1)

    f1_score = (
        2 * precision * recall /
        max(precision + recall, 1e-10)
    )

    fpr = fp / max(fp + tn, 1)

    fnr = fn / max(fn + tp, 1)

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
        "fpr": fpr,
        "fnr": fnr
    }


# ============================================================
# MAIN EXPERIMENT
# ============================================================

def run_sensitivity_analysis():

    print("=" * 100)
    print("Q-SHIELD")
    print("PHASE 5E: PARAMETER SENSITIVITY ANALYSIS")
    print("=" * 100)

    print(f"\nQuantum Shots: {SHOTS}")
    print(f"Trials per Scenario: {TRIALS_PER_SCENARIO}")

    print("\nBase Threshold Values:")
    print(BASE_THRESHOLDS)

    print("\nAdaptation Factor Values:")
    print(ADAPTATION_FACTORS)

    print("\nTotal Parameter Configurations:")
    print(len(BASE_THRESHOLDS) * len(ADAPTATION_FACTORS))

    engine = TeleportationEngine(shots=SHOTS)

    results = []

    print("\n" + "-" * 100)
    print("RUNNING PARAMETER GRID EVALUATION")
    print("-" * 100)

    # --------------------------------------------------------
    # PARAMETER GRID
    # --------------------------------------------------------

    for base_threshold in BASE_THRESHOLDS:

        for adaptation_factor in ADAPTATION_FACTORS:

            print(
                f"\nTesting "
                f"Base Threshold={base_threshold:.2f} | "
                f"Adaptation Factor={adaptation_factor:.2f}"
            )

            tp = 0
            fp = 0
            tn = 0
            fn = 0

            # ====================================================
            # CREATE ADAPTIVE DETECTOR
            # ====================================================

            adaptive_detector = BlindAdaptiveDetector(
                base_threshold=base_threshold,
                adaptation_factor=adaptation_factor
            )

            # ====================================================
            # NORMAL CHANNEL TESTING
            # ====================================================

            for noise_type, noise_probability in NORMAL_SCENARIOS:

                for trial in range(TRIALS_PER_SCENARIO):

                    bit = random.choice([0, 1])
                    basis = random.choice(["X", "Y", "Z"])

                    result = engine.run(
                        bit=bit,
                        basis=basis,
                        noise_type=noise_type,
                        noise_probability=noise_probability,
                        attack_type="none"
                    )

                    mismatch_rate = result["mismatch_rate"]

                    detection_result = adaptive_detector.detect(
                        mismatch_rate
                    )

                    if detection_result:
                        fp += 1
                    else:
                        tn += 1

            # ====================================================
            # ATTACK CHANNEL TESTING
            # ====================================================

            for (
                attack_type,
                noise_type,
                noise_probability
            ) in ATTACK_SCENARIOS:

                for trial in range(TRIALS_PER_SCENARIO):

                    bit = random.choice([0, 1])
                    basis = random.choice(["X", "Y", "Z"])

                    result = engine.run(
                        bit=bit,
                        basis=basis,
                        noise_type=noise_type,
                        noise_probability=noise_probability,
                        attack_type=attack_type
                    )

                    mismatch_rate = result["mismatch_rate"]

                    detection_result = adaptive_detector.detect(
                        mismatch_rate
                    )

                    if detection_result:
                        tp += 1
                    else:
                        fn += 1

            # ====================================================
            # CALCULATE PERFORMANCE
            # ====================================================

            metrics = calculate_metrics(
                tp,
                fp,
                tn,
                fn
            )

            print(
                f"Accuracy={metrics['accuracy']:.4f} | "
                f"Precision={metrics['precision']:.4f} | "
                f"Recall={metrics['recall']:.4f} | "
                f"F1={metrics['f1_score']:.4f} | "
                f"FPR={metrics['fpr']:.4f}"
            )

            results.append({
                "base_threshold": base_threshold,
                "adaptation_factor": adaptation_factor,
                "accuracy": metrics["accuracy"],
                "precision": metrics["precision"],
                "recall": metrics["recall"],
                "f1_score": metrics["f1_score"],
                "fpr": metrics["fpr"],
                "fnr": metrics["fnr"],
                "tp": tp,
                "fp": fp,
                "tn": tn,
                "fn": fn
            })

    # ============================================================
    # SAVE RESULTS
    # ============================================================

    df = pd.DataFrame(results)

    output_file = (
        "experiments/"
        "sensitivity_analysis_results.csv"
    )

    df.to_csv(
        output_file,
        index=False
    )

    # ============================================================
    # DISPLAY RESULTS
    # ============================================================

    print("\n" + "=" * 100)
    print("PARAMETER SENSITIVITY RESULTS")
    print("=" * 100)

    print(
        "\n"
        + df[
            [
                "base_threshold",
                "adaptation_factor",
                "accuracy",
                "precision",
                "recall",
                "f1_score",
                "fpr"
            ]
        ].to_string(index=False)
    )

    # ============================================================
    # BEST CONFIGURATION
    # ============================================================

    best_config = df.loc[
        df["f1_score"].idxmax()
    ]

    print("\n" + "=" * 100)
    print("BEST PARAMETER CONFIGURATION")
    print("=" * 100)

    print(
        f"\nBase Threshold: "
        f"{best_config['base_threshold']:.2f}"
    )

    print(
        f"Adaptation Factor: "
        f"{best_config['adaptation_factor']:.2f}"
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
        f"False Positive Rate: "
        f"{best_config['fpr']:.4f}"
    )

    print("\nResults saved to:")
    print(output_file)

    print("\n" + "=" * 100)
    print("PHASE 5E COMPLETED")
    print("=" * 100)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    run_sensitivity_analysis()