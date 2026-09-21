from qshield.quantum.teleportation import TeleportationEngine
from qshield.security.threat_detector import QuantumThreatDetector


def run_quantum_probes(
    engine,
    noise_type="none",
    noise_probability=0.0,
    attack_type="none"
):
    """
    Run probes across multiple measurement bases.
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


def run_experiment():

    print()
    print("=" * 90)
    print("Q-SHIELD")
    print("PHASE 4E: THRESHOLD SENSITIVITY ANALYSIS")
    print("=" * 90)

    engine = TeleportationEngine(
        shots=1024
    )

    thresholds = [
        0.10,
        0.15,
        0.20,
        0.25,
        0.30,
        0.35
    ]

    scenarios = [

        {
            "name": "Clean_Channel",
            "noise_type": "none",
            "noise_probability": 0.0,
            "attack_type": "none",
            "expected": "NORMAL"
        },

        {
            "name": "Low_Noise",
            "noise_type": "bit_flip",
            "noise_probability": 0.03,
            "attack_type": "none",
            "expected": "NORMAL"
        },

        {
            "name": "Moderate_Noise",
            "noise_type": "bit_flip",
            "noise_probability": 0.10,
            "attack_type": "none",
            "expected": "NORMAL"
        },

        {
            "name": "High_Noise",
            "noise_type": "bit_flip",
            "noise_probability": 0.20,
            "attack_type": "none",
            "expected": "NORMAL"
        },

        {
            "name": "Pauli_X_Attack",
            "noise_type": "none",
            "noise_probability": 0.0,
            "attack_type": "pauli_x",
            "expected": "ATTACK"
        },

        {
            "name": "Pauli_Y_Attack",
            "noise_type": "none",
            "noise_probability": 0.0,
            "attack_type": "pauli_y",
            "expected": "ATTACK"
        },

        {
            "name": "Pauli_Z_Attack",
            "noise_type": "none",
            "noise_probability": 0.0,
            "attack_type": "pauli_z",
            "expected": "ATTACK"
        },

        {
            "name": "Entanglement_Disruption",
            "noise_type": "none",
            "noise_probability": 0.0,
            "attack_type": "entanglement_disruption",
            "expected": "ATTACK"
        }
    ]

    print()
    print(
        f"{'Threshold':<12}"
        f"{'Detection Rate':<20}"
        f"{'False Positive Rate':<25}"
        f"{'Attack Detected':<20}"
        f"{'Normal Rejected':<20}"
    )

    print("-" * 90)

    experiment_results = []

    for threshold in thresholds:

        detector = QuantumThreatDetector(
            warn_threshold=0.05,
            reject_threshold=threshold
        )

        attack_total = 0
        attack_detected = 0

        normal_total = 0
        normal_rejected = 0

        for scenario in scenarios:

            probes = run_quantum_probes(
                engine,
                noise_type=scenario["noise_type"],
                noise_probability=scenario[
                    "noise_probability"
                ],
                attack_type=scenario["attack_type"]
            )

            analysis = detector.analyze(
                probes
            )

            decision = analysis["decision"]

            if scenario["expected"] == "ATTACK":

                attack_total += 1

                if decision == "REJECT":
                    attack_detected += 1

            else:

                normal_total += 1

                if decision == "REJECT":
                    normal_rejected += 1

        detection_rate = (
            attack_detected / attack_total
        ) * 100

        false_positive_rate = (
            normal_rejected / normal_total
        ) * 100

        print(
            f"{threshold:<12.2f}"
            f"{detection_rate:<20.2f}"
            f"{false_positive_rate:<25.2f}"
            f"{attack_detected}/{attack_total:<18}"
            f"{normal_rejected}/{normal_total:<20}"
        )

        experiment_results.append({
            "threshold": threshold,
            "detection_rate": detection_rate,
            "false_positive_rate": false_positive_rate,
            "attack_detected": attack_detected,
            "normal_rejected": normal_rejected
        })

    print("=" * 90)
    print("PHASE 4E COMPLETED")
    print("=" * 90)

    return experiment_results


if __name__ == "__main__":
    run_experiment()