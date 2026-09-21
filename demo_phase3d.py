from datetime import datetime, timezone, timedelta
import uuid

from qshield.protocol.signature import SignatureGenerator
from qshield.protocol.verifier import SignatureVerifier

from qshield.security.identity import IdentityRegistry
from qshield.security.authorization import AuthorizationManager
from qshield.security.replay import ReplayRegistry

from qshield.security.security_engine import (
    QShieldSecurityEngine
)


def create_payload():

    now = datetime.now(
        timezone.utc
    )

    return {
        "sender_id": "CITY_CONTROL_CENTER",
        "receiver_id": "TRAFFIC_GATEWAY_01",
        "device_id": "SMART_TRAFFIC_GATEWAY_01",
        "command": "AUTHORIZE_FIRMWARE_UPDATE",
        "firmware_hash": "abc123firmwarehashxyz",
        "nonce": str(uuid.uuid4()),
        "session_id": str(uuid.uuid4()),
        "timestamp": now.isoformat(),
        "expiry": (
            now + timedelta(minutes=10)
        ).isoformat(),
        "sequence_no": 1
    }


def build_engine():

    identity_registry = IdentityRegistry()

    authorization_manager = (
        AuthorizationManager()
    )

    authorization_manager.register_user(
        user_id="TRAFFIC_GATEWAY_01",
        role="VERIFIER"
    )

    return QShieldSecurityEngine(

        signature_verifier=SignatureVerifier(
            shots=256
        ),

        identity_registry=identity_registry,

        authorization_manager=(
            authorization_manager
        ),

        replay_registry=ReplayRegistry(),

        shots=256
    )

    # -----------------------------------------
    # IDENTITY REGISTRATION
    # -----------------------------------------

    identity_registry = IdentityRegistry()

    identity_registry.register(
        "CITY_CONTROL_CENTER"
    )

    # -----------------------------------------
    # VERIFIER AUTHORIZATION
    # -----------------------------------------

    authorization_manager = (
        AuthorizationManager()
    )

    authorization_manager.register(
        verifier_id="TRAFFIC_GATEWAY_01",
        role="VERIFIER"
    )

    # -----------------------------------------
    # BUILD UNIFIED ENGINE
    # -----------------------------------------

    return QShieldSecurityEngine(

        signature_verifier=SignatureVerifier(
            shots=256
        ),

        identity_registry=identity_registry,

        authorization_manager=(
            authorization_manager
        ),

        replay_registry=ReplayRegistry(),

        shots=256
    )


def print_result(
    title,
    result
):

    print("\n" + "=" * 75)

    print(title)

    print("-" * 75)

    print(
        "Decision:",
        result["decision"]
    )

    print(
        "Severity:",
        result["severity"]
    )

    print(
        "Rule ID:",
        result["rule_id"]
    )

    print(
        "Stage:",
        result["failed_stage"]
    )

    print(
        "Reason:",
        result["reason"]
    )

    if "evidence" in result:

        print(
            "Evidence:",
            result["evidence"]
        )

    if (
        "quantum_threat_analysis"
        in result
    ):

        quantum = result[
            "quantum_threat_analysis"
        ]

        print(
            "\nQuantum Analysis:"
        )

        print(
            "Quantum Decision:",
            quantum.get("decision")
        )

        print(
            "Quantum Severity:",
            quantum.get("severity")
        )

        print(
            "Quantum Rule:",
            quantum.get("rule_id")
        )


def run_demo():

    print("\n" + "=" * 75)

    print("Q-SHIELD")

    print(
        "PHASE 3D: UNIFIED END-TO-END SECURITY ENGINE"
    )

    print("=" * 75)

    generator = SignatureGenerator(
        shots=256
    )

    # =================================================
    # SCENARIO 1
    # LEGITIMATE COMMUNICATION
    # =================================================

    payload = create_payload()

    signature = generator.generate(
        payload,
        signature_length=16
    )

    engine = build_engine()

    result = engine.secure_verify(
        payload=payload,
        signature=signature,
        verifier_id="TRAFFIC_GATEWAY_01",
        attack_type="none"
    )

    print_result(
        "[1] LEGITIMATE COMMUNICATION",
        result
    )

    # =================================================
    # SCENARIO 2
    # QUANTUM PAULI-X ATTACK
    # =================================================

    payload = create_payload()

    signature = generator.generate(
        payload,
        signature_length=16
    )

    engine = build_engine()

    result = engine.secure_verify(
        payload=payload,
        signature=signature,
        verifier_id="TRAFFIC_GATEWAY_01",
        attack_type="pauli_x"
    )

    print_result(
        "[2] QUANTUM PAULI-X ATTACK",
        result
    )

    # =================================================
    # SCENARIO 3
    # MESSAGE TAMPERING
    # =================================================

    payload = create_payload()

    signature = generator.generate(
        payload,
        signature_length=16
    )

    tampered_payload = payload.copy()

    tampered_payload[
        "command"
    ] = "MALICIOUS_COMMAND"

    engine = build_engine()

    result = engine.secure_verify(
        payload=tampered_payload,
        signature=signature,
        verifier_id="TRAFFIC_GATEWAY_01",
        attack_type="none"
    )

    print_result(
        "[3] MESSAGE TAMPERING",
        result
    )

    # =================================================
    # SCENARIO 4
    # IDENTITY IMPERSONATION
    # =================================================

    payload = create_payload()

    signature = generator.generate(
        payload,
        signature_length=16
    )

    payload[
        "sender_id"
    ] = "FAKE_CITY_CONTROL"

    engine = build_engine()

    result = engine.secure_verify(
        payload=payload,
        signature=signature,
        verifier_id="TRAFFIC_GATEWAY_01"
    )

    print_result(
        "[4] IDENTITY IMPERSONATION",
        result
    )

    # =================================================
    # SCENARIO 5
    # REPLAY ATTACK
    # =================================================

    payload = create_payload()

    signature = generator.generate(
        payload,
        signature_length=16
    )

    engine = build_engine()

    # First legitimate transmission

    first_result = engine.secure_verify(
        payload=payload,
        signature=signature,
        verifier_id="TRAFFIC_GATEWAY_01",
        attack_type="none"
    )

    # Same payload transmitted again

    replay_result = engine.secure_verify(
        payload=payload,
        signature=signature,
        verifier_id="TRAFFIC_GATEWAY_01",
        attack_type="none"
    )

    print_result(
        "[5A] ORIGINAL TRANSMISSION",
        first_result
    )

    print_result(
        "[5B] REPLAY ATTACK",
        replay_result
    )

    print("\n" + "=" * 75)

    print(
        "PHASE 3D DEMONSTRATION COMPLETED"
    )

    print("=" * 75)


if __name__ == "__main__":
    run_demo()