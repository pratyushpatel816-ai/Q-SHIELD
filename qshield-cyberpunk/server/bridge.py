
import json
import sys
from datetime import datetime
from pathlib import Path

# Add the Q-SHIELD project root to Python's module search path.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from qshield.quantum.teleportation import TeleportationEngine
from qshield.detection.integrated_detector import IntegratedQShieldDetector
from qds.qds_protocol import QDSProtocol
from qds.qds_attack_simulator import QDSAttackSimulator


def run_qds(message, qds_attack, verifier_id):
    protocol = QDSProtocol()

    signature = protocol.generate_signature(
        message=message,
        signer_id="ALICE",
        authorized_verifiers=["BOB"],
    )

    attacked_signature, attack_metadata = (
        QDSAttackSimulator.apply_attack(
            signature,
            attack_type=qds_attack,
        )
    )

    if qds_attack == "replay":
        first = protocol.verify_signature(
            attacked_signature,
            verifier_id="BOB",
        )

        second = protocol.verify_signature(
            attacked_signature,
            verifier_id="BOB",
        )

        return {
            "signature": attacked_signature,
            "attack_metadata": attack_metadata,
            "verification": second,
            "first_verification": first,
            "second_verification": second,
        }

    verification = protocol.verify_signature(
        attacked_signature,
        verifier_id=verifier_id,
    )

    return {
        "signature": attacked_signature,
        "attack_metadata": attack_metadata,
        "verification": verification,
        "first_verification": None,
        "second_verification": None,
    }


def run_quantum(
    shots,
    bit,
    basis,
    noise_type,
    noise_probability,
    quantum_attack,
    seed=None,
):
    engine = TeleportationEngine(shots=shots)

    quantum = engine.run(
        bit=bit,
        basis=basis,
        noise_type=noise_type,
        noise_probability=noise_probability,
        attack_type=quantum_attack,
        seed=seed,
    )

    detector = IntegratedQShieldDetector(
        mismatch_weight=0.7,
        bell_weight=0.3,
        base_threshold=0.26,
        adaptation_factor=0.4,
        max_threshold=0.32,
    )

    shield = detector.analyze(
        mismatch_rate=quantum["mismatch_rate"],
        bell_measurements=quantum["bell_measurements"],
    )

    return quantum, shield


def main():
    request = json.loads(sys.stdin.read() or "{}")

    message = request.get(
        "message",
        "INSTALL_FIRMWARE",
    )

    qds_attack = request.get(
        "qds_attack",
        "none",
    )

    quantum_attack = request.get(
        "quantum_attack",
        "none",
    )

    verifier_id = request.get(
        "verifier_id",
        "BOB",
    )

    shots = int(
        request.get(
            "shots",
            1024,
        )
    )

    bit = int(
        request.get(
            "bit",
            0,
        )
    )

    basis = request.get(
        "basis",
        "Z",
    )

    noise_type = request.get(
        "noise_type",
        "none",
    )

    noise_probability = float(
        request.get(
            "noise_probability",
            0.0,
        )
    )

    seed_value = request.get("seed")

    seed = (
        int(seed_value)
        if seed_value is not None
        else None
    )

    qds = run_qds(
        message,
        qds_attack,
        verifier_id,
    )

    quantum, shield = run_quantum(
        shots=shots,
        bit=bit,
        basis=basis,
        noise_type=noise_type,
        noise_probability=noise_probability,
        quantum_attack=quantum_attack,
        seed=seed,
    )

    qds_threat = (
        qds["verification"]["final_decision"]
        == "REJECT"
    )

    quantum_threat = shield["attack_detected"]

    overall = qds_threat or quantum_threat

    print(
        json.dumps(
            {
                "timestamp": datetime.now().isoformat(
                    timespec="seconds"
                ),
                "final_decision": (
                    "SECURITY THREAT DETECTED"
                    if overall
                    else "SECURE COMMUNICATION"
                ),
                "qds_threat": qds_threat,
                "quantum_threat": quantum_threat,
                "qds": qds,
                "quantum": quantum,
                "qshield": shield,
            },
            default=str,
        )
    )


if __name__ == "__main__":
    main()