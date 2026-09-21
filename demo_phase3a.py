from qshield.protocol.payload import (
    CanonicalPayload
)

from qshield.protocol.signature import (
    SignatureGenerator
)

from qshield.protocol.verifier import (
    SignatureVerifier
)


def separator():
    print("\n" + "=" * 70)


def print_result(title, result):

    separator()

    print(title)

    print("Decision:", result["decision"])
    print("Severity:", result["severity"])
    print("Rule ID:", result["rule_id"])
    print("Reason:", result["reason"])

    if "evidence" in result:
        print("Evidence:", result["evidence"])


def main():

    print("\nQ-SHIELD")
    print("PHASE 3A: IDENTITY, RBAC & ANTI-REPLAY")

    # =============================================
    # Shared verifier = shared replay state
    # =============================================

    verifier = SignatureVerifier(
        shots=128
    )

    generator = SignatureGenerator(
        shots=128
    )

    # =============================================
    # SCENARIO 1
    # LEGITIMATE SIGNATURE
    # =============================================

    payload = CanonicalPayload.create(
        firmware_hash="firmware_v1",
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

    print_result(
        "[1] LEGITIMATE SIGNATURE",
        result
    )

    # =============================================
    # SCENARIO 2
    # REPLAY ATTACK
    # =============================================

    replay_result = verifier.verify(
        payload,
        signature
    )

    print_result(
        "[2] REPLAY ATTACK",
        replay_result
    )

    # =============================================
    # SCENARIO 3
    # IMPERSONATION
    # =============================================

    malicious_payload = (
        CanonicalPayload.create(
            sender_id="FAKE_CITY_CONTROL",
            sequence_no=2
        )
    )

    malicious_signature = (
        generator.generate(
            malicious_payload,
            signature_length=8
        )
    )

    impersonation_result = (
        verifier.verify(
            malicious_payload,
            malicious_signature
        )
    )

    print_result(
        "[3] IMPERSONATION ATTEMPT",
        impersonation_result
    )

    # =============================================
    # SCENARIO 4
    # UNAUTHORIZED VERIFICATION
    # =============================================

    new_payload = CanonicalPayload.create(
        sequence_no=3
    )

    new_signature = generator.generate(
        new_payload,
        signature_length=8
    )

    unauthorized_result = verifier.verify(
        new_payload,
        new_signature,
        verifier_id="TRAFFIC_OPERATOR"
    )

    print_result(
        "[4] UNAUTHORIZED VERIFICATION",
        unauthorized_result
    )

    # =============================================
    # SCENARIO 5
    # EXPIRED PAYLOAD
    # =============================================

    expired_payload = CanonicalPayload.create(
        sequence_no=4,
        expiry_minutes=-10
    )

    expired_signature = generator.generate(
        expired_payload,
        signature_length=8
    )

    expired_result = verifier.verify(
        expired_payload,
        expired_signature
    )

    print_result(
        "[5] EXPIRED PAYLOAD",
        expired_result
    )

    separator()

    print(
        "PHASE 3A DEMONSTRATION COMPLETED"
    )


if __name__ == "__main__":
    main()