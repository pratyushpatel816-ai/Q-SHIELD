from qshield.protocol.verifier import SignatureVerifier

from qshield.security.identity import IdentityRegistry
from qshield.security.authorization import AuthorizationManager
from qshield.security.replay import ReplayRegistry
from qshield.security.threat_detector import QuantumThreatDetector

from qshield.quantum.teleportation import TeleportationEngine


class QShieldSecurityEngine:
    """
    Unified Q-SHIELD end-to-end security engine.

    Security Pipeline:

    1. Sender Identity Validation
    2. Verifier Authorization
    3. Replay / Expiry Protection
    4. Quantum Digital Signature Verification
    5. Multi-Basis Quantum Threat Detection
    6. Consume Replay Credentials
    7. Final Security Decision
    """

    def __init__(
        self,
        signature_verifier=None,
        identity_registry=None,
        authorization_manager=None,
        replay_registry=None,
        shots=256
    ):

        self.signature_verifier = (
            signature_verifier
            if signature_verifier is not None
            else SignatureVerifier(shots=shots)
        )

        self.identity_registry = (
            identity_registry
            if identity_registry is not None
            else IdentityRegistry()
        )

        self.authorization_manager = (
            authorization_manager
            if authorization_manager is not None
            else AuthorizationManager()
        )

        self.replay_registry = (
            replay_registry
            if replay_registry is not None
            else ReplayRegistry()
        )

        self.teleportation_engine = (
            TeleportationEngine(shots=shots)
        )

        self.threat_detector = (
            QuantumThreatDetector()
        )

    def analyze_quantum_threat(
        self,
        attack_type="none"
    ):

        probes = [
            (0, "Z"),
            (1, "Z"),
            (0, "X"),
            (1, "X"),
            (0, "Y"),
            (1, "Y")
        ]

        probe_results = []

        for bit, basis in probes:

            result = (
                self.teleportation_engine.run(
                    bit=bit,
                    basis=basis,
                    attack_type=attack_type
                )
            )

            probe_results.append(result)

        return self.threat_detector.analyze(
            probe_results
        )

    @staticmethod
    def build_response(
        decision,
        severity,
        rule_id,
        reason,
        stage,
        evidence=None,
        quantum_analysis=None
    ):

        response = {
            "decision": decision,
            "severity": severity,
            "rule_id": rule_id,
            "reason": reason,
            "failed_stage": stage
        }

        if evidence is not None:

            response["evidence"] = evidence

        if quantum_analysis is not None:

            response[
                "quantum_threat_analysis"
            ] = quantum_analysis

        return response

    def secure_verify(
        self,
        payload,
        signature,
        verifier_id,
        attack_type="none"
    ):

        # =====================================
        # STAGE 1: SENDER IDENTITY VALIDATION
        # =====================================

        sender_valid = (
            self.identity_registry.validate_sender(
                payload["sender_id"]
            )
        )

        if not sender_valid:

            return self.build_response(
                decision="REJECT",
                severity="CRITICAL",
                rule_id="IMPERSONATION_ATTEMPT",
                reason=(
                    "Sender identity is not registered "
                    "or authorized."
                ),
                stage="IDENTITY",
                evidence={
                    "sender_id": payload["sender_id"],
                    "authorized": False
                }
            )

        # =====================================
        # STAGE 2: VERIFIER AUTHORIZATION
        # =====================================

        verifier_authorized = (
            self.authorization_manager.can_verify(
                verifier_id
            )
        )

        if not verifier_authorized:

            role = (
                self.authorization_manager.get_role(
                    verifier_id
                )
            )

            return self.build_response(
                decision="REJECT",
                severity="HIGH",
                rule_id="UNAUTHORIZED_VERIFICATION",
                reason=(
                    "Verifier does not have permission "
                    "to verify QDS signatures."
                ),
                stage="AUTHORIZATION",
                evidence={
                    "verifier_id": verifier_id,
                    "role": role
                }
            )

        # =====================================
        # STAGE 3: REPLAY / EXPIRY PROTECTION
        # =====================================

        replay_result = (
            self.replay_registry.validate_payload(
                payload
            )
        )

        if not replay_result["valid"]:

            return self.build_response(
                decision="REJECT",
                severity="HIGH",
                rule_id=replay_result["rule_id"],
                reason=replay_result["reason"],
                stage="REPLAY_PROTECTION",
                evidence=replay_result["evidence"]
            )

        # =====================================
        # STAGE 4: QUANTUM DIGITAL SIGNATURE
        # =====================================

        signature_result = (
            self.signature_verifier.verify(
                payload,
                signature
            )
        )

        if (
            signature_result["decision"]
            == "REJECT"
        ):

            return self.build_response(
                decision=signature_result["decision"],
                severity=signature_result["severity"],
                rule_id=signature_result["rule_id"],
                reason=signature_result["reason"],
                stage="QDS_VERIFICATION",
                evidence=signature_result.get(
                    "evidence"
                )
            )

        # =====================================
        # STAGE 5: QUANTUM THREAT DETECTION
        # =====================================

        quantum_result = (
            self.analyze_quantum_threat(
                attack_type=attack_type
            )
        )

        if (
            quantum_result["decision"]
            == "REJECT"
        ):

            return self.build_response(
                decision="REJECT",
                severity=quantum_result["severity"],
                rule_id=quantum_result["rule_id"],
                reason=quantum_result["reason"],
                stage="QUANTUM_THREAT_DETECTION",
                quantum_analysis=quantum_result
            )

        # =====================================
        # STAGE 6: CONSUME REPLAY CREDENTIALS
        #
        # Only after ALL checks pass.
        # =====================================

        self.replay_registry.consume_payload(
            payload
        )

        # =====================================
        # STAGE 7: FINAL DECISION
        # =====================================

        if (
            signature_result["decision"] == "WARN"
            or quantum_result["decision"] == "WARN"
        ):

            return self.build_response(
                decision="WARN",
                severity="MEDIUM",
                rule_id="QSHIELD_WARNING",
                reason=(
                    "Security verification completed "
                    "with non-critical anomalies."
                ),
                stage="COMPLETE",
                quantum_analysis=quantum_result
            )

        return self.build_response(
            decision="ACCEPT",
            severity="LOW",
            rule_id="QSHIELD_SECURE",
            reason=(
                "All Q-SHIELD security layers "
                "successfully validated."
            ),
            stage="COMPLETE",
            quantum_analysis=quantum_result
        )