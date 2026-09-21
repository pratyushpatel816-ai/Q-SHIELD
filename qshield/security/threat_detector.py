class QuantumThreatDetector:
    """
    Converts quantum verification statistics into
    explainable cybersecurity threat decisions.
    """

    def __init__(
        self,
        warn_threshold=0.05,
        reject_threshold=0.20
    ):
        """
        Thresholds represent aggregate mismatch rate.

        < warn_threshold:
            ACCEPT

        warn_threshold to reject_threshold:
            WARN

        >= reject_threshold:
            REJECT
        """

        if warn_threshold < 0:
            raise ValueError(
                "warn_threshold cannot be negative"
            )

        if reject_threshold <= warn_threshold:
            raise ValueError(
                "reject_threshold must be greater "
                "than warn_threshold"
            )

        self.warn_threshold = warn_threshold
        self.reject_threshold = reject_threshold

    def analyze(self, results):
        """
        Analyze multiple quantum probe results.

        Parameters
        ----------
        results : list[dict]

        Each result should contain:
        - match_rate
        - mismatch_rate
        - fidelity_proxy
        - basis
        """

        if not results:
            raise ValueError(
                "At least one quantum result is required"
            )

        total_match = 0.0
        total_mismatch = 0.0
        total_fidelity = 0.0

        basis_statistics = {}

        for result in results:

            basis = result["basis"]

            match_rate = result["match_rate"]
            mismatch_rate = result["mismatch_rate"]
            fidelity = result["fidelity_proxy"]

            total_match += match_rate
            total_mismatch += mismatch_rate
            total_fidelity += fidelity

            if basis not in basis_statistics:

                basis_statistics[basis] = {
                    "count": 0,
                    "match_total": 0.0,
                    "mismatch_total": 0.0,
                    "fidelity_total": 0.0
                }

            basis_statistics[basis][
                "count"
            ] += 1

            basis_statistics[basis][
                "match_total"
            ] += match_rate

            basis_statistics[basis][
                "mismatch_total"
            ] += mismatch_rate

            basis_statistics[basis][
                "fidelity_total"
            ] += fidelity

        n = len(results)

        average_match = total_match / n
        average_mismatch = total_mismatch / n
        average_fidelity = total_fidelity / n

        # Calculate basis-level statistics
        basis_summary = {}

        for basis, stats in (
            basis_statistics.items()
        ):

            count = stats["count"]

            basis_summary[basis] = {
                "average_match_rate":
                    round(
                        stats["match_total"] / count,
                        6
                    ),

                "average_mismatch_rate":
                    round(
                        stats["mismatch_total"] / count,
                        6
                    ),

                "average_fidelity":
                    round(
                        stats["fidelity_total"] / count,
                        6
                    )
            }

        # --------------------------------------------
        # THREAT CLASSIFICATION
        # --------------------------------------------

        if (
            average_mismatch
            >= self.reject_threshold
        ):

            decision = "REJECT"

            severity = "HIGH"

            rule_id = (
                "QUANTUM_STATE_MANIPULATION"
            )

            reason = (
                "Aggregate quantum mismatch exceeds "
                "the rejection threshold."
            )

        elif (
            average_mismatch
            >= self.warn_threshold
        ):

            decision = "WARN"

            severity = "MEDIUM"

            rule_id = (
                "QUANTUM_ANOMALY_DETECTED"
            )

            reason = (
                "Quantum mismatch exceeds the "
                "warning threshold."
            )

        else:

            decision = "ACCEPT"

            severity = "LOW"

            rule_id = (
                "QUANTUM_CHANNEL_NORMAL"
            )

            reason = (
                "Quantum verification statistics are "
                "within acceptable thresholds."
            )

        return {
            "decision": decision,

            "severity": severity,

            "rule_id": rule_id,

            "reason": reason,

            "evidence": {
                "probe_count": n,

                "average_match_rate":
                    round(
                        average_match,
                        6
                    ),

                "average_mismatch_rate":
                    round(
                        average_mismatch,
                        6
                    ),

                "average_fidelity":
                    round(
                        average_fidelity,
                        6
                    ),

                "warn_threshold":
                    self.warn_threshold,

                "reject_threshold":
                    self.reject_threshold,

                "basis_summary":
                    basis_summary
            }
        }