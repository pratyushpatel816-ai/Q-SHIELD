"""
Q-SHIELD
PHASE 4M: ADAPTIVE THRESHOLD ABLATION STUDY

This experiment evaluates the contribution of different
components of the adaptive threshold mechanism.

Variants:
1. Fixed Threshold
2. Oracle Adaptive Threshold
3. Blind Adaptive Threshold
4. Blind Adaptive without Noise Estimation
5. Blind Adaptive with Reduced Adaptation
"""

from qshield.quantum.teleportation import TeleportationEngine

import csv
import statistics


# ============================================================
# CONFIGURATION
# ============================================================

SHOTS = 2048
TRIALS = 20

FIXED_THRESHOLD = 0.26
BASE_THRESHOLD = 0.26


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def run_probes(
    engine,
    noise_type="none",
    noise_probability=0.0,
    attack_type="none"
):
    """
    Run quantum probes across all three measurement bases.
    """

    results = []

    for basis in ["Z", "X", "Y"]:

        result = engine.run(
            bit=0,
            basis=basis,
            noise_type=noise_type,
            noise_probability=noise_probability,
            attack_type=attack_type
        )

        results.append(result)

    return results


def calculate_mismatch(probes):
    """
    Calculate average mismatch across all bases.
    """

    mismatches = [
        probe["mismatch_rate"]
        for probe in probes
    ]

    return sum(mismatches) / len(mismatches)


def estimate_noise_from_probes(probes):
    """
    Blind noise estimator.

    Uses the minimum mismatch among measurement bases.

    This provides a simple estimate of natural channel noise
    without directly using the true noise probability.
    """

    mismatch_rates = [
        probe["mismatch_rate"]
        for probe in probes
    ]

    estimated_noise = min(mismatch_rates)

    return estimated_noise


def calculate_metrics(
    true_positive,
    false_positive,
    true_negative,
    false_negative
):
    """
    Calculate classification metrics.
    """

    total = (
        true_positive
        + false_positive
        + true_negative
        + false_negative
    )

    accuracy = (
        (true_positive + true_negative) / total
        if total > 0
        else 0
    )

    precision = (
        true_positive /
        (true_positive + false_positive)
        if (true_positive + false_positive) > 0
        else 0
    )

    recall = (
        true_positive /
        (true_positive + false_negative)
        if (true_positive + false_negative) > 0
        else 0
    )

    f1_score = (
        2 * precision * recall /
        (precision + recall)
        if (precision + recall) > 0
        else 0
    )

    false_positive_rate = (
        false_positive /
        (false_positive + true_negative)
        if (false_positive + true_negative) > 0
        else 0
    )

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
        "fpr": false_positive_rate
    }


# ============================================================
# THRESHOLD VARIANTS
# ============================================================

def fixed_threshold(
    true_noise,
    estimated_noise
):
    """
    Standard fixed threshold.
    """

    return FIXED_THRESHOLD


def oracle_adaptive_threshold(
    true_noise,
    estimated_noise
):
    """
    Oracle adaptive threshold.

    Uses true channel noise.
    This is included as an upper-bound reference.
    """

    adaptation_factor = 0.40

    threshold = (
        BASE_THRESHOLD
        + adaptation_factor * true_noise
    )

    return min(threshold, 0.50)


def blind_adaptive_threshold(
    true_noise,
    estimated_noise
):
    """
    Blind adaptive threshold.

    Uses estimated noise instead of true noise.
    """

    adaptation_factor = 0.40

    threshold = (
        BASE_THRESHOLD
        + adaptation_factor * estimated_noise
    )

    return min(threshold, 0.50)


def no_estimation_threshold(
    true_noise,
    estimated_noise
):
    """
    Ablation variant.

    Removes noise estimation.
    Equivalent to using only the base threshold.
    """

    return BASE_THRESHOLD


def reduced_adaptation_threshold(
    true_noise,
    estimated_noise
):
    """
    Ablation variant.

    Uses blind estimation but reduces
    the adaptation strength.
    """

    adaptation_factor = 0.15

    threshold = (
        BASE_THRESHOLD
        + adaptation_factor * estimated_noise
    )

    return min(threshold, 0.50)


