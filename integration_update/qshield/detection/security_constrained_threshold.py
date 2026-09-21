class SecurityConstrainedThreshold:
    """
    Security-Constrained Adaptive Thresholding (SCAT)

    The threshold adapts according to estimated channel noise,
    but is restricted by a maximum security threshold to prevent
    excessive adaptation from masking quantum attacks.
    """

    def __init__(
        self,
        base_threshold=0.26,
        adaptation_factor=0.4,
        max_threshold=0.32
    ):
        self.base_threshold = base_threshold
        self.adaptation_factor = adaptation_factor
        self.max_threshold = max_threshold

    def estimate_noise(self, mismatch_rate):
        """
        Blind noise estimation based on observed mismatch rate.

        In the current Q-SHIELD framework, mismatch is used as
        a proxy for channel degradation.
        """

        return max(0.0, mismatch_rate)

    def compute_threshold(self, mismatch_rate):
        """
        Compute security-constrained adaptive threshold.

        Formula:

        T_adaptive = T_base + alpha * estimated_noise

        T_secure = min(T_adaptive, T_max)
        """

        estimated_noise = self.estimate_noise(
            mismatch_rate
        )

        adaptive_threshold = (
            self.base_threshold
            + self.adaptation_factor
            * estimated_noise
        )

        secure_threshold = min(
            adaptive_threshold,
            self.max_threshold
        )

        return {
            "threshold": secure_threshold,
            "adaptive_threshold": adaptive_threshold,
            "estimated_noise": estimated_noise,
            "threshold_capped": (
                adaptive_threshold > self.max_threshold
            )
        }

    def detect(self, mismatch_rate):
        """
        Determine whether the observed mismatch indicates
        a potential attack.
        """

        result = self.compute_threshold(
            mismatch_rate
        )

        attack_detected = (
            mismatch_rate > result["threshold"]
        )

        result["attack_detected"] = attack_detected
        result["mismatch_rate"] = mismatch_rate

        return result