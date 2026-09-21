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


class SignatureVerifier:

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
        # 2. SENDER IDENTITY
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
        # 3. RECEIVER IDENTITY
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
        # 4. DEVICE IDENTITY
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
        # 5. ANTI-REPLAY CHECK
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
        # 6. PAYLOAD HASH VALIDATION
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
        # 7. QUANTUM VERIFICATION
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
        # 8. THRESHOLD DECISION
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
        # 9. CONSUME NONCE ONLY IF ACCEPTED
        # ==========================================

        if response["decision"] == "ACCEPT":

            self.replay_registry.consume_payload(
                payload
            )

        return response