# ============================================================
# MAIN EXPERIMENT
# ============================================================

def run_experiment():

    print()
    print("=" * 105)
    print("Q-SHIELD")
    print("PHASE 4M: ADAPTIVE THRESHOLD ABLATION STUDY")
    print("=" * 105)

    print()
    print(f"Fixed Threshold: {FIXED_THRESHOLD}")
    print(f"Base Threshold: {BASE_THRESHOLD}")
    print(f"Trials per Scenario: {TRIALS}")

    # --------------------------------------------------------
    # INITIALIZE QUANTUM ENGINE
    # --------------------------------------------------------

    engine = TeleportationEngine(
        shots=SHOTS
    )

    # --------------------------------------------------------
    # EXPERIMENT SCENARIOS
    # --------------------------------------------------------

    scenarios = [

        # NORMAL CONDITIONS

        {
            "name": "Clean_Channel",
            "noise": 0.00,
            "noise_type": "none",
            "attack": "none",
            "label": "NORMAL"
        },

        {
            "name": "Noise_0.05",
            "noise": 0.05,
            "noise_type": "bit_flip",
            "attack": "none",
            "label": "NORMAL"
        },

        {
            "name": "Noise_0.10",
            "noise": 0.10,
            "noise_type": "bit_flip",
            "attack": "none",
            "label": "NORMAL"
        },

        {
            "name": "Noise_0.15",
            "noise": 0.15,
            "noise_type": "bit_flip",
            "attack": "none",
            "label": "NORMAL"
        },

        {
            "name": "Noise_0.20",
            "noise": 0.20,
            "noise_type": "bit_flip",
            "attack": "none",
            "label": "NORMAL"
        },

        {
            "name": "Noise_0.25",
            "noise": 0.25,
            "noise_type": "bit_flip",
            "attack": "none",
            "label": "NORMAL"
        },

        {
            "name": "Noise_0.30",
            "noise": 0.30,
            "noise_type": "bit_flip",
            "attack": "none",
            "label": "NORMAL"
        },

        # ATTACK CONDITIONS

        {
            "name": "Pauli_X",
            "noise": 0.00,
            "noise_type": "none",
            "attack": "pauli_x",
            "label": "ATTACK"
        },

        {
            "name": "Pauli_Y",
            "noise": 0.00,
            "noise_type": "none",
            "attack": "pauli_y",
            "label": "ATTACK"
        },

        {
            "name": "Pauli_Z",
            "noise": 0.00,
            "noise_type": "none",
            "attack": "pauli_z",
            "label": "ATTACK"
        },

        {
            "name": "Entanglement_Disruption",
            "noise": 0.00,
            "noise_type": "none",
            "attack": "entanglement_disruption",
            "label": "ATTACK"
        },

        {
            "name": "Pauli_X_Noise",
            "noise": 0.10,
            "noise_type": "bit_flip",
            "attack": "pauli_x",
            "label": "ATTACK"
        },

        {
            "name": "Pauli_Y_Noise",
            "noise": 0.10,
            "noise_type": "bit_flip",
            "attack": "pauli_y",
            "label": "ATTACK"
        },

        {
            "name": "Pauli_Z_Noise",
            "noise": 0.10,
            "noise_type": "bit_flip",
            "attack": "pauli_z",
            "label": "ATTACK"
        },

        {
            "name": "Disruption_Noise",
            "noise": 0.10,
            "noise_type": "bit_flip",
            "attack": "entanglement_disruption",
            "label": "ATTACK"
        }
    ]

    # --------------------------------------------------------
    # DEFINE ABLATION VARIANTS
    # --------------------------------------------------------

    variants = {

        "Fixed": fixed_threshold,

        "Oracle_Adaptive": (
            oracle_adaptive_threshold
        ),

        "Blind_Adaptive": (
            blind_adaptive_threshold
        ),

        "No_Noise_Estimation": (
            no_estimation_threshold
        ),

        "Reduced_Adaptation": (
            reduced_adaptation_threshold
        )
    }

    # --------------------------------------------------------
    # CONFUSION MATRICES
    # --------------------------------------------------------

    confusion = {}

    for variant_name in variants:

        confusion[variant_name] = {
            "TP": 0,
            "FP": 0,
            "TN": 0,
            "FN": 0
        }

    detailed_results = []

    # ========================================================
    # RUN EXPERIMENT
    # ========================================================

    print()
    print("-" * 105)
    print("RUNNING ABLATION EXPERIMENT")
    print("-" * 105)

    for scenario in scenarios:

        print()
        print(
            f"Scenario: {scenario['name']}"
        )

        scenario_statistics = {}

        for variant_name in variants:

            scenario_statistics[
                variant_name
            ] = {
                "thresholds": [],
                "mismatches": [],
                "rejections": 0
            }

        # ----------------------------------------------------
        # MULTIPLE INDEPENDENT TRIALS
        # ----------------------------------------------------

        for trial in range(TRIALS):

            probes = run_probes(
                engine=engine,
                noise_type=scenario["noise_type"],
                noise_probability=scenario["noise"],
                attack_type=scenario["attack"]
            )

            mismatch = calculate_mismatch(
                probes
            )

            estimated_noise = (
                estimate_noise_from_probes(
                    probes
                )
            )

            # ------------------------------------------------
            # EVALUATE EACH VARIANT
            # ------------------------------------------------

            for (
                variant_name,
                threshold_function
            ) in variants.items():

                threshold = threshold_function(
                    scenario["noise"],
                    estimated_noise
                )

                predicted_attack = (
                    mismatch >= threshold
                )

                actual_attack = (
                    scenario["label"]
                    == "ATTACK"
                )

                scenario_statistics[
                    variant_name
                ]["thresholds"].append(
                    threshold
                )

                scenario_statistics[
                    variant_name
                ]["mismatches"].append(
                    mismatch
                )

                if predicted_attack:

                    scenario_statistics[
                        variant_name
                    ]["rejections"] += 1

                # --------------------------------------------
                # UPDATE CONFUSION MATRIX
                # --------------------------------------------

                if (
                    actual_attack
                    and predicted_attack
                ):

                    confusion[
                        variant_name
                    ]["TP"] += 1

                elif (
                    not actual_attack
                    and predicted_attack
                ):

                    confusion[
                        variant_name
                    ]["FP"] += 1

                elif (
                    not actual_attack
                    and not predicted_attack
                ):

                    confusion[
                        variant_name
                    ]["TN"] += 1

                elif (
                    actual_attack
                    and not predicted_attack
                ):

                    confusion[
                        variant_name
                    ]["FN"] += 1

        # ----------------------------------------------------
        # PRINT SCENARIO RESULTS
        # ----------------------------------------------------

        for variant_name in variants:

            average_threshold = statistics.mean(
                scenario_statistics[
                    variant_name
                ]["thresholds"]
            )

            average_mismatch = statistics.mean(
                scenario_statistics[
                    variant_name
                ]["mismatches"]
            )

            rejection_rate = (
                scenario_statistics[
                    variant_name
                ]["rejections"]
                / TRIALS
            )

            detailed_results.append({

                "scenario": scenario["name"],

                "variant": variant_name,

                "label": scenario["label"],

                "true_noise":
                    scenario["noise"],

                "mean_threshold":
                    round(
                        average_threshold,
                        6
                    ),

                "mean_mismatch":
                    round(
                        average_mismatch,
                        6
                    ),

                "rejection_rate":
                    round(
                        rejection_rate,
                        6
                    )
            })

            print(
                f"{variant_name:<25} "
                f"Threshold={average_threshold:.4f} | "
                f"Mismatch={average_mismatch:.4f} | "
                f"Rejected={rejection_rate:.2%}"
            )

    # ========================================================
    # PERFORMANCE SUMMARY
    # ========================================================

    print()
    print("=" * 105)
    print("ABLATION PERFORMANCE COMPARISON")
    print("=" * 105)

    print()
    print(
        f"{'Variant':<25}"
        f"{'Accuracy':<12}"
        f"{'Precision':<12}"
        f"{'Recall':<12}"
        f"{'F1 Score':<12}"
        f"{'FPR':<12}"
    )

    print("-" * 85)

    summary_results = []

    for variant_name in variants:

        metrics = calculate_metrics(

            confusion[variant_name]["TP"],

            confusion[variant_name]["FP"],

            confusion[variant_name]["TN"],

            confusion[variant_name]["FN"]
        )

        print(
            f"{variant_name:<25}"
            f"{metrics['accuracy']:<12.4f}"
            f"{metrics['precision']:<12.4f}"
            f"{metrics['recall']:<12.4f}"
            f"{metrics['f1_score']:<12.4f}"
            f"{metrics['fpr']:<12.4f}"
        )

        summary_results.append({

            "variant": variant_name,

            "accuracy":
                round(
                    metrics["accuracy"],
                    6
                ),

            "precision":
                round(
                    metrics["precision"],
                    6
                ),

            "recall":
                round(
                    metrics["recall"],
                    6
                ),

            "f1_score":
                round(
                    metrics["f1_score"],
                    6
                ),

            "fpr":
                round(
                    metrics["fpr"],
                    6
                ),

            "TP":
                confusion[variant_name]["TP"],

            "FP":
                confusion[variant_name]["FP"],

            "TN":
                confusion[variant_name]["TN"],

            "FN":
                confusion[variant_name]["FN"]
        })

    # ========================================================
    # CONFUSION MATRICES
    # ========================================================

    print()
    print("=" * 105)
    print("CONFUSION MATRIX BY VARIANT")
    print("=" * 105)

    for variant_name in variants:

        matrix = confusion[
            variant_name
        ]

        print()
        print(variant_name)

        print(
            f"TP={matrix['TP']} | "
            f"FP={matrix['FP']} | "
            f"TN={matrix['TN']} | "
            f"FN={matrix['FN']}"
        )

    # ========================================================
    # SAVE DETAILED RESULTS
    # ========================================================

    detailed_file = (
        "experiments/"
        "adaptive_ablation_detailed.csv"
    )

    with open(
        detailed_file,
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[

                "scenario",

                "variant",

                "label",

                "true_noise",

                "mean_threshold",

                "mean_mismatch",

                "rejection_rate"
            ]
        )

        writer.writeheader()

        writer.writerows(
            detailed_results
        )

    # ========================================================
    # SAVE SUMMARY RESULTS
    # ========================================================

    summary_file = (
        "experiments/"
        "adaptive_ablation_summary.csv"
    )

    with open(
        summary_file,
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[

                "variant",

                "accuracy",

                "precision",

                "recall",

                "f1_score",

                "fpr",

                "TP",

                "FP",

                "TN",

                "FN"
            ]
        )

        writer.writeheader()

        writer.writerows(
            summary_results
        )

    # ========================================================
    # CONCLUSION
    # ========================================================

    print()
    print("=" * 105)
    print("ABLATION STUDY CONCLUSION")
    print("=" * 105)

    best_variant = max(
        summary_results,
        key=lambda item: (
            item["f1_score"],
            item["accuracy"],
            -item["fpr"]
        )
    )

    print()

    print(
        f"Best Performing Variant: "
        f"{best_variant['variant']}"
    )

    print(
        f"Accuracy: "
        f"{best_variant['accuracy']:.4f}"
    )

    print(
        f"F1 Score: "
        f"{best_variant['f1_score']:.4f}"
    )

    print(
        f"False Positive Rate: "
        f"{best_variant['fpr']:.4f}"
    )

    print()

    print("Results saved to:")

    print(
        f"1. {detailed_file}"
    )

    print(
        f"2. {summary_file}"
    )

    print()
    print("=" * 105)
    print("PHASE 4M COMPLETED")
    print("=" * 105)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    run_experiment()