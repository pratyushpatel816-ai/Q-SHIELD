import pandas as pd
import matplotlib.pyplot as plt

from qshield.quantum.teleportation import TeleportationEngine
from qshield.detection.dual_signal_detector import DualSignalDetector


# ============================================================
# CONFIGURATION
# ============================================================

SHOTS = 1024
TRIALS = 20

DETECTION_THRESHOLD = 0.25

NOISE_TYPES = [
    "bit_flip",
    "phase_flip",
    "depolarizing",
    "readout"
]

NOISE_LEVELS = [
    0.00,
    0.05,
    0.10,
    0.15,
    0.20
]

ATTACK_TYPES = [
    "pauli_x",
    "pauli_y",
    "pauli_z",
    "entanglement_disruption"
]


# ============================================================
# METRIC CALCULATION
# ============================================================

def calculate_metrics(tp, fp, tn, fn):

    total = tp + fp + tn + fn

    accuracy = (
        (tp + tn) / total
        if total > 0
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

    fnr = (
        fn / (fn + tp)
        if (fn + tp) > 0
        else 0
    )

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
        "fpr": fpr,
        "fnr": fnr
    }


# ============================================================
# EVALUATE SINGLE CONFIGURATION
# ============================================================

def evaluate_detector(
    method_name,
    mismatch_weight,
    bell_weight
):

    engine = TeleportationEngine(
        shots=SHOTS
    )

    detector = DualSignalDetector(
        mismatch_weight=mismatch_weight,
        bell_weight=bell_weight,
        detection_threshold=DETECTION_THRESHOLD
    )

    tp = 0
    fp = 0
    tn = 0
    fn = 0

    print()
    print("-" * 100)
    print(
        f"Evaluating: {method_name}"
    )
    print(
        f"Mismatch Weight: {mismatch_weight}"
    )
    print(
        f"Bell Weight: {bell_weight}"
    )
    print("-" * 100)

    # ========================================================
    # NORMAL CHANNEL
    # ========================================================

    for noise_type in NOISE_TYPES:

        for noise_probability in NOISE_LEVELS:

            for _ in range(TRIALS):

                result = engine.run(
                    bit=0,
                    basis="Z",
                    noise_type=noise_type,
                    noise_probability=noise_probability,
                    attack_type="none"
                )

                decision = detector.detect(
                    mismatch_rate=result[
                        "mismatch_rate"
                    ],
                    bell_measurements=result[
                        "bell_measurements"
                    ]
                )

                if decision["attack_detected"]:
                    fp += 1
                else:
                    tn += 1

    # ========================================================
    # ATTACK CHANNEL
    # ========================================================

    for attack_type in ATTACK_TYPES:

        detected = 0

        for _ in range(TRIALS):

            result = engine.run(
                bit=0,
                basis="Z",
                noise_type="bit_flip",
                noise_probability=0.10,
                attack_type=attack_type
            )

            decision = detector.detect(
                mismatch_rate=result[
                    "mismatch_rate"
                ],
                bell_measurements=result[
                    "bell_measurements"
                ]
            )

            if decision["attack_detected"]:

                tp += 1
                detected += 1

            else:
                fn += 1

        print(
            f"{attack_type:<30} "
            f"Detected={detected}/{TRIALS}"
        )

    metrics = calculate_metrics(
        tp,
        fp,
        tn,
        fn
    )

    metrics["method"] = method_name
    metrics["mismatch_weight"] = mismatch_weight
    metrics["bell_weight"] = bell_weight

    metrics["tp"] = tp
    metrics["fp"] = fp
    metrics["tn"] = tn
    metrics["fn"] = fn

    print()

    print(
        f"Accuracy={metrics['accuracy']:.4f} | "
        f"Precision={metrics['precision']:.4f} | "
        f"Recall={metrics['recall']:.4f} | "
        f"F1={metrics['f1_score']:.4f} | "
        f"FPR={metrics['fpr']:.4f}"
    )

    return metrics


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 100)
    print("Q-SHIELD")
    print(
        "PHASE 5G: DUAL-SIGNAL DETECTOR "
        "ABLATION STUDY"
    )
    print("=" * 100)

    print()
    print(
        f"Quantum Shots: {SHOTS}"
    )
    print(
        f"Trials per Scenario: {TRIALS}"
    )
    print(
        f"Detection Threshold: "
        f"{DETECTION_THRESHOLD}"
    )

    results = []

    # ========================================================
    # CONFIGURATION 1
    # MISMATCH ONLY
    # ========================================================

    results.append(

        evaluate_detector(
            method_name="Mismatch Only",
            mismatch_weight=1.0,
            bell_weight=0.0
        )
    )

    # ========================================================
    # CONFIGURATION 2
    # BELL ONLY
    # ========================================================

    results.append(

        evaluate_detector(
            method_name="Bell Anomaly Only",
            mismatch_weight=0.0,
            bell_weight=1.0
        )
    )

    # ========================================================
    # CONFIGURATION 3
    # DUAL SIGNAL
    # ========================================================

    results.append(

        evaluate_detector(
            method_name="Q-SHIELD Dual Signal",
            mismatch_weight=0.7,
            bell_weight=0.3
        )
    )

    # ========================================================
    # RESULTS
    # ========================================================

    df = pd.DataFrame(
        results
    )

    df = df[
        [
            "method",
            "mismatch_weight",
            "bell_weight",
            "accuracy",
            "precision",
            "recall",
            "f1_score",
            "fpr",
            "fnr",
            "tp",
            "fp",
            "tn",
            "fn"
        ]
    ]

    df.to_csv(
        "experiments/dual_signal_ablation_results.csv",
        index=False
    )

    print()
    print("=" * 100)
    print(
        "DUAL-SIGNAL ABLATION RESULTS"
    )
    print("=" * 100)

    print()

    print(
        df.to_string(
            index=False
        )
    )

    # ========================================================
    # VISUALIZATION
    # ========================================================

    metrics = [
        "accuracy",
        "precision",
        "recall",
        "f1_score"
    ]

    x = range(len(df))

    plt.figure(
        figsize=(11, 6)
    )

    width = 0.18

    for index, metric in enumerate(metrics):

        positions = [
            value + index * width
            for value in x
        ]

        plt.bar(
            positions,
            df[metric],
            width=width,
            label=metric.upper()
        )

    center_positions = [
        value + width * 1.5
        for value in x
    ]

    plt.xticks(
        center_positions,
        df["method"],
        rotation=10
    )

    plt.ylabel(
        "Performance Score"
    )

    plt.title(
        "Q-SHIELD Dual-Signal Ablation Study"
    )

    plt.legend()

    plt.grid(
        axis="y"
    )

    plt.tight_layout()

    plt.savefig(
        "experiments/"
        "dual_signal_ablation.png",
        dpi=300
    )

    plt.close()

    # ========================================================
    # FPR COMPARISON
    # ========================================================

    plt.figure(
        figsize=(8, 6)
    )

    plt.bar(
        df["method"],
        df["fpr"]
    )

    plt.ylabel(
        "False Positive Rate"
    )

    plt.title(
        "False Positive Rate Across Detector Variants"
    )

    plt.xticks(
        rotation=10
    )

    plt.grid(
        axis="y"
    )

    plt.tight_layout()

    plt.savefig(
        "experiments/"
        "dual_signal_fpr_comparison.png",
        dpi=300
    )

    plt.close()

    print()

    print("=" * 100)
    print(
        "GENERATED FILES"
    )
    print("=" * 100)

    print(
        "1. experiments/"
        "dual_signal_ablation_results.csv"
    )

    print(
        "2. experiments/"
        "dual_signal_ablation.png"
    )

    print(
        "3. experiments/"
        "dual_signal_fpr_comparison.png"
    )

    print()

    print("=" * 100)
    print(
        "PHASE 5G COMPLETED"
    )
    print("=" * 100)


if __name__ == "__main__":
    main()