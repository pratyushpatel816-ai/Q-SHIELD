"""
Q-SHIELD
PHASE 5C: COMPARATIVE BASELINE ANALYSIS

Compares:
1. Fixed Threshold
2. Statistical Threshold
3. Percentile Threshold
4. Q-SHIELD Blind Adaptive Threshold

All methods are evaluated under identical
heterogeneous quantum noise and attack conditions.
"""

import os
import sys
import random
import numpy as np
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

from qshield.quantum.teleportation import TeleportationEngine


# ============================================================
# CONFIGURATION
# ============================================================

SHOTS = 1024
TRIALS_PER_SCENARIO = 20

FIXED_THRESHOLD = 0.26

# Statistical baseline parameter
STATISTICAL_K = 2.0

# Percentile baseline
PERCENTILE_VALUE = 95

# Q-SHIELD adaptive parameters
BASE_THRESHOLD = 0.26
ADAPTATION_FACTOR = 0.4

RANDOM_SEED = 42

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def calculate_metrics(y_true, y_pred):

    accuracy = accuracy_score(y_true, y_pred)

    precision = precision_score(
        y_true,
        y_pred,
        zero_division=0
    )

    recall = recall_score(
        y_true,
        y_pred,
        zero_division=0
    )

    f1 = f1_score(
        y_true,
        y_pred,
        zero_division=0
    )

    tn, fp, fn, tp = confusion_matrix(
        y_true,
        y_pred,
        labels=[0, 1]
    ).ravel()

    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    fnr = fn / (fn + tp) if (fn + tp) > 0 else 0.0

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "fpr": fpr,
        "fnr": fnr,
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn
    }


def get_probe_result(
    engine,
    noise_type,
    noise_probability,
    attack_type="none"
):
    """
    Run all six Pauli probe states and
    return mean mismatch rate.
    """

    probes = [
        (0, "X"),
        (1, "X"),
        (0, "Y"),
        (1, "Y"),
        (0, "Z"),
        (1, "Z")
    ]

    mismatch_rates = []

    for bit, basis in probes:

        result = engine.run(
            bit=bit,
            basis=basis,
            noise_type=noise_type,
            noise_probability=noise_probability,
            attack_type=attack_type
        )

        mismatch_rates.append(
            result["mismatch_rate"]
        )

    return float(np.mean(mismatch_rates))


# ============================================================
# CALIBRATION DATA
# ============================================================

def collect_calibration_data(engine):

    print("\n" + "=" * 100)
    print("CALIBRATION PHASE")
    print("=" * 100)

    calibration_noise_types = [
        "bit_flip",
        "phase_flip",
        "bit_phase_flip",
        "depolarizing",
        "readout"
    ]

    calibration_noise_levels = [
        0.00,
        0.02,
        0.05,
        0.08,
        0.10
    ]

    calibration_values = []

    for noise_type in calibration_noise_types:

        for noise_probability in calibration_noise_levels:

            for _ in range(TRIALS_PER_SCENARIO):

                mismatch = get_probe_result(
                    engine=engine,
                    noise_type=noise_type,
                    noise_probability=noise_probability,
                    attack_type="none"
                )

                calibration_values.append(mismatch)

            print(
                f"Calibration | "
                f"{noise_type:<18} | "
                f"Noise={noise_probability:.2f}"
            )

    return np.array(calibration_values)


# ============================================================
# THRESHOLD METHODS
# ============================================================

def fixed_threshold():
    return FIXED_THRESHOLD


def statistical_threshold(calibration_data):

    mean_value = np.mean(calibration_data)
    std_value = np.std(calibration_data)

    threshold = (
        mean_value
        + STATISTICAL_K * std_value
    )

    return min(float(threshold), 1.0)


def percentile_threshold(calibration_data):

    threshold = np.percentile(
        calibration_data,
        PERCENTILE_VALUE
    )

    return float(threshold)


def estimate_noise_from_mismatch(mismatch):

    """
    Blind noise estimator.

    The estimator uses observed mismatch only,
    without access to true channel noise.
    """

    estimated_noise = min(
        mismatch * 2.0,
        0.50
    )

    return float(estimated_noise)


def blind_adaptive_threshold(mismatch):

    estimated_noise = estimate_noise_from_mismatch(
        mismatch
    )

    threshold = (
        BASE_THRESHOLD
        + ADAPTATION_FACTOR * estimated_noise
    )

    return min(float(threshold), 1.0)


# ============================================================
# EXPERIMENT SCENARIOS
# ============================================================

