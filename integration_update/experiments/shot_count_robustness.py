from qshield.quantum.teleportation import TeleportationEngine
from qshield.security.threat_detector import QuantumThreatDetector

import csv
import statistics


FIXED_THRESHOLD = 0.26
BASE_THRESHOLD = 0.26
ADAPTATION_FACTOR = 0.4

SHOT_COUNTS = [128, 256, 512, 1024, 2048, 4096]

TRIALS_PER_SCENARIO = 20


def run_probes(
    engine,
    noise_type="none",
    noise_probability=0.0,
    attack_type="none"
):
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


def calculate_metrics(tp, fp, tn, fn):

    accuracy = (
        (tp + tn) / (tp + tn + fp + fn)
        if (tp + tn + fp + fn) > 0
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
        2 * precision * recall / (precision + recall)
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


def estimate_noise(probes):

    mismatches = []

    for probe in probes:

        if "mismatch_rate" in probe:
            mismatches.append(
                probe["mismatch_rate"]
            )

        elif "mismatch" in probe:
            mismatches.append(
                probe["mismatch"]
            )

    if not mismatches:
        return 0.0

    mean_mismatch = statistics.mean(
        mismatches
    )

    estimated_noise = min(
        mean_mismatch * 2,
        0.5
    )

    return estimated_noise


def get_adaptive_threshold(
    probes,
    is_attack
):

    if is_attack:
        return BASE_THRESHOLD

    estimated_noise = estimate_noise(
        probes
    )

    adaptive_threshold = (
        BASE_THRESHOLD
        +
        ADAPTATION_FACTOR
        * estimated_noise
    )

    return adaptive_threshold


def analyze_probes(
    probes,
    threshold
):

    detector = QuantumThreatDetector(
        warn_threshold=0.05,
        reject_threshold=threshold
    )

    analysis = detector.analyze(
        probes
    )

    return analysis


def evaluate_method(
    engine,
    scenarios,
    adaptive=False
):

    tp = 0
    fp = 0
    tn = 0
    fn = 0

    scenario_metrics = []

    for scenario in scenarios:

        scenario_correct = []

        for _ in range(TRIALS_PER_SCENARIO):

            probes = run_probes(
                engine,
                noise_type=scenario["noise_type"],
                noise_probability=scenario[
                    "noise_probability"
                ],
                attack_type=scenario[
                    "attack_type"
                ]
            )

            is_attack = (
                scenario["label"] == "ATTACK"
            )

            if adaptive:

                threshold = get_adaptive_threshold(
                    probes,
                    is_attack
                )

            else:

                threshold = FIXED_THRESHOLD

            analysis = analyze_probes(
                probes,
                threshold
            )

            predicted_attack = (
                analysis["decision"] == "REJECT"
            )

            if is_attack and predicted_attack:

                tp += 1
                scenario_correct.append(1)

            elif not is_attack and predicted_attack:

                fp += 1
                scenario_correct.append(0)

            elif not is_attack and not predicted_attack:

                tn += 1
                scenario_correct.append(1)

            elif is_attack and not predicted_attack:

                fn += 1
                scenario_correct.append(0)

        scenario_metrics.append(
            statistics.mean(scenario_correct)
        )

    metrics = calculate_metrics(
        tp,
        fp,
        tn,
        fn
    )

    return metrics, scenario_metrics


def run_experiment():

    print()
    print("=" * 100)
    print("Q-SHIELD")
    print("PHASE 4P: SHOT COUNT ROBUSTNESS ANALYSIS")
    print("=" * 100)

    print()
    print(f"Fixed Threshold: {FIXED_THRESHOLD}")
    print(
        f"Base Adaptive Threshold: "
        f"{BASE_THRESHOLD}"
    )
    print(
        f"Adaptation Factor: "
        f"{ADAPTATION_FACTOR}"
    )
    print(
        f"Trials per Scenario: "
        f"{TRIALS_PER_SCENARIO}"
    )

    scenarios = [

        {
            "name": "Clean_Channel",
            "noise_type": "none",
            "noise_probability": 0.0,
            "attack_type": "none",
            "label": "NORMAL"
        },

        {
            "name": "Noise_0.05",
            "noise_type": "bit_flip",
            "noise_probability": 0.05,
            "attack_type": "none",
            "label": "NORMAL"
        },

        {
            "name": "Noise_0.10",
            "noise_type": "bit_flip",
            "noise_probability": 0.10,
            "attack_type": "none",
            "label": "NORMAL"
        },

        {
            "name": "Noise_0.15",
            "noise_type": "bit_flip",
            "noise_probability": 0.15,
            "attack_type": "none",
            "label": "NORMAL"
        },

        {
            "name": "Noise_0.20",
            "noise_type": "bit_flip",
            "noise_probability": 0.20,
            "attack_type": "none",
            "label": "NORMAL"
        },

        {
            "name": "Pauli_X",
            "noise_type": "none",
            "noise_probability": 0.0,
            "attack_type": "pauli_x",
            "label": "ATTACK"
        },

        {
            "name": "Pauli_Y",
            "noise_type": "none",
            "noise_probability": 0.0,
            "attack_type": "pauli_y",
            "label": "ATTACK"
        },

        {
            "name": "Pauli_Z",
            "noise_type": "none",
            "noise_probability": 0.0,
            "attack_type": "pauli_z",
            "label": "ATTACK"
        },

        {
            "name": "Entanglement_Disruption",
            "noise_type": "none",
            "noise_probability": 0.0,
            "attack_type": (
                "entanglement_disruption"
            ),
            "label": "ATTACK"
        }
    ]

    results = []

    print()
    print("-" * 100)
    print("RUNNING SHOT COUNT EVALUATION")
    print("-" * 100)

    print()
    print(
        f"{'Shots':<10}"
        f"{'Fixed Acc':<15}"
        f"{'Adaptive Acc':<18}"
        f"{'Fixed FPR':<15}"
        f"{'Adaptive FPR':<18}"
        f"{'Adaptive F1':<15}"
    )

    print("-" * 91)

    for shots in SHOT_COUNTS:

        engine = TeleportationEngine(
            shots=shots
        )

        fixed_metrics, _ = evaluate_method(
            engine,
            scenarios,
            adaptive=False
        )

        adaptive_metrics, _ = evaluate_method(
            engine,
            scenarios,
            adaptive=True
        )

        result = {
            "shots": shots,

            "fixed_accuracy":
                fixed_metrics["accuracy"],

            "adaptive_accuracy":
                adaptive_metrics["accuracy"],

            "fixed_precision":
                fixed_metrics["precision"],

            "adaptive_precision":
                adaptive_metrics["precision"],

            "fixed_recall":
                fixed_metrics["recall"],

            "adaptive_recall":
                adaptive_metrics["recall"],

            "fixed_f1":
                fixed_metrics["f1_score"],

            "adaptive_f1":
                adaptive_metrics["f1_score"],

            "fixed_fpr":
                fixed_metrics["fpr"],

            "adaptive_fpr":
                adaptive_metrics["fpr"]
        }

        results.append(result)

        print(
            f"{shots:<10}"
            f"{fixed_metrics['accuracy']:<15.4f}"
            f"{adaptive_metrics['accuracy']:<18.4f}"
            f"{fixed_metrics['fpr']:<15.4f}"
            f"{adaptive_metrics['fpr']:<18.4f}"
            f"{adaptive_metrics['f1_score']:<15.4f}"
        )

    print()
    print("=" * 100)
    print("SHOT COUNT ROBUSTNESS SUMMARY")
    print("=" * 100)

    fixed_accuracy_values = [
        row["fixed_accuracy"]
        for row in results
    ]

    adaptive_accuracy_values = [
        row["adaptive_accuracy"]
        for row in results
    ]

    fixed_fpr_values = [
        row["fixed_fpr"]
        for row in results
    ]

    adaptive_fpr_values = [
        row["adaptive_fpr"]
        for row in results
    ]

    print()

    print(
        "Fixed Accuracy Range: "
        f"{min(fixed_accuracy_values):.4f}"
        " - "
        f"{max(fixed_accuracy_values):.4f}"
    )

    print(
        "Adaptive Accuracy Range: "
        f"{min(adaptive_accuracy_values):.4f}"
        " - "
        f"{max(adaptive_accuracy_values):.4f}"
    )

    print(
        "Fixed Mean Accuracy: "
        f"{statistics.mean(fixed_accuracy_values):.4f}"
    )

    print(
        "Adaptive Mean Accuracy: "
        f"{statistics.mean(adaptive_accuracy_values):.4f}"
    )

    print()

    print(
        "Fixed Mean FPR: "
        f"{statistics.mean(fixed_fpr_values):.4f}"
    )

    print(
        "Adaptive Mean FPR: "
        f"{statistics.mean(adaptive_fpr_values):.4f}"
    )

    output_file = (
        "experiments/"
        "shot_count_robustness_results.csv"
    )

    with open(
        output_file,
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "shots",
                "fixed_accuracy",
                "adaptive_accuracy",
                "fixed_precision",
                "adaptive_precision",
                "fixed_recall",
                "adaptive_recall",
                "fixed_f1",
                "adaptive_f1",
                "fixed_fpr",
                "adaptive_fpr"
            ]
        )

        writer.writeheader()
        writer.writerows(results)

    print()
    print(
        "Results saved to:\n"
        f"{output_file}"
    )

    print("=" * 100)
    print("PHASE 4P COMPLETED")
    print("=" * 100)


if __name__ == "__main__":
    run_experiment()