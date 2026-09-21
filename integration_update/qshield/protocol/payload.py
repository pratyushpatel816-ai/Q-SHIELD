import json
import hashlib
import uuid
from datetime import datetime, timedelta, timezone


class CanonicalPayload:
    """
    Creates a cryptographically canonical payload.

    The SHA-256 hash of this payload binds all
    message context to the quantum signature.
    """

    @staticmethod
    def create(
        sender_id="CITY_CONTROL_CENTER",
        receiver_id="TRAFFIC_GATEWAY_01",
        device_id="SMART_TRAFFIC_GATEWAY_01",
        command="AUTHORIZE_FIRMWARE_UPDATE",
        firmware_hash="firmware_sha256_placeholder",
        sequence_no=1,
        expiry_minutes=10
    ):

        session_id = str(uuid.uuid4())
        nonce = str(uuid.uuid4())

        timestamp = datetime.now(
            timezone.utc
        )

        expiry = timestamp + timedelta(
            minutes=expiry_minutes
        )

        payload = {
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "device_id": device_id,
            "command": command,
            "firmware_hash": firmware_hash,
            "nonce": nonce,
            "session_id": session_id,
            "timestamp": timestamp.isoformat(),
            "expiry": expiry.isoformat(),
            "sequence_no": sequence_no
        }

        return payload

    @staticmethod
    def canonical_json(payload):
        """
        Deterministic JSON serialization.

        Same payload always produces same hash.
        """

        return json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False
        )

    @staticmethod
    def hash_payload(payload):
        """
        SHA-256 hash of canonical payload.
        """

        canonical = CanonicalPayload.canonical_json(
            payload
        )

        return hashlib.sha256(
            canonical.encode("utf-8")
        ).hexdigest()

    @staticmethod
    def verify_hash(
        payload,
        expected_hash
    ):

        actual_hash = CanonicalPayload.hash_payload(
            payload
        )

        return actual_hash == expected_hash