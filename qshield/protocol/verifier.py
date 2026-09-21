
from qshield.quantum.teleportation import (
    TeleportationEngine
)

from qshield.security.identity import (
    IdentityRegistry
)

from qshield.security.replay import (
    ReplayRegistry
)

from qshield.security.authorization import (
    AuthorizationManager
)

from .payload import CanonicalPayload
from .thresholds import ThresholdEngine
from .signature import SignatureGenerator


class SignatureVerifier:

    VALID_SIGNATURE_TYPE = (
        "Q-SHIELD_TELEPORTATION_QDS"
    )

    VALID_BASES = {
        "X",
        "Y",
        "Z"
    }

    VALID_BITS = {
        0,
        1
    }

    def __init__(
        self,
        shots=256,
        threshold_engine=None,
        identity_registry=None,
        replay_registry=None,
        authorization_manager=None
    ):

        self.shots = shots

        self.quantum_engine = TeleportationEngine(
            shots=shots
        )

        self.threshold_engine = (
            threshold_engine
            or ThresholdEngine()
        )

        self.identity_registry = (
            identity_registry
            or IdentityRegistry()
        )

        self.replay_registry = (
            replay_registry
            or ReplayRegistry()
        )

        self.authorization_manager = (
            authorization_manager
            or AuthorizationManager()
        )

        self.signature_generator = (
            SignatureGenerator(
                shots=shots
            )
        )

    def reject(
        self,
        rule_id,
        reason,
        severity="HIGH",
        evidence=None
    ):

        return {
            "decision": "REJECT",
            "severity": severity,
            "rule_id": rule_id,
            "reason": reason,
            "evidence": evidence or {}
        }

    def validate_signature_structure(
        self,
        payload,
        signature
    ):

        # ==========================================
        # 1. BASIC SIGNATURE TYPE VALIDATION
        # ==========================================

        if not isinstance(signature, dict):

            return self.reject(
                rule_id="INVALID_SIGNATURE_STRUCTURE",
                reason=(
                    "Signature must be a dictionary."
                ),
                evidence={
                    "signature_type": type(signature).__name__
                }
            )

        required_fields = {
            "signature_type",
            "signature_length",
            "payload_hash",
            "session_id",
            "sender_id",
            "positions"
        }

        missing_fields = (
            required_fields
            - set(signature.keys())
        )

        if missing_fields:

            return self.reject(
                rule_id="INVALID_SIGNATURE_STRUCTURE",
                reason=(
                    "Signature is missing required fields."
                ),
                evidence={
                    "missing_fields": sorted(
                        missing_fields
                    )
                }
            )

        if (
            signature["signature_type"]
            != self.VALID_SIGNATURE_TYPE
        ):

            return self.reject(
                rule_id="INVALID_SIGNATURE_TYPE",
                reason=(
                    "Signature type is not supported."
                ),
                evidence={
                    "signature_type":
                        signature["signature_type"]
                }
            )

        # ==========================================
        # 2. SIGNATURE LENGTH VALIDATION
        # ==========================================

        signature_length = (
            signature["signature_length"]
        )

        if (
            not isinstance(signature_length, int)
            or isinstance(signature_length, bool)
            or signature_length
            not in SignatureGenerator.VALID_LENGTHS
        ):

            return self.reject(
                rule_id="INVALID_SIGNATURE_LENGTH",
                reason=(
                    "Signature length is invalid."
                ),
                evidence={
                    "signature_length":
                        signature_length,
                    "valid_lengths":
                        SignatureGenerator.VALID_LENGTHS
                }
            )

        positions = signature["positions"]

        if not isinstance(positions, list):

            return self.reject(
                rule_id="INVALID_SIGNATURE_STRUCTURE",
                reason=(
                    "Signature positions must be a list."
                ),
                evidence={
                    "positions_type":
                        type(positions).__name__
                }
            )

        if len(positions) != signature_length:

            return self.reject(
                rule_id="SIGNATURE_LENGTH_MISMATCH",
                reason=(
                    "Number of positions does not match "
                    "signature length."
                ),
                evidence={
                    "declared_length":
                        signature_length,
                    "actual_positions":
                        len(positions)
                }
            )

        # ==========================================
        # 3. PAYLOAD BINDING VALIDATION
        # ==========================================

        if (
            signature["payload_hash"]
            != CanonicalPayload.hash_payload(
                payload
            )
        ):

            return self.reject(
                rule_id="MESSAGE_TAMPERING",
                severity="CRITICAL",
                reason=(
                    "Payload hash does not match the "
                    "hash bound to the quantum signature."
                ),
                evidence={
                    "expected_hash":
                        signature["payload_hash"],
                    "actual_hash":
                        CanonicalPayload.hash_payload(
                            payload
                        )
                }
            )

        if (
            signature["session_id"]
            != payload.get("session_id")
        ):

            return self.reject(
                rule_id="SIGNATURE_SESSION_MISMATCH",
                severity="CRITICAL",
                reason=(
                    "Signature session ID does not match "
                    "the payload session ID."
                ),
                evidence={
                    "signature_session_id":
                        signature["session_id"],
                    "payload_session_id":
                        payload.get("session_id")
                }
            )

        if (
            signature["sender_id"]
            != payload.get("sender_id")
        ):

            return self.reject(
                rule_id="SIGNATURE_SENDER_MISMATCH",
                severity="CRITICAL",
                reason=(
                    "Signature sender ID does not match "
                    "the payload sender ID."
                ),
                evidence={
                    "signature_sender_id":
                        signature["sender_id"],
                    "payload_sender_id":
                        payload.get("sender_id")
                }
            )

        # ==========================================
        # 4. POSITION VALIDATION
        # ==========================================

        expected_schedule = (
            self.signature_generator.derive_schedule(
                signature["payload_hash"],
                signature_length
            )
        )

        expected_positions = set(
            range(signature_length)
        )

        actual_positions = set()

        for index, position in enumerate(positions):

            if not isinstance(position, dict):

                return self.reject(
                    rule_id="INVALID_SIGNATURE_POSITION",
                    reason=(
                        "Each signature position must "
                        "be a dictionary."
                    ),
                    evidence={
                        "index": index
                    }
                )

            required_position_fields = {
                "position",
                "basis",
                "expected_bit"
            }

            missing_position_fields = (
                required_position_fields
                - set(position.keys())
            )

            if missing_position_fields:

                return self.reject(
                    rule_id="INVALID_SIGNATURE_POSITION",
                    reason=(
                        "Signature position is missing "
                        "required fields."
                    ),
                    evidence={
                        "index": index,
                        "missing_fields":
                            sorted(
                                missing_position_fields
                            )
                    }
                )

            position_index = position["position"]

            if (
                not isinstance(position_index, int)
                or isinstance(position_index, bool)
                or position_index
                not in expected_positions
            ):

                return self.reject(
                    rule_id="INVALID_SIGNATURE_POSITION_INDEX",
                    reason=(
                        "Signature position index is invalid."
                    ),
                    evidence={
                        "index": index,
                        "position":
                            position_index
                    }
                )

            if position_index in actual_positions:

                return self.reject(
                    rule_id="DUPLICATE_SIGNATURE_POSITION",
                    reason=(
                        "Signature contains duplicate "
                        "position indices."
                    ),
                    evidence={
                        "position":
                            position_index
                    }
                )

            actual_positions.add(position_index)

            basis = position["basis"]
            expected_bit = position["expected_bit"]

            if basis not in self.VALID_BASES:

                return self.reject(
                    rule_id="INVALID_QUANTUM_BASIS",
                    reason=(
                        "Quantum basis must be X, Y, or Z."
                    ),
                    evidence={
                        "position":
                            position_index,
                        "basis":
                            basis
                    }
                )

            if (
                not isinstance(expected_bit, int)
                or isinstance(expected_bit, bool)
                or expected_bit not in self.VALID_BITS
            ):

                return self.reject(
                    rule_id="INVALID_EXPECTED_BIT",
                    reason=(
                        "Expected quantum bit must be 0 or 1."
                    ),
                    evidence={
                        "position":
                            position_index,
                        "expected_bit":
                            expected_bit
                    }
                )

            expected_item = (
                expected_schedule[position_index]
            )

            if (
                basis
                != expected_item["basis"]
                or expected_bit
                != expected_item["bit"]
            ):

                return self.reject(
                    rule_id="QUANTUM_SCHEDULE_MISMATCH",
                    severity="CRITICAL",
                    reason=(
                        "Submitted quantum schedule does "
                        "not match the payload-derived schedule."
                    ),
                    evidence={
                        "position":
                            position_index,
                        "submitted": {
                            "basis":
                                basis,
                            "expected_bit":
                                expected_bit
                        },
                        "derived": {
                            "basis":
                                expected_item["basis"],
                            "expected_bit":
                                expected_item["bit"]
                        }
                    }
                )

        if actual_positions != expected_positions:

            return self.reject(
                rule_id="INVALID_SIGNATURE_POSITIONS",
                reason=(
                    "Signature positions must contain "
                    "each index exactly once."
                ),
                evidence={
                    "expected_positions":
                        sorted(expected_positions),
                    "actual_positions":
                        sorted(actual_positions)
                }
            )

        return None

    def verify(
        self,
        payload,
        signature,
        verifier_id="CITY_SECURITY_VERIFIER",
        noise_type="none",
        noise_probability=0.0
    ):

        # ==========================================
        # 1. VERIFIER AUTHORIZATION
        # ==========================================

        if not self.authorization_manager.can_verify(
            verifier_id
        ):

            return self.reject(
                rule_id="UNAUTHORIZED_VERIFICATION",
                severity="HIGH",
                reason=(
                    "Verifier does not have permission "
                    "to verify QDS signatures."
                ),
                evidence={
                    "verifier_id": verifier_id,
                    "role":
                        self.authorization_manager.get_role(
                            verifier_id
                        )
                }
            )

        # ==========================================
        # 2. SIGNATURE STRUCTURE AND BINDING
        # ==========================================

        structure_result = (
            self.validate_signature_structure(
                payload,
                signature
            )
        )

        if structure_result is not None:

            return structure_result

        # ==========================================
        # 3. SENDER IDENTITY
        # ==========================================

        sender_id = payload.get(
            "sender_id"
        )

        if not self.identity_registry.validate_sender(
            sender_id
        ):

            return self.reject(
                rule_id="IMPERSONATION_ATTEMPT",
                severity="CRITICAL",
                reason=(
                    "Sender identity is not registered "
                    "or authorized."
                ),
                evidence={
                    "sender_id": sender_id,
                    "authorized": False
                }
            )

        # ==========================================
        # 4. RECEIVER IDENTITY
        # ==========================================

        receiver_id = payload.get(
            "receiver_id"
        )

        if not self.identity_registry.validate_receiver(
            receiver_id
        ):

            return self.reject(
                rule_id="INVALID_RECEIVER_IDENTITY",
                reason=(
                    "Receiver identity is not authorized."
                ),
                evidence={
                    "receiver_id": receiver_id
                }
            )

        # ==========================================
        # 5. DEVICE IDENTITY
        # ==========================================

        device_id = payload.get(
            "device_id"
        )

        if not self.identity_registry.validate_device(
            device_id
        ):

            return self.reject(
                rule_id="INVALID_DEVICE_IDENTITY",
                reason=(
                    "Target device is not registered."
                ),
                evidence={
                    "device_id": device_id
                }
            )

        # ==========================================
        # 6. ANTI-REPLAY CHECK
        # ==========================================

        replay_check = (
            self.replay_registry.validate_payload(
                payload
            )
        )

        if not replay_check["valid"]:

            return self.reject(
                rule_id=replay_check["rule_id"],
                severity="HIGH",
                reason=replay_check["reason"],
                evidence=replay_check["evidence"]
            )

        # ==========================================
        # 7. PAYLOAD HASH VALIDATION
        # ==========================================

        actual_hash = (
            CanonicalPayload.hash_payload(
                payload
            )
        )

        expected_hash = signature[
            "payload_hash"
        ]

        if actual_hash != expected_hash:

            return self.reject(
                rule_id="MESSAGE_TAMPERING",
                severity="CRITICAL",
                reason=(
                    "Payload hash does not match the "
                    "hash bound to the quantum signature."
                ),
                evidence={
                    "expected_hash": expected_hash,
                    "actual_hash": actual_hash
                }
            )

        # ==========================================
        # 8. QUANTUM VERIFICATION
        # ==========================================

        measurements = []
        mismatch_count = 0
        fidelity_values = []

        for position in signature["positions"]:

            expected_bit = position[
                "expected_bit"
            ]

            basis = position["basis"]

            result = self.quantum_engine.run(
                bit=expected_bit,
                basis=basis,
                noise_type=noise_type,
                noise_probability=noise_probability
            )

            position_mismatch = (
                result["mismatch_rate"] > 0.5
            )

            if position_mismatch:
                mismatch_count += 1

            fidelity_values.append(
                result["fidelity_proxy"]
            )

            measurements.append({
                "position":
                    position["position"],

                "basis":
                    basis,

                "expected_bit":
                    expected_bit,

                "match_rate":
                    result["match_rate"],

                "mismatch_rate":
                    result["mismatch_rate"],

                "fidelity":
                    result["fidelity_proxy"],

                "mismatch":
                    position_mismatch
            })

        signature_length = signature[
            "signature_length"
        ]

        mismatch_rate = (
            mismatch_count
            / signature_length
        )

        average_fidelity = (
            sum(fidelity_values)
            / len(fidelity_values)
        )

        # ==========================================
        # 9. THRESHOLD DECISION
        # ==========================================

        threshold_decision = (
            self.threshold_engine.decide(
                mismatch_rate,
                average_fidelity
            )
        )

        response = {
            "decision":
                threshold_decision["decision"],

            "severity":
                threshold_decision["severity"],

            "rule_id":
                threshold_decision["rule_id"],

            "reason":
                threshold_decision["reason"],

            "payload_hash_valid": True,

            "mismatch_count":
                mismatch_count,

            "signature_length":
                signature_length,

            "mismatch_rate":
                round(mismatch_rate, 6),

            "fidelity":
                round(average_fidelity, 6),

            "noise_type":
                noise_type,

            "noise_probability":
                noise_probability,

            "verifier_id":
                verifier_id,

            "measurements":
                measurements
        }

        # ==========================================
        # 10. CONSUME NONCE ONLY IF ACCEPTED
        # ==========================================

        if response["decision"] == "ACCEPT":

            self.replay_registry.consume_payload(
                payload
            )

        return response