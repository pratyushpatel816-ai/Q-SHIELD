from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


class BellPairAnalyzer:

    def __init__(self, shots=1024):
        self.shots = shots
        self.simulator = AerSimulator()

    @staticmethod
    def create_bell_pair(circuit, qubit_a, qubit_b):
        """
        Create Bell state:

        |Phi+> = (|00> + |11>) / sqrt(2)
        """

        circuit.h(qubit_a)
        circuit.cx(qubit_a, qubit_b)

    def correlation_test(self):
        """
        Test Bell pair correlations.

        For |Phi+>, ideal measurements should
        primarily produce 00 and 11.
        """

        qc = QuantumCircuit(2, 2)

        self.create_bell_pair(qc, 0, 1)

        qc.measure(0, 0)
        qc.measure(1, 1)

        result = self.simulator.run(
            qc,
            shots=self.shots
        ).result()

        counts = result.get_counts()

        correlated = (
            counts.get("00", 0)
            + counts.get("11", 0)
        )

        correlation_rate = correlated / self.shots

        return {
            "counts": counts,
            "correlation_rate": correlation_rate,
            "healthy": correlation_rate >= 0.95
        }