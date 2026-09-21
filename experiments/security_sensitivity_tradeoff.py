import pandas as pd
import matplotlib.pyplot as plt

from qshield.quantum.teleportation import TeleportationEngine
from qshield.detection.dual_signal_detector import DualSignalDetector


# ============================================================
# CONFIGURATION
# ============================================================

SHOTS = 1024
TRIALS = 20

MISMATCH_WEIGHT = 0.7
BELL_WEIGHT = 0.3

THRESHOLDS = [
    0.20,
    0.25,
    0.30,
    0.32,
    0.35,
    0.40
]

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
# SINGLE THRESHOLD EXPERIMENT
# ============================================================

def run_experiment(detection_threshold):

    engine = TeleportationEngine(
        shots=SHOTS
    )

    detector = DualSignalDetector(
        mismatch_weight=MISMATCH_WEIGHT,
        bell_weight=BELL_WEIGHT,
        detection_threshold=detection_threshold
    )

    tp = 0
    fp = 0
    tn = 0
    fn = 0

    # --------------------------------------------------------
    # NORMAL CHANNEL EVALUATION
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # ATTACK CHANNEL EVALUATION
    # --------------------------------------------------------

    for attack_type in ATTACK_TYPES:

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
            else:
                fn += 1

    metrics = calculate_metrics(
        tp,
        fp,
        tn,
        fn
    )

    metrics[
        "detection_threshold"
    ] = detection_threshold

    metrics["tp"] = tp
    metrics["fp"] = fp
    metrics["tn"] = tn
    metrics["fn"] = fn

    return metrics


# ============================================================
# MAIN EXPERIMENT
# ============================================================

def main():

    print("=" * 100)
    print("Q-SHIELD")
    print(
        "PHASE 5F: SECURITY-SENSITIVITY "
        "TRADE-OFF ANALYSIS"
    )
    print("=" * 100)

    print()
    print(f"Quantum Shots: {SHOTS}")
    print(f"Trials per Scenario: {TRIALS}")
    print(
        f"Mismatch Signal Weight: "
        f"{MISMATCH_WEIGHT}"
    )
    print(
        f"Bell Signal Weight: "
        f"{BELL_WEIGHT}"
    )

    print()

    results = []

    # ========================================================
    # THRESHOLD SWEEP
    # ========================================================

    for threshold in THRESHOLDS:

        print("-" * 100)

        print(
            f"Testing Detection Threshold: "
            f"{threshold:.2f}"
        )

        metrics = run_experiment(
            threshold
        )

        results.append(metrics)

        print(
            f"Accuracy={metrics['accuracy']:.4f} | "
            f"Precision={metrics['precision']:.4f} | "
            f"Recall={metrics['recall']:.4f} | "
            f"F1={metrics['f1_score']:.4f} | "
            f"FPR={metrics['fpr']:.4f}"
        )

    # ========================================================
    # DATAFRAME
    # ========================================================

    df = pd.DataFrame(results)

    df = df[
        [
            "detection_threshold",
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
        "experiments/security_sensitivity_tradeoff.csv",
        index=False
    )

    # ========================================================
    # PRINT RESULTS
    # ========================================================

    print()
    print("=" * 100)
    print(
        "SECURITY-SENSITIVITY TRADE-OFF RESULTS"
    )
    print("=" * 100)

    print()

    print(
        df.to_string(
            index=False
        )
    )

    # ========================================================
    # GRAPH 1
    # RECALL VS FALSE POSITIVE RATE
    # ========================================================

    plt.figure(
        figsize=(9, 6)
    )

    plt.plot(
        df["fpr"],
        df["recall"],
        marker="o"
    )

    for _, row in df.iterrows():

        plt.annotate(
            f'{row["detection_threshold"]:.2f}',
            (
                row["fpr"],
                row["recall"]
            ),
            xytext=(5, 5),
            textcoords="offset points"
        )

    plt.xlabel(
        "False Positive Rate"
    )

    plt.ylabel(
        "Attack Detection Recall"
    )

    plt.title(
        "Q-SHIELD Security-Sensitivity Trade-off"
    )

    plt.grid()

    plt.tight_layout()

    plt.savefig(
        "experiments/"
        "security_sensitivity_tradeoff.png",
        dpi=300
    )

    plt.close()

    # ========================================================
    # GRAPH 2
    # PERFORMANCE VS THRESHOLD
    # ========================================================

    plt.figure(
        figsize=(10, 6)
    )

    plt.plot(
        df["detection_threshold"],
        df["accuracy"],
        marker="o",
        label="Accuracy"
    )

    plt.plot(
        df["detection_threshold"],
        df["precision"],
        marker="o",
        label="Precision"
    )

    plt.plot(
        df["detection_threshold"],
        df["recall"],
        marker="o",
        label="Recall"
    )

    plt.plot(
        df["detection_threshold"],
        df["f1_score"],
        marker="o",
        label="F1 Score"
    )

    plt.xlabel(
        "Detection Threshold"
    )

    plt.ylabel(
        "Performance Score"
    )

    plt.title(
        "Q-SHIELD Performance vs Detection Threshold"
    )

    plt.legend()

    plt.grid()

    plt.tight_layout()

    plt.savefig(
        "experiments/"
        "threshold_sensitivity_performance.png",
        dpi=300
    )

    plt.close()

    # ========================================================
    # GRAPH 3
    # FPR AND FNR TRADE-OFF
    # ========================================================

    plt.figure(
        figsize=(9, 6)
    )

    plt.plot(
        df["detection_threshold"],
        df["fpr"],
        marker="o",
        label="False Positive Rate"
    )

    plt.plot(
        df["detection_threshold"],
        df["fnr"],
        marker="o",
        label="False Negative Rate"
    )

    plt.xlabel(
        "Detection Threshold"
    )

    plt.ylabel(
        "Error Rate"
    )

    plt.title(
        "False Positive vs False Negative Trade-off"
    )

    plt.legend()

    plt.grid()

    plt.tight_layout()

    plt.savefig(
        "experiments/"
        "fpr_fnr_tradeoff.png",
        dpi=300
    )

    plt.close()

    # ========================================================
    # BEST BALANCED CONFIGURATION
    # ========================================================

    best = df.loc[
        df["f1_score"].idxmax()
    ]

    print()
    print("=" * 100)
    print(
        "BEST BALANCED CONFIGURATION"
    )
    print("=" * 100)

    print()

    print(
        f"Detection Threshold: "
        f"{best['detection_threshold']:.2f}"
    )

    print(
        f"Accuracy: "
        f"{best['accuracy']:.4f}"
    )

    print(
        f"Precision: "
        f"{best['precision']:.4f}"
    )

    print(
        f"Recall: "
        f"{best['recall']:.4f}"
    )

    print(
        f"F1 Score: "
        f"{best['f1_score']:.4f}"
    )

    print(
        f"False Positive Rate: "
        f"{best['fpr']:.4f}"
    )

    print(
        f"False Negative Rate: "
        f"{best['fnr']:.4f}"
    )

    print()

    print("=" * 100)
    print(
        "GENERATED FILES"
    )
    print("=" * 100)

    print(
        "1. experiments/"
        "security_sensitivity_tradeoff.csv"
    )

    print(
        "2. experiments/"
        "security_sensitivity_tradeoff.png"
    )

    print(
        "3. experiments/"
        "threshold_sensitivity_performance.png"
    )

    print(
        "4. experiments/"
        "fpr_fnr_tradeoff.png"
    )

    print()

    print("=" * 100)
    print(
        "PHASE 5F COMPLETED"
    )
    print("=" * 100)


if __name__ == "__main__":
    main()