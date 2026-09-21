from qds.qds_protocol import QDSProtocol
from qds.qds_attack_simulator import QDSAttackSimulator

from qshield.quantum.teleportation import TeleportationEngine
from qshield.detection.integrated_detector import (
    IntegratedQShieldDetector
)


class QShieldQDSSecuritySystem:

    def __init__(self, shots=1024):

        self.shots = shots

        # =====================================================
        # QDS PROTOCOL
        # =====================================================

        self.qds_protocol = QDSProtocol()

        # =====================================================
        # QUANTUM TELEPORTATION ENGINE
        # =====================================================

        self.quantum_engine = TeleportationEngine(
            shots=shots
        )

        # =====================================================
        # Q-SHIELD INTEGRATED DETECTOR
        # =====================================================

        self.detector = IntegratedQShieldDetector(
            mismatch_weight=0.7,
            bell_weight=0.3,
            base_threshold=0.26,
            adaptation_factor=0.4,
            max_threshold=0.32
        )

    # =========================================================
    # END-TO-END SECURITY PIPELINE
    # =========================================================

    def run(
        self,
        message,
        signer_id,
        authorized_verifiers,
        verifier_id,
        qds_attack="none",
        quantum_attack="none",
        noise_type="none",
        noise_probability=0.0
    ):

        # =====================================================
        # 1. GENERATE QDS SIGNATURE
        # =====================================================

        signature = self.qds_protocol.generate_signature(
            message=message,
            signer_id=signer_id,
            authorized_verifiers=authorized_verifiers
        )

        # =====================================================
        # 2. APPLY QDS-LEVEL ATTACK
        # =====================================================

        attacked_signature, attack_metadata = (
            QDSAttackSimulator.apply_attack(
                signature,
                attack_type=qds_attack
            )
        )

        # =====================================================
        # 3. QDS VERIFICATION
        # =====================================================

        qds_verification = self.qds_protocol.verify_signature(
            attacked_signature,
            verifier_id=verifier_id
        )

        # =====================================================
        # 4. QUANTUM TELEPORTATION
        # =====================================================

        quantum_result = self.quantum_engine.run(
            bit=0,
            basis="Z",
            noise_type=noise_type,
            noise_probability=noise_probability,
            attack_type=quantum_attack
        )

        # =====================================================
        # 5. Q-SHIELD SECURITY ANALYSIS
        # =====================================================

        qshield_result = self.detector.analyze(
            mismatch_rate=quantum_result["mismatch_rate"],
            bell_measurements=quantum_result["bell_measurements"]
        )

        # =====================================================
        # 6. OVERALL SECURITY DECISION
        # =====================================================

        qds_threat = (
            qds_verification["final_decision"]
            == "REJECT"
        )

        quantum_threat = (
            qshield_result["attack_detected"]
        )

        overall_threat = (
            qds_threat
            or
            quantum_threat
        )

        if overall_threat:

            final_decision = (
                "SECURITY THREAT DETECTED"
            )

        else:

            final_decision = (
                "SECURE COMMUNICATION"
            )

        # =====================================================
        # 7. RETURN COMPLETE RESULT
        # =====================================================

        return {

            "final_decision":
                final_decision,

            "qds_attack":
                attack_metadata,

            "qds_verification":
                qds_verification,

            "quantum_result":
                quantum_result,

            "qshield_result":
                qshield_result
        }