from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

from .states import PauliStateEncoder
from .noise import NoiseFactory


class TeleportationEngine:

    def __init__(self, shots=1024):
        self.shots = shots

    @staticmethod
    def apply_measurement_basis(
        circuit,
        qubit,
        basis
    ):
        """
        Convert X/Y basis measurement
        into computational Z measurement.
        """

        basis = basis.upper()

        if basis == "Z":
            pass

        elif basis == "X":
            circuit.h(qubit)

        elif basis == "Y":
            circuit.sdg(qubit)
            circuit.h(qubit)

        else:
            raise ValueError(
                "Basis must be X, Y or Z"
            )

    def build_circuit(
        self,
        bit,
        basis
    ):

        # q0 = message qubit
        # q1 = Alice Bell qubit
        # q2 = Bob Bell qubit

        qc = QuantumCircuit(3, 3)

        # ------------------------------------------------
        # STEP 1: PREPARE PAULI EIGENSTATE
        # ------------------------------------------------

        PauliStateEncoder.prepare_state(
            qc,
            qubit=0,
            bit=bit,
            basis=basis
        )

        # ------------------------------------------------
        # STEP 2: CREATE BELL PAIR
        # ------------------------------------------------

        qc.h(1)
        qc.cx(1, 2)

        # ------------------------------------------------
        # STEP 3: BELL MEASUREMENT
        # ------------------------------------------------

        qc.cx(0, 1)
        qc.h(0)

        qc.measure(0, 0)
        qc.measure(1, 1)

        # ------------------------------------------------
        # STEP 4: CONDITIONAL PAULI CORRECTION
        #
        # Standard teleportation:
        #
        # Z^m1 X^m2
        # ------------------------------------------------

        with qc.if_test((qc.clbits[0], 1)):
            qc.z(2)

        with qc.if_test((qc.clbits[1], 1)):
            qc.x(2)

        # ------------------------------------------------
        # STEP 5: PROJECTIVE MEASUREMENT
        # ------------------------------------------------

        self.apply_measurement_basis(
            qc,
            2,
            basis
        )

        qc.measure(2, 2)

        return qc

    def run(
        self,
        bit=0,
        basis="Z",
        noise_type="none",
        noise_probability=0.0
    ):

        circuit = self.build_circuit(
            bit,
            basis
        )

        noise_model = NoiseFactory.get_noise(
            noise_type,
            noise_probability
        )

        simulator = AerSimulator(
            noise_model=noise_model
        )

        result = simulator.run(
            circuit,
            shots=self.shots
        ).result()

        counts = result.get_counts()

        total = sum(counts.values())

        matching_shots = 0
        mismatch_shots = 0

        bell_outcomes = {}

        for outcome, count in counts.items():

            # Qiskit bit string order:
            # c2 c1 c0
            #
            # c0 = m1
            # c1 = m2
            # c2 = Bob final measurement

            outcome = outcome.replace(" ", "")

            bob_bit = int(outcome[0])

            m2 = int(outcome[1])
            m1 = int(outcome[2])

            bell_key = f"{m1}{m2}"

            bell_outcomes[bell_key] = (
                bell_outcomes.get(bell_key, 0)
                + count
            )

            if bob_bit == bit:
                matching_shots += count
            else:
                mismatch_shots += count

        match_rate = matching_shots / total
        mismatch_rate = mismatch_shots / total

        # Prototype fidelity proxy:
        # probability that the expected state is recovered.
        fidelity_proxy = match_rate

        return {
            "expected_bit": bit,
            "basis": basis.upper(),
            "expected_state":
                PauliStateEncoder.state_name(
                    bit,
                    basis
                ),
            "counts": counts,
            "bell_measurements": bell_outcomes,
            "total_shots": total,
            "matching_shots": matching_shots,
            "mismatch_shots": mismatch_shots,
            "match_rate": round(match_rate, 6),
            "mismatch_rate": round(
                mismatch_rate,
                6
            ),
            "fidelity_proxy": round(
                fidelity_proxy,
                6
            ),
            "noise_type": noise_type,
            "noise_probability":
                noise_probability
        }