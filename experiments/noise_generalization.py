from qshield.quantum.teleportation import TeleportationEngine
from qshield.security.threat_detector import QuantumThreatDetector

import csv


FIXED_THRESHOLD = 0.26
SHOTS = 2048
TRIALS = 20


def run_probes(
    engine,
    noise_type,
    noise_probability,
    attack_type
):
    """
    Run probes across X, Y and Z bases.
    """

    probes = []

    for basis in ["Z", "X", "Y"]:

        result = engine.run(
            bit=0,
            basis=basis,
            noise_type=noise_type,
            noise_probability=noise_probability,
            attack_type=attack_type
        )

        probes.append(result)

    return probes


def evaluate_scenario(
    engine,
    detector,
    noise_type,
    noise_probability,
    attack_type,
    label
):
    """
    Evaluate one scenario repeatedly.
    """

    rejected = 0

    for _ in range(TRIALS):

        probes = run_probes(
            engine,
            noise_type,
            noise_probability,
            attack_type
        )

        analysis = detector.analyze(probes)

        if analysis["decision"] == "REJECT":
            rejected += 1

    rejection_rate = rejected / TRIALS

    if label == "ATTACK":
        detection_rate = rejection_rate
        false_positive_rate = 0.0
    else:
        detection_rate = 0.0
        false_positive_rate = rejection_rate

    return {
        "rejected": rejected,
        "rejection_rate": rejection_rate,
        "detection_rate": detection_rate,
        "false_positive_rate": false_positive_rate
    }


def calculate_metrics(tp, fp, tn, fn):

    accuracy = (
        (tp + tn) / (tp + fp + tn + fn)
        if (tp + fp + tn + fn) > 0
        else 0
    )

    precision = (
        tp / (tp + fp)
        if (tp + fp) > 0
        else 0
    )

    recall = (
        tp / (tp + fn)
        if (tp + fn) > 0
        else 0
    )

    f1_score = (
        2 * precision * recall /
        (precision + recall)
        if (precision + recall) > 0
        else 0
    )

    fpr = (
        fp / (fp + tn)
        if (fp + tn) > 0
        else 0
    )

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
        "fpr": fpr
    }


