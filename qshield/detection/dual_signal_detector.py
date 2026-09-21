from .bell_anomaly import BellMeasurementAnomaly


class DualSignalDetector:
    """
    Q-SHIELD Dual-Signal Attack Detector.

    Combines two quantum security signals:

    1. Teleportation mismatch rate
    2. Bell measurement distribution anomaly

    The combined score is used to distinguish legitimate
    quantum channel noise from adversarial disturbances.
    """

    def __init__(
        self,
        mismatch_weight=0.7,
        bell_weight=0.3,
        detection_threshold=0.30
    ):

        if abs(
            (mismatch_weight + bell_weight) - 1.0
        ) > 1e-6:

            raise ValueError(
                "Mismatch and Bell weights must sum to 1.0"
            )

        self.mismatch_weight = mismatch_weight
        self.bell_weight = bell_weight
        self.detection_threshold = detection_threshold

        self.bell_analyzer = (
            BellMeasurementAnomaly()
        )

    def compute_security_score(
        self,
        mismatch_rate,
        bell_measurements
    ):
        """
        Compute the combined dual-signal security score.

        Security Score =
            mismatch_weight × mismatch_rate
            +
            bell_weight × Bell anomaly score
        """

        bell_result = (
            self.bell_analyzer.analyze(
                bell_measurements
            )
        )

        bell_anomaly_score = (
            bell_result["anomaly_score"]
        )

        security_score = (
            self.mismatch_weight
            * mismatch_rate
            +
            self.bell_weight
            * bell_anomaly_score
        )

        return {
            "security_score": security_score,
            "mismatch_rate": mismatch_rate,
            "bell_anomaly_score": bell_anomaly_score,
            "bell_analysis": bell_result
        }

    def detect(
        self,
        mismatch_rate,
        bell_measurements
    ):
        """
        Perform dual-signal attack detection.
        """

        result = self.compute_security_score(
            mismatch_rate,
            bell_measurements
        )

        attack_detected = (
            result["security_score"]
            > self.detection_threshold
        )

        result["threshold"] = (
            self.detection_threshold
        )

        result["attack_detected"] = (
            attack_detected
        )

        return result