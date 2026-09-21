import random
import numpy as np
import pandas as pd

from qshield.quantum.teleportation import (
    TeleportationEngine
)

from qshield.detection.integrated_detector import (
    IntegratedQShieldDetector
)


# ============================================================
# CONFIGURATION
# ============================================================

SHOTS = 1024
TRIALS = 20

random.seed(42)
np.random.seed(42)


# ============================================================
# TEST SCENARIOS
# ============================================================

NORMAL_SCENARIOS = [

    ("bit_flip", 0.00),
    ("bit_flip", 0.05),
    ("bit_flip", 0.10),
    ("bit_flip", 0.15),
    ("bit_flip", 0.20),

    ("phase_flip", 0.00),
    ("phase_flip", 0.05),
    ("phase_flip", 0.10),
    ("phase_flip", 0.15),
    ("phase_flip", 0.20),

    ("depolarizing", 0.00),
    ("depolarizing", 0.05),
    ("depolarizing", 0.10),
    ("depolarizing", 0.15),
    ("depolarizing", 0.20),

    ("readout", 0.00),
    ("readout", 0.05),
    ("readout", 0.10),
    ("readout", 0.15),
    ("readout", 0.20),
]


ATTACK_SCENARIOS = [

    "pauli_x",
    "pauli_y",
    "pauli_z",
    "entanglement_disruption"
]


# ============================================================
# METRIC FUNCTION
# ============================================================

def calculate_metrics(tp, fp, tn, fn):

    accuracy = (
        (tp + tn)
        / max(tp + fp + tn + fn, 1)
    )

    precision = (
        tp / max(tp + fp, 1)
    )

    recall = (
        tp / max(tp + fn, 1)
    )

    f1 = (
        2 * precision * recall
        / max(precision + recall, 1e-9)
    )

    fpr = (
        fp / max(fp + tn, 1)
    )

    fnr = (
        fn / max(fn + tp, 1)
    )

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "fpr": fpr,
        "fnr": fnr
    }


# ============================================================
# MAIN EXPERIMENT
# ============================================================

def main():

    print("=" * 100)
    print("Q-SHIELD")
    print(
        "PHASE 5E: INTEGRATED SECURITY-CONSTRAINED "
        "DUAL-SIGNAL DETECTOR"
    )
    print("=" * 100)

    print()
    print(f"Quantum Shots: {SHOTS}")
    print(f"Trials per Scenario: {TRIALS}")
    print("Base Threshold: 0.26")
    print("Adaptation Factor: 0.4")
    print("Maximum Threshold: 0.32")

    engine = TeleportationEngine(
        shots=SHOTS
    )

    detector = (
        IntegratedQShieldDetector(
            base_threshold=0.26,
            adaptation_factor=0.4,
            max_threshold=0.32
        )
    )

    results = []

    tp = fp = tn = fn = 0

    # ========================================================
    # NORMAL CHANNEL TESTING
    # ========================================================

    print()
    print("-" * 100)
    print("NORMAL QUANTUM CHANNEL EVALUATION")
    print("-" * 100)

    for noise_type, probability in NORMAL_SCENARIOS:

        detections = 0

        for _ in range(TRIALS):

            bit = random.randint(0, 1)

            basis = random.choice(
                ["X", "Y", "Z"]
            )

            result = engine.run(
                bit=bit,
                basis=basis,
                noise_type=noise_type,
                noise_probability=probability,
                attack_type="none"
            )

            detection = detector.analyze(
                mismatch_rate=result[
                    "mismatch_rate"
                ],
                bell_measurements=result[
                    "bell_measurements"
                ]
            )

            if detection["attack_detected"]:

                detections += 1
                fp += 1

            else:
                tn += 1

            results.append({

                "scenario":
                    f"{noise_type}_{probability}",

                "category":
                    "normal",

                "noise_type":
                    noise_type,

                "noise_probability":
                    probability,

                "attack_type":
                    "none",

                "mismatch_rate":
                    result["mismatch_rate"],

                "security_score":
                    detection["security_score"],

                "adaptive_threshold":
                    detection[
                        "adaptive_threshold"
                    ],

                "bell_anomaly_score":
                    detection[
                        "bell_anomaly_score"
                    ],

                "attack_detected":
                    detection[
                        "attack_detected"
                    ]
            })

        print(
            f"{noise_type:<15} "
            f"Noise={probability:.2f} | "
            f"False Alarms={detections}/{TRIALS}"
        )

    # ========================================================
    # ATTACK TESTING
    # ========================================================

    print()
    print("-" * 100)
    print("ADVERSARIAL QUANTUM ATTACK EVALUATION")
    print("-" * 100)

    for attack_type in ATTACK_SCENARIOS:

        detections = 0

        for _ in range(TRIALS):

            bit = random.randint(0, 1)

            basis = random.choice(
                ["X", "Y", "Z"]
            )

            noise_type = random.choice([
                "bit_flip",
                "phase_flip",
                "bit_phase_flip",
                "depolarizing",
                "readout"
            ])

            probability = random.choice([
                0.05,
                0.10,
                0.15,
                0.20
            ])

            result = engine.run(
                bit=bit,
                basis=basis,
                noise_type=noise_type,
                noise_probability=probability,
                attack_type=attack_type
            )

            detection = detector.analyze(
                mismatch_rate=result[
                    "mismatch_rate"
                ],
                bell_measurements=result[
                    "bell_measurements"
                ]
            )

            if detection["attack_detected"]:

                detections += 1
                tp += 1

            else:
                fn += 1

            results.append({

                "scenario":
                    attack_type,

                "category":
                    "attack",

                "noise_type":
                    noise_type,

                "noise_probability":
                    probability,

                "attack_type":
                    attack_type,

                "mismatch_rate":
                    result["mismatch_rate"],

                "security_score":
                    detection["security_score"],

                "adaptive_threshold":
                    detection[
                        "adaptive_threshold"
                    ],

                "bell_anomaly_score":
                    detection[
                        "bell_anomaly_score"
                    ],

                "attack_detected":
                    detection[
                        "attack_detected"
                    ]
            })

        print(
            f"{attack_type:<30} "
            f"Detected={detections}/{TRIALS}"
        )

    # ========================================================
    # FINAL METRICS
    # ========================================================

    metrics = calculate_metrics(
        tp, fp, tn, fn
    )

    print()
    print("=" * 100)
    print("INTEGRATED Q-SHIELD PERFORMANCE")
    print("=" * 100)

    print()
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

    for name, value in metrics.items():

        print(
            f"{name.upper():<15}: "
            f"{value:.4f}"
        )

    # ========================================================
    # SAVE RESULTS
    # ========================================================

    df = pd.DataFrame(results)

    df.to_csv(
        "experiments/"
        "integrated_detector_results.csv",
        index=False
    )

    summary = pd.DataFrame([{

        "method":
            "Integrated Q-SHIELD",

        **metrics

    }])

    summary.to_csv(
        "experiments/"
        "integrated_detector_summary.csv",
        index=False
    )

    print()
    print("Results saved:")

    print(
        "1. experiments/"
        "integrated_detector_results.csv"
    )

    print(
        "2. experiments/"
        "integrated_detector_summary.csv"
    )

    print()
    print("=" * 100)
    print("PHASE 5E COMPLETED")
    print("=" * 100)


if __name__ == "__main__":
    main()