def create_scenarios():

    scenarios = []

    noise_types = [
        "bit_flip",
        "phase_flip",
        "bit_phase_flip",
        "depolarizing",
        "readout"
    ]

    noise_levels = [
        0.00,
        0.05,
        0.10,
        0.15,
        0.20
    ]

    # --------------------------------------------------------
    # NORMAL CHANNEL SCENARIOS
    # Label = 0
    # --------------------------------------------------------

    for noise_type in noise_types:

        for noise_probability in noise_levels:

            scenarios.append({
                "name":
                    f"{noise_type}_noise_{noise_probability:.2f}",

                "noise_type":
                    noise_type,

                "noise_probability":
                    noise_probability,

                "attack_type":
                    "none",

                "label":
                    0
            })

    # --------------------------------------------------------
    # ATTACK SCENARIOS
    # Label = 1
    # --------------------------------------------------------

    attack_types = [
        "pauli_x",
        "pauli_y",
        "pauli_z",
        "entanglement_disruption"
    ]

    for noise_type in noise_types:

        for attack_type in attack_types:

            scenarios.append({
                "name":
                    f"{noise_type}_{attack_type}",

                "noise_type":
                    noise_type,

                "noise_probability":
                    0.10,

                "attack_type":
                    attack_type,

                "label":
                    1
            })

    return scenarios


# ============================================================
# MAIN EXPERIMENT
# ============================================================

