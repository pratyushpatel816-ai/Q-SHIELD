from qshield.protocol.payload import (
    CanonicalPayload
)

from qshield.protocol.signature import (
    SignatureGenerator
)

from qshield.protocol.verifier import (
    SignatureVerifier
)


def create_payload(sequence_no=1):

    return CanonicalPayload.create(
        sender_id="CITY_CONTROL_CENTER",
        receiver_id="TRAFFIC_GATEWAY_01",
        device_id="SMART_TRAFFIC_GATEWAY_01",
        sequence_no=sequence_no
    )


def test_replay_attack_detected():

    verifier = SignatureVerifier(
        shots=64
    )

    generator = SignatureGenerator(
        shots=64
    )

    payload = create_payload()

    signature = generator.generate(
        payload,
        signature_length=8
    )

    first = verifier.verify(
        payload,
        signature
    )

    second = verifier.verify(
        payload,
        signature
    )

    assert first["decision"] == "ACCEPT"

    assert second["decision"] == "REJECT"

    assert second["rule_id"] == (
        "REPLAY_ATTACK"
    )


def test_impersonation_detected():

    verifier = SignatureVerifier(
        shots=64
    )

    generator = SignatureGenerator(
        shots=64
    )

    payload = CanonicalPayload.create(
        sender_id="UNKNOWN_ATTACKER",
        sequence_no=1
    )

    signature = generator.generate(
        payload,
        signature_length=8
    )

    result = verifier.verify(
        payload,
        signature
    )

    assert result["decision"] == "REJECT"

    assert result["rule_id"] == (
        "IMPERSONATION_ATTEMPT"
    )


def test_unauthorized_verifier():

    verifier = SignatureVerifier(
        shots=64
    )

    generator = SignatureGenerator(
        shots=64
    )

    payload = create_payload()

    signature = generator.generate(
        payload,
        signature_length=8
    )

    result = verifier.verify(
        payload,
        signature,
        verifier_id="TRAFFIC_OPERATOR"
    )

    assert result["decision"] == "REJECT"

    assert result["rule_id"] == (
        "UNAUTHORIZED_VERIFICATION"
    )


def test_expired_payload_rejected():

    verifier = SignatureVerifier(
        shots=64
    )

    generator = SignatureGenerator(
        shots=64
    )

    payload = CanonicalPayload.create(
        expiry_minutes=-5
    )

    signature = generator.generate(
        payload,
        signature_length=8
    )

    result = verifier.verify(
        payload,
        signature
    )

    assert result["decision"] == "REJECT"

    assert result["rule_id"] == (
        "REPLAY_ATTACK"
    )