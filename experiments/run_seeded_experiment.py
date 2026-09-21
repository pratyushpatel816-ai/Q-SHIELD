
import csv
import random
import sys
from datetime import datetime
from pathlib import Path

# Project root: C:\Users\USER\qshield
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from qshield.quantum.teleportation import TeleportationEngine
from qshield.detection.integrated_detector import (
    IntegratedQShieldDetector,
)


# -----------------------------
# Experiment configuration
# -----------------------------

SHOTS = 1024
BIT = 0
BASIS = "X"
NOISE_TYPE = "depolarizing"
NOISE_PROBABILITY = 0.30

TRIALS_PER_CONDITION = 100

# Master seed controls generation of trial seeds.
MASTER_SEED = 20260917

OUTPUT_DIR = PROJECT_ROOT / "experiments" / "results"


def create_detector():
    """
    Create a fresh detector for each trial.
    """
    return IntegratedQShieldDetector(
        mismatch_weight=0.7,
        bell_weight=0.3,
        base_threshold=0.26,
        adaptation_factor=0.4,
        max_threshold=0.32,
    )


def run_single_trial(
    condition,
    trial,
    seed,
    quantum_attack,
):
    """
    Execute one reproducible quantum simulation trial.
    """

    engine = TeleportationEngine(shots=SHOTS)

    quantum = engine.run(
        bit=BIT,
        basis=BASIS,
        noise_type=NOISE_TYPE,
        noise_probability=NOISE_PROBABILITY,
        attack_type=quantum_attack,
        seed=seed,
    )

    detector = create_detector()

    shield = detector.analyze(
        mismatch_rate=quantum["mismatch_rate"],
        bell_measurements=quantum["bell_measurements"],
    )

    expected_attack = quantum_attack != "none"
    detected_attack = bool(shield["attack_detected"])

    true_positive = expected_attack and detected_attack
    false_negative = expected_attack and not detected_attack
    true_negative = not expected_attack and not detected_attack
    false_positive = not expected_attack and detected_attack

    return {
        "Timestamp": datetime.now().isoformat(timespec="seconds"),
        "Condition": condition,
        "Trial": trial,
        "Seed": seed,
        "Shots": SHOTS,
        "Bit": BIT,
        "Basis": BASIS,
        "NoiseType": NOISE_TYPE,
        "NoiseProbability": NOISE_PROBABILITY,
        "QuantumAttack": quantum_attack,
        "MismatchRate": quantum["mismatch_rate"],
        "SecurityScore": shield["security_score"],
        "AdaptiveThreshold": shield["adaptive_threshold"],
        "BellAnomalyScore": shield["bell_anomaly_score"],
        "Decision": shield["decision"],
        "AttackDetected": detected_attack,
        "ExpectedAttack": expected_attack,
        "TP": int(true_positive),
        "FN": int(false_negative),
        "TN": int(true_negative),
        "FP": int(false_positive),
    }


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = (
        OUTPUT_DIR
        / "qshield_seeded_experiment_200_trials.csv"
    )

    # Deterministically generate 200 unique trial seeds.
    seed_generator = random.Random(MASTER_SEED)

    seeds = set()

    while len(seeds) < 2 * TRIALS_PER_CONDITION:
        seeds.add(
            seed_generator.randint(1, 2_147_483_646)
        )

    seeds = list(seeds)

    rows = []

    conditions = [
        {
            "name": "noise_only",
            "quantum_attack": "none",
        },
        {
            "name": "pauli_z_attack",
            "quantum_attack": "pauli_z",
        },
    ]

    seed_index = 0

    for condition_config in conditions:
        condition_name = condition_config["name"]
        quantum_attack = condition_config["quantum_attack"]

        print(
            f"\nRunning condition: {condition_name}"
        )

        for trial in range(1, TRIALS_PER_CONDITION + 1):
            seed = seeds[seed_index]
            seed_index += 1

            row = run_single_trial(
                condition=condition_name,
                trial=trial,
                seed=seed,
                quantum_attack=quantum_attack,
            )

            rows.append(row)

            print(
                f"{condition_name}: "
                f"trial {trial}/{TRIALS_PER_CONDITION} | "
                f"seed={seed} | "
                f"mismatch={row['MismatchRate']:.6f} | "
                f"decision={row['Decision']}"
            )

    fieldnames = list(rows[0].keys())

    with output_file.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(rows)

    print("\nExperiment completed.")
    print(f"Total trials: {len(rows)}")
    print(f"Output file: {output_file}")


if __name__ == "__main__":
    main()