def main():

    print("\n" + "=" * 100)
    print("Q-SHIELD")
    print("PHASE 5C: COMPARATIVE BASELINE ANALYSIS")
    print("=" * 100)

    print(f"\nQuantum Shots: {SHOTS}")
    print(f"Trials per Scenario: {TRIALS_PER_SCENARIO}")
    print(f"Fixed Threshold: {FIXED_THRESHOLD}")

    print("\nMethods Compared:")
    print("1. Fixed Threshold")
    print("2. Statistical Threshold")
    print("3. Percentile Threshold")
    print("4. Q-SHIELD Blind Adaptive")

    # --------------------------------------------------------
    # CREATE ENGINE
    # --------------------------------------------------------

    engine = TeleportationEngine(
        shots=SHOTS
    )

    # --------------------------------------------------------
    # CALIBRATION
    # --------------------------------------------------------

    calibration_data = collect_calibration_data(
        engine
    )

    statistical_t = statistical_threshold(
        calibration_data
    )

    percentile_t = percentile_threshold(
        calibration_data
    )

    print("\n" + "-" * 100)
    print("CALIBRATED BASELINE THRESHOLDS")
    print("-" * 100)

    print(
        f"Calibration Samples: "
        f"{len(calibration_data)}"
    )

    print(
        f"Calibration Mean: "
        f"{np.mean(calibration_data):.4f}"
    )

    print(
        f"Calibration Std Dev: "
        f"{np.std(calibration_data):.4f}"
    )

    print(
        f"Statistical Threshold: "
        f"{statistical_t:.4f}"
    )

    print(
        f"Percentile Threshold: "
        f"{percentile_t:.4f}"
    )

    # --------------------------------------------------------
    # METHODS
    # --------------------------------------------------------

    methods = [
        "Fixed",
        "Statistical",
        "Percentile",
        "Blind_Adaptive"
    ]

    predictions = {
        method: [] for method in methods
    }

    ground_truth = []

    detailed_results = []

    scenarios = create_scenarios()

    print("\n" + "=" * 100)
    print("RUNNING BASELINE COMPARISON")
    print("=" * 100)

    # --------------------------------------------------------
    # SCENARIO EVALUATION
    # --------------------------------------------------------

    for scenario in scenarios:

        scenario_name = scenario["name"]

        noise_type = scenario["noise_type"]

        noise_probability = (
            scenario["noise_probability"]
        )

        attack_type = scenario["attack_type"]

        label = scenario["label"]

        scenario_mismatches = []

        scenario_predictions = {
            method: []
            for method in methods
        }

        scenario_thresholds = {
            method: []
            for method in methods
        }

        for trial in range(TRIALS_PER_SCENARIO):

            mismatch = get_probe_result(
                engine=engine,
                noise_type=noise_type,
                noise_probability=noise_probability,
                attack_type=attack_type
            )

            scenario_mismatches.append(
                mismatch
            )

            # Fixed
            fixed_t = fixed_threshold()

            fixed_prediction = int(
                mismatch > fixed_t
            )

            # Statistical
            statistical_prediction = int(
                mismatch > statistical_t
            )

            # Percentile
            percentile_prediction = int(
                mismatch > percentile_t
            )

            # Blind Adaptive
            adaptive_t = blind_adaptive_threshold(
                mismatch
            )

            adaptive_prediction = int(
                mismatch > adaptive_t
            )

            # Store predictions

            predictions["Fixed"].append(
                fixed_prediction
            )

            predictions["Statistical"].append(
                statistical_prediction
            )

            predictions["Percentile"].append(
                percentile_prediction
            )

            predictions["Blind_Adaptive"].append(
                adaptive_prediction
            )

            ground_truth.append(label)

            # Scenario-level storage

            scenario_predictions["Fixed"].append(
                fixed_prediction
            )

            scenario_predictions["Statistical"].append(
                statistical_prediction
            )

            scenario_predictions["Percentile"].append(
                percentile_prediction
            )

            scenario_predictions[
                "Blind_Adaptive"
            ].append(
                adaptive_prediction
            )

            scenario_thresholds["Fixed"].append(
                fixed_t
            )

            scenario_thresholds[
                "Statistical"
            ].append(
                statistical_t
            )

            scenario_thresholds[
                "Percentile"
            ].append(
                percentile_t
            )

            scenario_thresholds[
                "Blind_Adaptive"
            ].append(
                adaptive_t
            )

        # ----------------------------------------------------
        # SCENARIO SUMMARY
        # ----------------------------------------------------

        mean_mismatch = np.mean(
            scenario_mismatches
        )

        result_row = {
            "scenario": scenario_name,
            "noise_type": noise_type,
            "noise_probability": noise_probability,
            "attack_type": attack_type,
            "true_label": label,
            "mean_mismatch": mean_mismatch
        }

        for method in methods:

            rejection_rate = np.mean(
                scenario_predictions[method]
            )

            mean_threshold = np.mean(
                scenario_thresholds[method]
            )

            result_row[
                f"{method}_threshold"
            ] = mean_threshold

            result_row[
                f"{method}_rejection_rate"
            ] = rejection_rate

        detailed_results.append(
            result_row
        )

        print(
            f"{scenario_name:<45} | "
            f"Mismatch={mean_mismatch:.4f} | "
            f"Fixed={np.mean(scenario_predictions['Fixed']):.2f} | "
            f"Stat={np.mean(scenario_predictions['Statistical']):.2f} | "
            f"Pct={np.mean(scenario_predictions['Percentile']):.2f} | "
            f"Adaptive={np.mean(scenario_predictions['Blind_Adaptive']):.2f}"
        )

    # ========================================================
    # PERFORMANCE SUMMARY
    # ========================================================

    print("\n" + "=" * 100)
    print("BASELINE PERFORMANCE COMPARISON")
    print("=" * 100)

    summary_results = []

    print(
        f"\n{'Method':<20}"
        f"{'Accuracy':<12}"
        f"{'Precision':<12}"
        f"{'Recall':<12}"
        f"{'F1 Score':<12}"
        f"{'FPR':<12}"
        f"{'FNR':<12}"
    )

    print("-" * 92)

    for method in methods:

        metrics = calculate_metrics(
            ground_truth,
            predictions[method]
        )

        summary_results.append({
            "method": method,
            **metrics
        })

        print(
            f"{method:<20}"
            f"{metrics['accuracy']:<12.4f}"
            f"{metrics['precision']:<12.4f}"
            f"{metrics['recall']:<12.4f}"
            f"{metrics['f1_score']:<12.4f}"
            f"{metrics['fpr']:<12.4f}"
            f"{metrics['fnr']:<12.4f}"
        )

    # ========================================================
    # SAVE RESULTS
    # ========================================================

    os.makedirs(
        "experiments",
        exist_ok=True
    )

    detailed_df = pd.DataFrame(
        detailed_results
    )

    summary_df = pd.DataFrame(
        summary_results
    )

    detailed_path = (
        "experiments/"
        "baseline_comparison_detailed.csv"
    )

    summary_path = (
        "experiments/"
        "baseline_comparison_summary.csv"
    )

    detailed_df.to_csv(
        detailed_path,
        index=False
    )

    summary_df.to_csv(
        summary_path,
        index=False
    )

    # ========================================================
    # FINAL CONCLUSION
    # ========================================================

    best_method = summary_df.loc[
        summary_df["f1_score"].idxmax()
    ]

    print("\n" + "=" * 100)
    print("BASELINE COMPARISON CONCLUSION")
    print("=" * 100)

    print(
        f"\nBest Method by F1 Score: "
        f"{best_method['method']}"
    )

    print(
        f"Accuracy: "
        f"{best_method['accuracy']:.4f}"
    )

    print(
        f"F1 Score: "
        f"{best_method['f1_score']:.4f}"
    )

    print(
        f"False Positive Rate: "
        f"{best_method['fpr']:.4f}"
    )

    print("\nResults saved:")

    print(
        "1. experiments/"
        "baseline_comparison_detailed.csv"
    )

    print(
        "2. experiments/"
        "baseline_comparison_summary.csv"
    )

    print("\n" + "=" * 100)
    print("PHASE 5C COMPLETED")
    print("=" * 100)


if __name__ == "__main__":
    main()