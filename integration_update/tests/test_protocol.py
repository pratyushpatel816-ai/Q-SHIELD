from qshield.protocol.payload import (
    CanonicalPayload
)

from qshield.protocol.signature import (
    SignatureGenerator
)

from qshield.protocol.verifier import (
    SignatureVerifier
)


def create_test_payload(sequence_no=1):
    """
    Create a payload using identities registered
    in the Q-SHIELD IdentityRegistry.
    """

    return CanonicalPayload.create(
        sender_id="CITY_CONTROL_CENTER",
        receiver_id="TRAFFIC_GATEWAY_01",
        device_id="SMART_TRAFFIC_GATEWAY_01",
        command="FIRMWARE_UPDATE",
        firmware_hash="test_hash",
        sequence_no=sequence_no
    )


def test_canonical_hash_consistency():

    payload = create_test_payload()

    hash1 = CanonicalPayload.hash_payload(
        payload
    )

    hash2 = CanonicalPayload.hash_payload(
        payload
    )

    assert hash1 == hash2


def test_signature_generation():

    payload = create_test_payload()

    generator = SignatureGenerator(
        shots=128
    )

    signature = generator.generate(
        payload,
        signature_length=16
    )

    assert signature[
        "signature_length"
    ] == 16

    assert len(
        signature["positions"]
    ) == 16


def test_clean_signature_accepts():

    payload = create_test_payload()

    generator = SignatureGenerator(
        shots=128
    )

    signature = generator.generate(
        payload,
        signature_length=8
    )

    verifier = SignatureVerifier(
        shots=128
    )

    result = verifier.verify(
        payload,
        signature
    )

    assert result["decision"] == "ACCEPT"

    assert result["rule_id"] == (
        "QDS_VALID_SIGNATURE"
    )


def test_message_tampering_rejected():

    payload = create_test_payload()

    generator = SignatureGenerator(
        shots=128
    )

    signature = generator.generate(
        payload,
        signature_length=8
    )

    # Create a copy and modify only the command.
    # Identity remains valid, so verification reaches
    # the payload hash validation layer.
    tampered_payload = payload.copy()

    tampered_payload[
        "command"
    ] = "MALICIOUS_COMMAND"

    verifier = SignatureVerifier(
        shots=128
    )

    result = verifier.verify(
        tampered_payload,
        signature
    )

    assert result["decision"] == "REJECT"

    assert result["rule_id"] == (
        "MESSAGE_TAMPERING"
    )


def test_signature_lengths():

    payload = create_test_payload()

    generator = SignatureGenerator(
        shots=64
    )

    for length in [8, 16, 32]:

        signature = generator.generate(
            payload,
            signature_length=length
        )

        assert len(
            signature["positions"]
        ) == length