def run_experiment():

    print()
    print("=" * 100)
    print("Q-SHIELD")
    print("PHASE 4Q: NOISE MODEL GENERALIZATION ANALYSIS")
    print("=" * 100)

    print()
    print(f"Fixed Rejection Threshold: {FIXED_THRESHOLD}")
    print(f"Quantum Shots: {SHOTS}")
    print(f"Trials per Scenario: {TRIALS}")

    engine = TeleportationEngine(
        shots=SHOTS
    )

    detector = QuantumThreatDetector(
        warn_threshold=0.05,
        reject_threshold=FIXED_THRESHOLD
    )

    noise_models = [

        "bit_flip",

        "phase_flip",

        "bit_phase_flip",

        "depolarizing",

        "readout"
    ]

    noise_probabilities = [
        0.00,
        0.05,
        0.10,
        0.15,
        0.20
    ]

    attacks = [

        "pauli_x",

        "pauli_y",

        "pauli_z",

        "entanglement_disruption"
    ]

    detailed_results = []

    summary_results = []

    print()
    print("-" * 100)
    print("RUNNING MULTI-NOISE GENERALIZATION EXPERIMENT")
    print("-" * 100)

    for noise_type in noise_models:

        print()
        print("=" * 100)
        print(
            f"NOISE MODEL: {noise_type.upper()}"
        )
        print("=" * 100)

        tp = 0
        fp = 0
        tn = 0
        fn = 0

        # ============================================================
        # NORMAL CHANNEL CONDITIONS
        # ============================================================

        print()
        print("NORMAL CHANNEL CONDITIONS")
        print("-" * 100)

        for probability in noise_probabilities:

            result = evaluate_scenario(
                engine=engine,
                detector=detector,
                noise_type=noise_type,
                noise_probability=probability,
                attack_type="none",
                label="NORMAL"
            )

            fp += result["rejected"]
            tn += TRIALS - result["rejected"]

            print(
                f"Noise={probability:.2f} | "
                f"Rejected={result['rejected']}/{TRIALS} | "
                f"FPR={result['false_positive_rate']:.2%}"
            )

            detailed_results.append({

                "noise_model": noise_type,

                "condition": "NORMAL",

                "noise_probability": probability,

                "attack_type": "none",

                "rejected": result["rejected"],

                "trials": TRIALS,

                "rejection_rate":
                    round(
                        result["rejection_rate"],
                        6
                    ),

                "detection_rate":
                    round(
                        result["detection_rate"],
                        6
                    ),

                "false_positive_rate":
                    round(
                        result["false_positive_rate"],
                        6
                    )
            })

        # ============================================================
        # ATTACK CONDITIONS
        # ============================================================

        print()
        print("ATTACK CONDITIONS")
        print("-" * 100)

        for attack in attacks:

            for probability in [
                0.00,
                0.05,
                0.10
            ]:

                result = evaluate_scenario(
                    engine=engine,
                    detector=detector,
                    noise_type=noise_type,
                    noise_probability=probability,
                    attack_type=attack,
                    label="ATTACK"
                )

                tp += result["rejected"]
                fn += TRIALS - result["rejected"]

                print(
                    f"Attack={attack:<28} "
                    f"Noise={probability:.2f} | "
                    f"Detected={result['rejected']}/{TRIALS} | "
                    f"Detection={result['detection_rate']:.2%}"
                )

                detailed_results.append({

                    "noise_model": noise_type,

                    "condition": "ATTACK",

                    "noise_probability": probability,

                    "attack_type": attack,

                    "rejected": result["rejected"],

                    "trials": TRIALS,

                    "rejection_rate":
                        round(
                            result["rejection_rate"],
                            6
                        ),

                    "detection_rate":
                        round(
                            result["detection_rate"],
                            6
                        ),

                    "false_positive_rate":
                        round(
                            result["false_positive_rate"],
                            6
                        )
                })

        metrics = calculate_metrics(
            tp,
            fp,
            tn,
            fn
        )

        summary_results.append({

            "noise_model": noise_type,

            "TP": tp,

            "FP": fp,

            "TN": tn,

            "FN": fn,

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
                )
        })

    # ================================================================
    # FINAL COMPARISON
    # ================================================================

    print()
    print("=" * 100)
    print("NOISE MODEL GENERALIZATION SUMMARY")
    print("=" * 100)

    print()

    print(
        f"{'Noise Model':<22}"
        f"{'Accuracy':<14}"
        f"{'Precision':<14}"
        f"{'Recall':<14}"
        f"{'F1 Score':<14}"
        f"{'FPR':<14}"
    )

    print("-" * 92)

    for result in summary_results:

        print(
            f"{result['noise_model']:<22}"
            f"{result['accuracy']:<14.4f}"
            f"{result['precision']:<14.4f}"
            f"{result['recall']:<14.4f}"
            f"{result['f1_score']:<14.4f}"
            f"{result['fpr']:<14.4f}"
        )

    # ================================================================
    # SAVE DETAILED RESULTS
    # ================================================================

    detailed_file = (
        "experiments/"
        "noise_generalization_detailed.csv"
    )

    with open(
        detailed_file,
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[

                "noise_model",

                "condition",

                "noise_probability",

                "attack_type",

                "rejected",

                "trials",

                "rejection_rate",

                "detection_rate",

                "false_positive_rate"
            ]
        )

        writer.writeheader()

        writer.writerows(
            detailed_results
        )

    # ================================================================
    # SAVE SUMMARY RESULTS
    # ================================================================

    summary_file = (
        "experiments/"
        "noise_generalization_summary.csv"
    )

    with open(
        summary_file,
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[

                "noise_model",

                "TP",

                "FP",

                "TN",

                "FN",

                "accuracy",

                "precision",

                "recall",

                "f1_score",

                "fpr"
            ]
        )

        writer.writeheader()

        writer.writerows(
            summary_results
        )

    # ================================================================
    # CONCLUSION
    # ================================================================

    print()
    print("=" * 100)
    print("GENERALIZATION CONCLUSION")
    print("=" * 100)

    best_result = max(
        summary_results,
        key=lambda x: x["f1_score"]
    )

    worst_result = min(
        summary_results,
        key=lambda x: x["f1_score"]
    )

    mean_accuracy = sum(
        x["accuracy"]
        for x in summary_results
    ) / len(summary_results)

    mean_f1 = sum(
        x["f1_score"]
        for x in summary_results
    ) / len(summary_results)

    mean_fpr = sum(
        x["fpr"]
        for x in summary_results
    ) / len(summary_results)

    print()
    print(
        f"Mean Accuracy Across Noise Models: "
        f"{mean_accuracy:.4f}"
    )

    print(
        f"Mean F1 Score Across Noise Models: "
        f"{mean_f1:.4f}"
    )

    print(
        f"Mean False Positive Rate: "
        f"{mean_fpr:.4f}"
    )

    print()

    print(
        f"Best Noise Model Performance: "
        f"{best_result['noise_model']} "
        f"(F1={best_result['f1_score']:.4f})"
    )

    print(
        f"Worst Noise Model Performance: "
        f"{worst_result['noise_model']} "
        f"(F1={worst_result['f1_score']:.4f})"
    )

    print()
    print("Results saved to:")

    print(
        f"1. {detailed_file}"
    )

    print(
        f"2. {summary_file}"
    )

    print("=" * 100)
    print("PHASE 4Q COMPLETED")
    print("=" * 100)


if __name__ == "__main__":
    run_experiment()