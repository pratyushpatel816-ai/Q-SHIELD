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


def create_payload(
    sender_id="CITY_CONTROL_CENTER",
    sequence_no=1,
    expired=False
):

    now = datetime.now(
        timezone.utc
    )

    if expired:

        expiry = (
            now - timedelta(minutes=10)
        ).isoformat()

    else:

        expiry = (
            now + timedelta(minutes=10)
        ).isoformat()

    return {
        "sender_id": sender_id,
        "receiver_id": "TRAFFIC_GATEWAY_01",
        "device_id": "SMART_TRAFFIC_GATEWAY_01",
        "command": "AUTHORIZE_FIRMWARE_UPDATE",
        "firmware_hash": "abc123firmwarehashxyz",
        "nonce": str(uuid.uuid4()),
        "session_id": str(uuid.uuid4()),
        "timestamp": now.isoformat(),
        "expiry": expiry,
        "sequence_no": sequence_no
    }


def build_engine():

    identity_registry = IdentityRegistry()

    authorization_manager = (
        AuthorizationManager()
    )

    authorization_manager.register_user(
        "TRAFFIC_GATEWAY_01",
        "VERIFIER"
    )

    return QShieldSecurityEngine(

        signature_verifier=SignatureVerifier(
            shots=128
        ),

        identity_registry=identity_registry,

        authorization_manager=(
            authorization_manager
        ),

        replay_registry=ReplayRegistry(),

        shots=128
    )


def generate_signature(payload):

    generator = SignatureGenerator(
        shots=128
    )

    return generator.generate(
        payload,
        signature_length=8
    )


# =====================================================
# TEST 1
# LEGITIMATE END-TO-END COMMUNICATION
# =====================================================

def test_legitimate_communication():

    payload = create_payload()

    signature = generate_signature(
        payload
    )

    engine = build_engine()

    result = engine.secure_verify(
        payload=payload,
        signature=signature,
        verifier_id="TRAFFIC_GATEWAY_01",
        attack_type="none"
    )

    assert result["decision"] == "ACCEPT"

    assert result["rule_id"] == (
        "QSHIELD_SECURE"
    )

    assert result["failed_stage"] == (
        "COMPLETE"
    )


# =====================================================
# TEST 2
# QUANTUM PAULI-X ATTACK
# =====================================================

def test_quantum_pauli_x_attack():

    payload = create_payload()

    signature = generate_signature(
        payload
    )

    engine = build_engine()

    result = engine.secure_verify(
        payload=payload,
        signature=signature,
        verifier_id="TRAFFIC_GATEWAY_01",
        attack_type="pauli_x"
    )

    assert result["decision"] == "REJECT"

    assert result["rule_id"] == (
        "QUANTUM_STATE_MANIPULATION"
    )

    assert result["failed_stage"] == (
        "QUANTUM_THREAT_DETECTION"
    )


# =====================================================
# TEST 3
# MESSAGE TAMPERING
# =====================================================

def test_message_tampering():

    payload = create_payload()

    signature = generate_signature(
        payload
    )

    tampered_payload = payload.copy()

    tampered_payload[
        "command"
    ] = "MALICIOUS_COMMAND"

    engine = build_engine()

    result = engine.secure_verify(
        payload=tampered_payload,
        signature=signature,
        verifier_id="TRAFFIC_GATEWAY_01"
    )

    assert result["decision"] == "REJECT"

    assert result["rule_id"] == (
        "MESSAGE_TAMPERING"
    )

    assert result["failed_stage"] == (
        "QDS_VERIFICATION"
    )


# =====================================================
# TEST 4
# IDENTITY IMPERSONATION
# =====================================================

def test_identity_impersonation():

    payload = create_payload(
        sender_id="FAKE_CITY_CONTROL"
    )

    signature = generate_signature(
        payload
    )

    engine = build_engine()

    result = engine.secure_verify(
        payload=payload,
        signature=signature,
        verifier_id="TRAFFIC_GATEWAY_01"
    )

    assert result["decision"] == "REJECT"

    assert result["rule_id"] == (
        "IMPERSONATION_ATTEMPT"
    )

    assert result["failed_stage"] == (
        "IDENTITY"
    )


# =====================================================
# TEST 5
# UNAUTHORIZED VERIFIER
# =====================================================

def test_unauthorized_verifier():

    payload = create_payload()

    signature = generate_signature(
        payload
    )

    engine = build_engine()

    result = engine.secure_verify(
        payload=payload,
        signature=signature,
        verifier_id="TRAFFIC_OPERATOR"
    )

    assert result["decision"] == "REJECT"

    assert result["rule_id"] == (
        "UNAUTHORIZED_VERIFICATION"
    )

    assert result["failed_stage"] == (
        "AUTHORIZATION"
    )


# =====================================================
# TEST 6
# REPLAY ATTACK
# =====================================================

def test_replay_attack():

    payload = create_payload()

    signature = generate_signature(
        payload
    )

    engine = build_engine()

    first_result = engine.secure_verify(
        payload=payload,
        signature=signature,
        verifier_id="TRAFFIC_GATEWAY_01"
    )

    second_result = engine.secure_verify(
        payload=payload,
        signature=signature,
        verifier_id="TRAFFIC_GATEWAY_01"
    )

    assert first_result["decision"] == (
        "ACCEPT"
    )

    assert second_result["decision"] == (
        "REJECT"
    )

    assert second_result["rule_id"] == (
        "REPLAY_ATTACK"
    )


# =====================================================
# TEST 7
# EXPIRED PAYLOAD
# =====================================================

def test_expired_payload():

    payload = create_payload(
        expired=True
    )

    signature = generate_signature(
        payload
    )

    engine = build_engine()

    result = engine.secure_verify(
        payload=payload,
        signature=signature,
        verifier_id="TRAFFIC_GATEWAY_01"
    )

    assert result["decision"] == "REJECT"

    assert result["rule_id"] == (
        "REPLAY_ATTACK"
    )

    assert result["failed_stage"] == (
        "REPLAY_PROTECTION"
    )