import hashlib
import uuid
import time


class QDSProtocol:
    """
    Simulation-level Quantum Digital Signature workflow.

    This module provides an application layer around the
    Q-SHIELD quantum security detector.

    It models:

    - Message signing
    - Signer identity
    - Signature integrity
    - Authorized verification
    - Replay protection

    Note:
    This is a research simulation workflow and does not claim
    to implement a production-grade information-theoretic QDS protocol.
    """

    def __init__(self):

        self.used_signature_ids = set()

    @staticmethod
    def generate_message_hash(message):
        """
        Generate deterministic message fingerprint.
        """

        return hashlib.sha256(
            message.encode()
        ).hexdigest()

    def generate_signature(
        self,
        message,
        signer_id,
        authorized_verifiers
    ):
        """
        Generate a simulated QDS signature packet.
        """

        message_hash = self.generate_message_hash(
            message
        )

        signature_id = str(
            uuid.uuid4()
        )

        signature = {

            "signature_id": signature_id,

            "message": message,

            "message_hash": message_hash,

            "signer_id": signer_id,

            "authorized_verifiers":
                authorized_verifiers,

            "timestamp":
                time.time(),

            "signature_valid":
                True
        }

        return signature

    def verify_signature(
        self,
        signature,
        verifier_id
    ):
        """
        Verify signature integrity and authorization.
        """

        results = {

            "valid_message": False,

            "authorized_verifier": False,

            "replay_detected": False,

            "signature_valid": False,

            "final_decision": "REJECT",

            "reason": []
        }

        # -----------------------------------------
        # 1. MESSAGE INTEGRITY CHECK
        # -----------------------------------------

        expected_hash = (
            self.generate_message_hash(
                signature["message"]
            )
        )

        if (
            expected_hash
            == signature["message_hash"]
        ):

            results["valid_message"] = True

        else:

            results["reason"].append(
                "Message integrity violation detected"
            )

        # -----------------------------------------
        # 2. VERIFIER AUTHORIZATION
        # -----------------------------------------

        if (
            verifier_id
            in signature[
                "authorized_verifiers"
            ]
        ):

            results[
                "authorized_verifier"
            ] = True

        else:

            results["reason"].append(
                "Unauthorized verification attempt"
            )

        # -----------------------------------------
        # 3. REPLAY DETECTION
        # -----------------------------------------

        signature_id = (
            signature["signature_id"]
        )

        if (
            signature_id
            in self.used_signature_ids
        ):

            results[
                "replay_detected"
            ] = True

            results["reason"].append(
                "Replay attack detected"
            )

        # -----------------------------------------
        # 4. SIGNATURE VALIDITY
        # -----------------------------------------

        if (
            signature.get(
                "signature_valid",
                False
            )
        ):

            results[
                "signature_valid"
            ] = True

        else:

            results["reason"].append(
                "Invalid or forged signature"
            )

        # -----------------------------------------
        # 5. FINAL QDS DECISION
        # -----------------------------------------

        if (

            results["valid_message"]

            and results[
                "authorized_verifier"
            ]

            and not results[
                "replay_detected"
            ]

            and results[
                "signature_valid"
            ]
        ):

            results[
                "final_decision"
            ] = "ACCEPT"

            self.used_signature_ids.add(
                signature_id
            )

        else:

            results[
                "final_decision"
            ] = "REJECT"

        return results