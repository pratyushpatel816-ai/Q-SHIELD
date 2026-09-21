from qshield.quantum.teleportation import TeleportationEngine
from qshield.security.threat_detector import (
    QuantumThreatDetector
)

import csv
import statistics


FIXED_THRESHOLD = 0.26
BASE_THRESHOLD = 0.26
ADAPTATION_FACTOR = 0.40

SHOTS = 2048
TRIALS = 20


def run_probes(
    engine,
    noise_type="none",
    noise_probability=0.0,
    attack_type="none"
):
    """
    Execute quantum probes across Z, X and Y bases.
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


def get_average_mismatch(probes):
    """
    Calculate aggregate mismatch rate.
    """

    mismatches = [
        probe["mismatch_rate"]
        for probe in probes
    ]

    return statistics.mean(mismatches)


def estimate_noise_from_probes(probes):
    """
    Blind channel-noise estimation.

    The estimator uses basis-dependent mismatch
    behavior observed during normal channel
    operation.

    Important:
    This is a heuristic measurement-derived
    estimate and does not use the true simulator
    noise probability.
    """

    basis_mismatch = {}

    for probe in probes:

        basis = probe["basis"]

        basis_mismatch[basis] = (
            probe["mismatch_rate"]
        )

    # Bit-flip noise affects X/Y bases more strongly
    # than Z basis in this simulation model.
    #
    # Estimate natural channel degradation from
    # the difference between basis mismatch rates.

    z_mismatch = basis_mismatch.get(
        "Z",
        0.0
    )

    x_mismatch = basis_mismatch.get(
        "X",
        0.0
    )

    y_mismatch = basis_mismatch.get(
        "Y",
        0.0
    )

    transverse_noise = (
        x_mismatch + y_mismatch
    ) / 2

    # Estimated noise proxy.
    estimated_noise = max(
        0.0,
        transverse_noise - z_mismatch
    )

    # Scale the proxy to a practical range.
    estimated_noise = min(
        estimated_noise * 2.0,
        0.50
    )

    return estimated_noise


def calculate_blind_threshold(
    estimated_noise
):
    """
    Calculate threshold using estimated noise.

    T = T_base + alpha * estimated_noise
    """

    threshold = (
        BASE_THRESHOLD
        + ADAPTATION_FACTOR
        * estimated_noise
    )

    return min(
        threshold,
        0.60
    )


def analyze_with_threshold(
    probes,
    threshold
):

    detector = QuantumThreatDetector(
        warn_threshold=0.05,
        reject_threshold=threshold
    )

    return detector.analyze(
        probes
    )


def calculate_metrics(
    predictions,
    labels
):

    tp = fp = tn = fn = 0

    for prediction, label in zip(
        predictions,
        labels
    ):

        actual_attack = (
            label == "ATTACK"
        )

        if actual_attack and prediction:
            tp += 1

        elif not actual_attack and prediction:
            fp += 1

        elif not actual_attack and not prediction:
            tn += 1

        else:
            fn += 1

    total = tp + fp + tn + fn

    accuracy = (
        (tp + tn) / total
        if total else 0
    )

    precision = (
        tp / (tp + fp)
        if (tp + fp) else 0
    )

    recall = (
        tp / (tp + fn)
        if (tp + fn) else 0
    )

    f1_score = (
        2 * precision * recall /
        (precision + recall)
        if (precision + recall) else 0
    )

    fpr = (
        fp / (fp + tn)
        if (fp + tn) else 0
    )

    return {
        "TP": tp,
        "FP": fp,
        "TN": tn,
        "FN": fn,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
        "fpr": fpr
    }


def run_experiment():

    print()
    print("=" * 105)
    print("Q-SHIELD")
    print("PHASE 4L: BLIND ADAPTIVE THRESHOLD VALIDATION")
    print("=" * 105)

    print(
        f"\nFixed Threshold: {FIXED_THRESHOLD}"
    )

    print(
        f"Base Adaptive Threshold: "
        f"{BASE_THRESHOLD}"
    )

    print(
        f"Adaptation Factor: "
        f"{ADAPTATION_FACTOR}"
    )

    print(
        f"Independent Trials: {TRIALS}"
    )

    engine = TeleportationEngine(
        shots=SHOTS
    )

    scenarios = [

        # NORMAL CHANNELS

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

        # PURE ATTACKS

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
            "attack": (
                "entanglement_disruption"
            ),
            "label": "ATTACK"
        },

        # ATTACK + NOISE

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
            "attack": (
                "entanglement_disruption"
            ),
            "label": "ATTACK"
        }
    ]

    fixed_predictions = []
    blind_predictions = []
    labels = []

    rows = []

    print()

    print(
        f"{'Scenario':<28}"
        f"{'True Noise':<12}"
        f"{'Est. Noise':<12}"
        f"{'Blind T':<12}"
        f"{'Fixed Reject':<15}"
        f"{'Blind Reject':<15}"
    )

    print("-" * 94)

    for scenario in scenarios:

        fixed_rejected = 0
        blind_rejected = 0

        estimated_noise_values = []
        threshold_values = []

        for _ in range(TRIALS):

            probes = run_probes(
                engine,
                noise_type=scenario[
                    "noise_type"
                ],
                noise_probability=scenario[
                    "noise"
                ],
                attack_type=scenario[
                    "attack"
                ]
            )

            # Fixed baseline
            fixed_analysis = (
                analyze_with_threshold(
                    probes,
                    FIXED_THRESHOLD
                )
            )

            fixed_prediction = (
                fixed_analysis["decision"]
                == "REJECT"
            )

            # Blind estimation
            estimated_noise = (
                estimate_noise_from_probes(
                    probes
                )
            )

            blind_threshold = (
                calculate_blind_threshold(
                    estimated_noise
                )
            )

            blind_analysis = (
                analyze_with_threshold(
                    probes,
                    blind_threshold
                )
            )

            blind_prediction = (
                blind_analysis["decision"]
                == "REJECT"
            )

            if fixed_prediction:
                fixed_rejected += 1

            if blind_prediction:
                blind_rejected += 1

            fixed_predictions.append(
                fixed_prediction
            )

            blind_predictions.append(
                blind_prediction
            )

            labels.append(
                scenario["label"]
            )

            estimated_noise_values.append(
                estimated_noise
            )

            threshold_values.append(
                blind_threshold
            )

        avg_estimated_noise = (
            statistics.mean(
                estimated_noise_values
            )
        )

        avg_threshold = (
            statistics.mean(
                threshold_values
            )
        )

        fixed_rate = (
            fixed_rejected / TRIALS
        )

        blind_rate = (
            blind_rejected / TRIALS
        )

        rows.append({

            "scenario":
                scenario["name"],

            "label":
                scenario["label"],

            "true_noise":
                scenario["noise"],

            "estimated_noise":
                round(
                    avg_estimated_noise,
                    6
                ),

            "blind_threshold":
                round(
                    avg_threshold,
                    6
                ),

            "fixed_rejection_rate":
                round(
                    fixed_rate,
                    6
                ),

            "blind_rejection_rate":
                round(
                    blind_rate,
                    6
                )
        })

        print(
            f"{scenario['name']:<28}"
            f"{scenario['noise']:<12.2f}"
            f"{avg_estimated_noise:<12.4f}"
            f"{avg_threshold:<12.4f}"
            f"{fixed_rate:<15.2%}"
            f"{blind_rate:<15.2%}"
        )

    fixed_metrics = calculate_metrics(
        fixed_predictions,
        labels
    )

    blind_metrics = calculate_metrics(
        blind_predictions,
        labels
    )

    print()
    print("=" * 105)
    print("BLIND ADAPTIVE PERFORMANCE COMPARISON")
    print("=" * 105)

    print()

    print(
        f"{'Metric':<20}"
        f"{'Fixed':<20}"
        f"{'Blind Adaptive':<20}"
    )

    print("-" * 60)

    for metric in [
        "accuracy",
        "precision",
        "recall",
        "f1_score",
        "fpr"
    ]:

        print(
            f"{metric.upper():<20}"
            f"{fixed_metrics[metric]:<20.4f}"
            f"{blind_metrics[metric]:<20.4f}"
        )

    print()

    print(
        f"{'Confusion Matrix':<20}"
        f"{'Fixed':<20}"
        f"{'Blind Adaptive':<20}"
    )

    print("-" * 60)

    for metric in ["TP", "FP", "TN", "FN"]:

        print(
            f"{metric:<20}"
            f"{fixed_metrics[metric]:<20}"
            f"{blind_metrics[metric]:<20}"
        )

    output_file = (
        "experiments/"
        "blind_adaptive_results.csv"
    )

    with open(
        output_file,
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "scenario",
                "label",
                "true_noise",
                "estimated_noise",
                "blind_threshold",
                "fixed_rejection_rate",
                "blind_rejection_rate"
            ]
        )

        writer.writeheader()

        writer.writerows(rows)

    print()
    print(
        f"Results saved to:\n{output_file}"
    )

    print()
    print("=" * 105)
    print("PHASE 4L COMPLETED")
    print("=" * 105)


if __name__ == "__main__":
    run_experiment()