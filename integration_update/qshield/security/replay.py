from datetime import datetime, timezone


class ReplayRegistry:
    """
    Anti-replay protection.

    Tracks:
    - Consumed nonces
    - Last accepted sequence number
    - Payload expiry
    """

    def __init__(self):

        self.consumed_nonces = set()

        self.last_sequence = {}

    def is_nonce_used(
        self,
        nonce
    ):

        return nonce in self.consumed_nonces

    def consume_nonce(
        self,
        nonce
    ):

        self.consumed_nonces.add(nonce)

    def validate_sequence(
        self,
        sender_id,
        sequence_no
    ):
        """
        Sequence number must strictly increase.
        """

        last = self.last_sequence.get(
            sender_id
        )

        if last is None:
            return True

        return sequence_no > last

    def update_sequence(
        self,
        sender_id,
        sequence_no
    ):

        self.last_sequence[
            sender_id
        ] = sequence_no

    def is_expired(
        self,
        expiry_timestamp
    ):

        expiry = datetime.fromisoformat(
            expiry_timestamp
        )

        now = datetime.now(
            timezone.utc
        )

        return now > expiry

    def validate_payload(
        self,
        payload
    ):
        """
        Run all anti-replay checks.

        Returns detailed evidence.
        """

        nonce = payload["nonce"]

        sender_id = payload[
            "sender_id"
        ]

        sequence_no = payload[
            "sequence_no"
        ]

        expiry = payload["expiry"]

        # Check nonce
        if self.is_nonce_used(nonce):

            return {
                "valid": False,
                "rule_id": "REPLAY_ATTACK",
                "reason":
                    "Nonce has already been consumed.",
                "evidence": {
                    "nonce": nonce,
                    "nonce_status": "REUSED"
                }
            }

        # Check sequence
        if not self.validate_sequence(
            sender_id,
            sequence_no
        ):

            return {
                "valid": False,
                "rule_id": "REPLAY_ATTACK",
                "reason":
                    "Sequence number is not greater "
                    "than the previously accepted sequence.",
                "evidence": {
                    "sequence_no": sequence_no,
                    "last_sequence":
                        self.last_sequence.get(
                            sender_id
                        )
                }
            }

        # Check expiry
        if self.is_expired(expiry):

            return {
                "valid": False,
                "rule_id": "REPLAY_ATTACK",
                "reason":
                    "Payload has expired.",
                "evidence": {
                    "expiry": expiry,
                    "status": "EXPIRED"
                }
            }

        return {
            "valid": True,
            "rule_id": "REPLAY_CHECK_PASSED",
            "reason":
                "Nonce, sequence number and expiry are valid.",
            "evidence": {
                "nonce_status": "NEW",
                "sequence_status": "VALID",
                "expiry_status": "VALID"
            }
        }

    def consume_payload(
        self,
        payload
    ):
        """
        Call ONLY after successful verification.
        """

        self.consume_nonce(
            payload["nonce"]
        )

        self.update_sequence(
            payload["sender_id"],
            payload["sequence_no"]
        )