import math


class BellMeasurementAnomaly:
    """
    Bell Measurement Distribution Anomaly Detector.

    Measures how far the observed Bell measurement distribution
    deviates from the expected approximately uniform distribution.

    In ideal quantum teleportation, the four Bell measurement
    outcomes (00, 01, 10, 11) are expected to occur with
    approximately equal probability.
    """

    EXPECTED_PROBABILITY = 0.25

    @staticmethod
    def compute_probabilities(bell_measurements):
        """
        Convert Bell measurement counts into probabilities.
        """

        total = sum(bell_measurements.values())

        if total == 0:
            return {
                "00": 0.0,
                "01": 0.0,
                "10": 0.0,
                "11": 0.0
            }

        probabilities = {}

        for outcome in ["00", "01", "10", "11"]:

            count = bell_measurements.get(
                outcome,
                0
            )

            probabilities[outcome] = (
                count / total
            )

        return probabilities

    @staticmethod
    def total_variation_distance(probabilities):
        """
        Calculate Total Variation Distance (TVD) between
        observed Bell distribution and ideal uniform distribution.

        TVD = 1/2 * sum(|P_observed - P_expected|)
        """

        distance = 0.0

        for outcome in ["00", "01", "10", "11"]:

            observed = probabilities.get(
                outcome,
                0.0
            )

            distance += abs(
                observed
                - BellMeasurementAnomaly.EXPECTED_PROBABILITY
            )

        return 0.5 * distance

    @staticmethod
    def chi_square_anomaly(
        bell_measurements
    ):
        """
        Calculate normalized Chi-Square anomaly score.

        Measures deviation from the expected uniform
        Bell measurement distribution.
        """

        total = sum(
            bell_measurements.values()
        )

        if total == 0:
            return 0.0

        expected = total / 4

        chi_square = 0.0

        for outcome in [
            "00",
            "01",
            "10",
            "11"
        ]:

            observed = bell_measurements.get(
                outcome,
                0
            )

            chi_square += (
                (observed - expected) ** 2
                / expected
            )

        # Normalize to approximately 0-1 range
        normalized_score = (
            chi_square
            / (chi_square + total)
        )

        return normalized_score

    def analyze(self, bell_measurements):
        """
        Perform complete Bell distribution anomaly analysis.
        """

        probabilities = (
            self.compute_probabilities(
                bell_measurements
            )
        )

        tvd_score = (
            self.total_variation_distance(
                probabilities
            )
        )

        chi_square_score = (
            self.chi_square_anomaly(
                bell_measurements
            )
        )

        # Combined anomaly score
        anomaly_score = (
            0.6 * tvd_score
            + 0.4 * chi_square_score
        )

        return {
            "bell_probabilities": probabilities,
            "tvd_score": round(
                tvd_score,
                6
            ),
            "chi_square_score": round(
                chi_square_score,
                6
            ),
            "anomaly_score": round(
                anomaly_score,
                6
            )
        }