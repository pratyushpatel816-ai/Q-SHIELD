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


def main():

    separator()

    print("Q-SHIELD")
    print("PHASE 2: QUANTUM DIGITAL SIGNATURE PROTOCOL")

    separator()

    # ==================================================
    # STEP 1: CREATE FIRMWARE COMMAND
    # ==================================================

    print("\n[1] CREATING CANONICAL PAYLOAD")

    payload = CanonicalPayload.create(
        sender_id="CITY_CONTROL_CENTER",
        receiver_id="TRAFFIC_GATEWAY_01",
        device_id="SMART_TRAFFIC_GATEWAY_01",
        command="AUTHORIZE_FIRMWARE_UPDATE",
        firmware_hash="abc123firmwarehashxyz",
        sequence_no=1
    )

    print("\nPayload:")

    for key, value in payload.items():
        print(f"{key}: {value}")

    separator()

    # ==================================================
    # STEP 2: GENERATE QUANTUM SIGNATURE
    # ==================================================

    print("[2] GENERATING QUANTUM SIGNATURE")

    generator = SignatureGenerator(
        shots=256
    )

    signature = generator.generate(
        payload=payload,
        signature_length=16
    )

    print(
        "Signature Type:",
        signature["signature_type"]
    )

    print(
        "Signature Length:",
        signature["signature_length"]
    )

    print(
        "Payload SHA-256:",
        signature["payload_hash"]
    )

    print("\nQuantum Schedule:")

    for position in signature["positions"]:

        print(
            f"Position "
            f"{position['position']:02d} | "
            f"Basis={position['basis']} | "
            f"Bit={position['expected_bit']} | "
            f"State={position['expected_state']}"
        )

    separator()

    # ==================================================
    # STEP 3: VERIFY CLEAN SIGNATURE
    # ==================================================

    print("[3] VERIFYING CLEAN SIGNATURE")

    verifier = SignatureVerifier(
        shots=256
    )

    result = verifier.verify(
        payload=payload,
        signature=signature
    )

    print("\nVERIFICATION RESULT")

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
        "Reason:",
        result["reason"]
    )

    print(
        "Hash Valid:",
        result["payload_hash_valid"]
    )

    print(
        "Mismatch Count:",
        result["mismatch_count"]
    )

    print(
        "Mismatch Rate:",
        result["mismatch_rate"]
    )

    print(
        "Fidelity:",
        result["fidelity"]
    )

    separator()

    # ==================================================
    # STEP 4: NOISY CHANNEL TEST
    # ==================================================

    print("[4] VERIFYING UNDER DEPOLARIZING NOISE")

    noisy_result = verifier.verify(
        payload=payload,
        signature=signature,
        noise_type="depolarizing",
        noise_probability=0.05
    )

    print(
        "Decision:",
        noisy_result["decision"]
    )

    print(
        "Mismatch Rate:",
        noisy_result["mismatch_rate"]
    )

    print(
        "Fidelity:",
        noisy_result["fidelity"]
    )

    print(
        "Reason:",
        noisy_result["reason"]
    )

    separator()

    # ==================================================
    # STEP 5: TAMPERING DEMONSTRATION
    # ==================================================

    print("[5] MESSAGE TAMPERING DEMONSTRATION")

    tampered_payload = payload.copy()

    tampered_payload[
        "command"
    ] = "DELETE_ALL_TRAFFIC_DATA"

    tampered_result = verifier.verify(
        payload=tampered_payload,
        signature=signature
    )

    print(
        "Decision:",
        tampered_result["decision"]
    )

    print(
        "Rule ID:",
        tampered_result["rule_id"]
    )

    print(
        "Reason:",
        tampered_result["reason"]
    )

    separator()

    print("PHASE 2 DEMONSTRATION COMPLETED")


if __name__ == "__main__":
    main()