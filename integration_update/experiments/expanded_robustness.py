from qshield.quantum.teleportation import TeleportationEngine
from qshield.security.threat_detector import QuantumThreatDetector

import csv
import statistics


OPTIMAL_THRESHOLD = 0.26
SHOTS = 1024
TRIALS_PER_SCENARIO = 20


NORMAL_NOISE_LEVELS = [
    0.00,
    0.02,
    0.05,
    0.08,
    0.10,
    0.12,
    0.15,
    0.18,
    0.20,
    0.25,
    0.30
]


ATTACK_TYPES = [
    "pauli_x",
    "pauli_y",
    "pauli_z",
    "entanglement_disruption"
]


def run_probes(
    engine,
    noise_type="none",
    noise_probability=0.0,
    attack_type="none"
):
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


def evaluate_scenario(
    engine,
    detector,
    noise_type,
    noise_probability,
    attack_type,
    label
):

    decisions = []
    mismatches = []

    for _ in range(TRIALS_PER_SCENARIO):

        probes = run_probes(
            engine=engine,
            noise_type=noise_type,
            noise_probability=noise_probability,
            attack_type=attack_type
        )

        analysis = detector.analyze(probes)

        decision = analysis["decision"]

        mismatch = analysis[
            "evidence"
        ]["average_mismatch_rate"]

        decisions.append(decision)
        mismatches.append(mismatch)

    reject_count = decisions.count(
        "REJECT"
    )

    detection_rate = (
        reject_count /
        TRIALS_PER_SCENARIO
    )

    return {
        "label": label,
        "noise_probability": noise_probability,
        "attack_type": attack_type,
        "mean_mismatch":
            statistics.mean(mismatches),
        "std_mismatch":
            statistics.stdev(mismatches)
            if len(mismatches) > 1
            else 0.0,
        "reject_count": reject_count,
        "trials": TRIALS_PER_SCENARIO,
        "detection_rate": detection_rate
    }


def run_experiment():

    print()
    print("=" * 100)
    print("Q-SHIELD")
    print("PHASE 4J: EXPANDED INDEPENDENT ROBUSTNESS EVALUATION")
    print("=" * 100)

    print(
        f"\nFixed Rejection Threshold: "
        f"{OPTIMAL_THRESHOLD}"
    )

    print(
        f"Trials per Scenario: "
        f"{TRIALS_PER_SCENARIO}"
    )

    engine = TeleportationEngine(
        shots=SHOTS
    )

    detector = QuantumThreatDetector(
        warn_threshold=0.05,
        reject_threshold=OPTIMAL_THRESHOLD
    )

    results = []

    # ==================================================
    # NORMAL CHANNEL EVALUATION
    # ==================================================

    print()
    print("NORMAL CHANNEL CONDITIONS")
    print("-" * 100)

    for noise_level in NORMAL_NOISE_LEVELS:

        result = evaluate_scenario(
            engine=engine,
            detector=detector,
            noise_type="bit_flip",
            noise_probability=noise_level,
            attack_type="none",
            label="NORMAL"
        )

        results.append(result)

        print(
            f"Noise={noise_level:.2f} | "
            f"Mismatch={result['mean_mismatch']:.4f} | "
            f"Rejected={result['reject_count']}/"
            f"{TRIALS_PER_SCENARIO}"
        )

    # ==================================================
    # ATTACK EVALUATION
    # ==================================================

    print()
    print("ATTACK CONDITIONS")
    print("-" * 100)

    attack_noise_levels = [
        0.00,
        0.05,
        0.10
    ]

    for attack_type in ATTACK_TYPES:

        for noise_level in attack_noise_levels:

            noise_type = (
                "none"
                if noise_level == 0.0
                else "bit_flip"
            )

            result = evaluate_scenario(
                engine=engine,
                detector=detector,
                noise_type=noise_type,
                noise_probability=noise_level,
                attack_type=attack_type,
                label="ATTACK"
            )

            results.append(result)

            print(
                f"Attack={attack_type:<28} "
                f"Noise={noise_level:.2f} | "
                f"Mismatch={result['mean_mismatch']:.4f} | "
                f"Detected={result['reject_count']}/"
                f"{TRIALS_PER_SCENARIO}"
            )

    # ==================================================
    # GLOBAL PERFORMANCE METRICS
    # ==================================================

    tp = 0
    fp = 0
    tn = 0
    fn = 0

    for result in results:

        predicted_rejects = (
            result["reject_count"]
        )

        predicted_accepts = (
            result["trials"] -
            predicted_rejects
        )

        if result["label"] == "ATTACK":

            tp += predicted_rejects
            fn += predicted_accepts

        else:

            fp += predicted_rejects
            tn += predicted_accepts

    accuracy = (
        (tp + tn) /
        (tp + tn + fp + fn)
    )

    precision = (
        tp / (tp + fp)
        if (tp + fp) > 0
        else 0.0
    )

    recall = (
        tp / (tp + fn)
        if (tp + fn) > 0
        else 0.0
    )

    f1_score = (
        2 * precision * recall /
        (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )

    fpr = (
        fp / (fp + tn)
        if (fp + tn) > 0
        else 0.0
    )

    # ==================================================
    # RESULTS
    # ==================================================

    print()
    print("=" * 100)
    print("INDEPENDENT ROBUSTNESS EVALUATION RESULTS")
    print("=" * 100)

    print(
        f"True Positives:  {tp}"
    )

    print(
        f"False Positives: {fp}"
    )

    print(
        f"True Negatives:  {tn}"
    )

    print(
        f"False Negatives: {fn}"
    )

    print()

    print(
        f"Accuracy:        "
        f"{accuracy:.4f}"
    )

    print(
        f"Precision:       "
        f"{precision:.4f}"
    )

    print(
        f"Recall:          "
        f"{recall:.4f}"
    )

    print(
        f"F1 Score:        "
        f"{f1_score:.4f}"
    )

    print(
        f"False Positive Rate: "
        f"{fpr:.4f}"
    )

    # ==================================================
    # SAVE RESULTS
    # ==================================================

    output_file = (
        "experiments/"
        "expanded_robustness_results.csv"
    )

    with open(
        output_file,
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "label",
                "noise_probability",
                "attack_type",
                "mean_mismatch",
                "std_mismatch",
                "reject_count",
                "trials",
                "detection_rate"
            ]
        )

        writer.writeheader()

        writer.writerows(results)

    print()
    print(
        f"Results saved to:\n"
        f"{output_file}"
    )

    print("=" * 100)
    print("PHASE 4J COMPLETED")
    print("=" * 100)


if __name__ == "__main__":
    run_experiment()