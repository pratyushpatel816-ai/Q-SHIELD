class ThresholdEngine:
    """
    Deterministic threshold-based decision engine.

    IMPORTANT:
    These are prototype calibration values.
    They must later be experimentally evaluated.
    """

    def __init__(
        self,
        s_a=0.05,
        s_v=0.20,
        fidelity_warn=0.95,
        fidelity_reject=0.80
    ):

        if not s_a < s_v:
            raise ValueError(
                "Requirement: s_a must be less than s_v"
            )

        self.s_a = s_a
        self.s_v = s_v

        self.fidelity_warn = fidelity_warn
        self.fidelity_reject = fidelity_reject

    def decide(
        self,
        mismatch_rate,
        fidelity
    ):

        # Strong rejection conditions
        if mismatch_rate > self.s_v:

            return {
                "decision": "REJECT",
                "severity": "HIGH",
                "rule_id": "QDS_MISMATCH_THRESHOLD_EXCEEDED",
                "reason":
                    "Mismatch rate exceeds verification threshold."
            }

        if fidelity < self.fidelity_reject:

            return {
                "decision": "REJECT",
                "severity": "HIGH",
                "rule_id": "QDS_FIDELITY_CRITICAL",
                "reason":
                    "Quantum state recovery fidelity is critically low."
            }

        # Warning conditions
        if mismatch_rate > self.s_a:

            return {
                "decision": "WARN",
                "severity": "MEDIUM",
                "rule_id": "QDS_CHANNEL_DEGRADED",
                "reason":
                    "Mismatch rate exceeds authentication threshold."
            }

        if fidelity < self.fidelity_warn:

            return {
                "decision": "WARN",
                "severity": "MEDIUM",
                "rule_id": "QDS_FIDELITY_DEGRADED",
                "reason":
                    "Quantum channel fidelity is degraded."
            }

        # Valid signature
        return {
            "decision": "ACCEPT",
            "severity": "LOW",
            "rule_id": "QDS_VALID_SIGNATURE",
            "reason":
                "Signature satisfies mismatch and fidelity thresholds."
        }