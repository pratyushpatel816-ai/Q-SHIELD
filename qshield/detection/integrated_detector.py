from .dual_signal_detector import DualSignalDetector
from .security_constrained_threshold import (
    SecurityConstrainedThreshold
)


class IntegratedQShieldDetector:
    """
    Final integrated Q-SHIELD detection architecture.

    Combines:

    1. Teleportation mismatch rate
    2. Bell measurement anomaly
    3. Blind adaptive threshold estimation
    4. Security-constrained threshold capping

    The detector computes a dual-signal security score and
    compares it against a dynamically adapted but security-bounded
    threshold.
    """

    def __init__(
        self,
        mismatch_weight=0.7,
        bell_weight=0.3,
        base_threshold=0.26,
        adaptation_factor=0.4,
        max_threshold=0.32
    ):

        # Dual quantum signal analyzer
        self.dual_detector = DualSignalDetector(
            mismatch_weight=mismatch_weight,
            bell_weight=bell_weight,
            detection_threshold=base_threshold
        )

        # Security-constrained adaptive threshold
        self.threshold_engine = (
            SecurityConstrainedThreshold(
                base_threshold=base_threshold,
                adaptation_factor=adaptation_factor,
                max_threshold=max_threshold
            )
        )

    def analyze(
        self,
        mismatch_rate,
        bell_measurements
    ):
        """
        Perform complete integrated Q-SHIELD analysis.
        """

        # ---------------------------------------------
        # STEP 1: COMPUTE DUAL-SIGNAL SECURITY SCORE
        # ---------------------------------------------

        signal_result = (
            self.dual_detector.compute_security_score(
                mismatch_rate=mismatch_rate,
                bell_measurements=bell_measurements
            )
        )

        security_score = (
            signal_result["security_score"]
        )

        # ---------------------------------------------
        # STEP 2: ESTIMATE CHANNEL NOISE
        # ---------------------------------------------

        threshold_result = (
            self.threshold_engine.compute_threshold(
                mismatch_rate
            )
        )

        adaptive_threshold = (
            threshold_result["threshold"]
        )

        # ---------------------------------------------
        # STEP 3: FINAL SECURITY DECISION
        # ---------------------------------------------

        attack_detected = (
            security_score > adaptive_threshold
        )

        # ---------------------------------------------
        # STEP 4: SECURITY SEVERITY
        # ---------------------------------------------

        margin = (
            security_score
            - adaptive_threshold
        )

        if attack_detected:

            if margin > 0.20:
                severity = "HIGH"

            else:
                severity = "MEDIUM"

            decision = "ATTACK"

        else:

            severity = "LOW"
            decision = "NORMAL"

        # ---------------------------------------------
        # FINAL RESULT
        # ---------------------------------------------

        return {

            "decision": decision,

            "attack_detected":
                attack_detected,

            "severity":
                severity,

            "security_score":
                round(security_score, 6),

            "adaptive_threshold":
                round(adaptive_threshold, 6),

            "decision_margin":
                round(margin, 6),

            "estimated_noise":
                round(
                    threshold_result[
                        "estimated_noise"
                    ],
                    6
                ),

            "threshold_capped":
                threshold_result[
                    "threshold_capped"
                ],

            "mismatch_rate":
                round(mismatch_rate, 6),

            "bell_anomaly_score":
                signal_result[
                    "bell_anomaly_score"
                ],

            "bell_analysis":
                signal_result[
                    "bell_analysis"
                ]
        }