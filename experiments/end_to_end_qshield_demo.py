from qshield.quantum.teleportation import TeleportationEngine
from qshield.detection.integrated_detector import (
    IntegratedQShieldDetector
)

import pandas as pd


print("=" * 100)
print("Q-SHIELD")
print("PHASE 7A: END-TO-END QUANTUM SECURITY DEMONSTRATION")
print("=" * 100)


# ============================================================
# CONFIGURATION
# ============================================================

SHOTS = 1024

engine = TeleportationEngine(
    shots=SHOTS
)

detector = IntegratedQShieldDetector(
    mismatch_weight=0.7,
    bell_weight=0.3,
    base_threshold=0.26,
    adaptation_factor=0.4,
    max_threshold=0.32
)


# ============================================================
# DEMONSTRATION SCENARIOS
# ============================================================

scenarios = [

    {
        "name": "Normal Quantum Communication",
        "bit": 0,
        "basis": "Z",
        "noise_type": "none",
        "noise_probability": 0.0,
        "attack_type": "none"
    },

    {
        "name": "Noisy Legitimate Channel",
        "bit": 0,
        "basis": "Z",
        "noise_type": "depolarizing",
        "noise_probability": 0.10,
        "attack_type": "none"
    },

    {
        "name": "Pauli-X Attack",
        "bit": 0,
        "basis": "Z",
        "noise_type": "none",
        "noise_probability": 0.0,
        "attack_type": "pauli_x"
    },

    {
        "name": "Pauli-Y Attack",
        "bit": 0,
        "basis": "Z",
        "noise_type": "none",
        "noise_probability": 0.0,
        "attack_type": "pauli_y"
    },

    {
        "name": "Pauli-Z Attack",
        "bit": 0,
        "basis": "X",
        "noise_type": "none",
        "noise_probability": 0.0,
        "attack_type": "pauli_z"
    },

    {
        "name": "Entanglement Disruption Attack",
        "bit": 1,
        "basis": "Z",
        "noise_type": "none",
        "noise_probability": 0.0,
        "attack_type": "entanglement_disruption"
    }

]


# ============================================================
# RUN END-TO-END PIPELINE
# ============================================================

results = []

print("\n")
print("=" * 100)
print("RUNNING Q-SHIELD SECURITY PIPELINE")
print("=" * 100)


for index, scenario in enumerate(scenarios, start=1):

    print("\n" + "-" * 100)

    print(
        f"SCENARIO {index}: "
        f"{scenario['name']}"
    )

    print("-" * 100)

    # --------------------------------------------------------
    # STEP 1: QUANTUM TELEPORTATION
    # --------------------------------------------------------

    quantum_result = engine.run(

        bit=scenario["bit"],

        basis=scenario["basis"],

        noise_type=scenario["noise_type"],

        noise_probability=
        scenario["noise_probability"],

        attack_type=
        scenario["attack_type"]
    )


    # --------------------------------------------------------
    # STEP 2: EXTRACT QUANTUM SECURITY SIGNALS
    # --------------------------------------------------------

    mismatch_rate = (
        quantum_result["mismatch_rate"]
    )

    bell_measurements = (
        quantum_result["bell_measurements"]
    )


    # --------------------------------------------------------
    # STEP 3: Q-SHIELD SECURITY ANALYSIS
    # --------------------------------------------------------

    security_result = detector.analyze(

        mismatch_rate=mismatch_rate,

        bell_measurements=
        bell_measurements
    )


    # --------------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------------

    print(
        f"Expected State: "
        f"{quantum_result['expected_state']}"
    )

    print(
        f"Noise Model: "
        f"{scenario['noise_type']}"
    )

    print(
        f"Noise Probability: "
        f"{scenario['noise_probability']}"
    )

    print(
        f"Attack Type: "
        f"{scenario['attack_type']}"
    )

    print()

    print(
        f"Mismatch Rate: "
        f"{mismatch_rate:.4f}"
    )

    print(
        f"Bell Anomaly Score: "
        f"{security_result['bell_anomaly_score']:.4f}"
    )

    print(
        f"Security Score: "
        f"{security_result['security_score']:.4f}"
    )

    print(
        f"Adaptive Threshold: "
        f"{security_result['adaptive_threshold']:.4f}"
    )

    print(
        f"Decision Margin: "
        f"{security_result['decision_margin']:.4f}"
    )

    print()

    print(
        f"FINAL DECISION: "
        f"{security_result['decision']}"
    )

    print(
        f"SECURITY SEVERITY: "
        f"{security_result['severity']}"
    )


    # --------------------------------------------------------
    # STORE RESULTS
    # --------------------------------------------------------

    results.append({

        "scenario":
        scenario["name"],

        "attack_type":
        scenario["attack_type"],

        "noise_type":
        scenario["noise_type"],

        "noise_probability":
        scenario["noise_probability"],

        "mismatch_rate":
        mismatch_rate,

        "bell_anomaly_score":
        security_result[
            "bell_anomaly_score"
        ],

        "security_score":
        security_result[
            "security_score"
        ],

        "adaptive_threshold":
        security_result[
            "adaptive_threshold"
        ],

        "decision_margin":
        security_result[
            "decision_margin"
        ],

        "decision":
        security_result[
            "decision"
        ],

        "attack_detected":
        security_result[
            "attack_detected"
        ],

        "severity":
        security_result[
            "severity"
        ]
    })


# ============================================================
# FINAL SUMMARY
# ============================================================

df = pd.DataFrame(results)

print("\n")
print("=" * 100)
print("FINAL Q-SHIELD END-TO-END SECURITY SUMMARY")
print("=" * 100)

print(
    df[
        [
            "scenario",
            "attack_type",
            "mismatch_rate",
            "bell_anomaly_score",
            "security_score",
            "adaptive_threshold",
            "decision",
            "severity"
        ]
    ].to_string(
        index=False
    )
)


# ============================================================
# SAVE RESULTS
# ============================================================

output_file = (
    "experiments/"
    "qshield_end_to_end_demo_results.csv"
)

df.to_csv(
    output_file,
    index=False
)


# ============================================================
# DETECTION STATISTICS
# ============================================================

total_scenarios = len(df)

attacks_detected = len(
    df[
        df["decision"] == "ATTACK"
    ]
)

normal_detected = len(
    df[
        df["decision"] == "NORMAL"
    ]
)


print("\n")
print("=" * 100)
print("DEMONSTRATION STATISTICS")
print("=" * 100)

print(
    f"Total Scenarios: {total_scenarios}"
)

print(
    f"Attacks Detected: {attacks_detected}"
)

print(
    f"Normal Decisions: {normal_detected}"
)


print("\n")
print("=" * 100)
print("GENERATED FILE")
print("=" * 100)

print(
    "experiments/qshield_end_to_end_demo_results.csv"
)


print("\n")
print("=" * 100)
print("PHASE 7A COMPLETED")
print("Q-SHIELD END-TO-END PIPELINE VALIDATED")
print("=" * 100)