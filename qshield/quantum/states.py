from qiskit import QuantumCircuit
import numpy as np


class PauliStateEncoder:
    """
    Encodes classical bits into Pauli eigenstates.

    Z basis:
        0 -> |0>
        1 -> |1>

    X basis:
        0 -> |+>
        1 -> |->

    Y basis:
        0 -> |+i>
        1 -> |-i>
    """

    VALID_BASES = ["X", "Y", "Z"]

    @staticmethod
    def validate(bit: int, basis: str):
        if bit not in [0, 1]:
            raise ValueError("Bit must be 0 or 1")

        if basis.upper() not in PauliStateEncoder.VALID_BASES:
            raise ValueError(
                f"Invalid basis {basis}. Use X, Y, or Z."
            )

    @staticmethod
    def prepare_state(circuit: QuantumCircuit,
                      qubit: int,
                      bit: int,
                      basis: str):
        """
        Prepare one of six Pauli eigenstates.
        """

        basis = basis.upper()

        PauliStateEncoder.validate(bit, basis)

        # Z BASIS
        if basis == "Z":
            if bit == 1:
                circuit.x(qubit)

        # X BASIS
        elif basis == "X":

            # |+> = H|0>
            if bit == 0:
                circuit.h(qubit)

            # |-> = H|1>
            else:
                circuit.x(qubit)
                circuit.h(qubit)

        # Y BASIS
        elif basis == "Y":

            # |+i>
            if bit == 0:
                circuit.h(qubit)
                circuit.s(qubit)

            # |-i>
            else:
                circuit.x(qubit)
                circuit.h(qubit)
                circuit.s(qubit)

    @staticmethod
    def state_name(bit: int, basis: str) -> str:

        mapping = {
            ("Z", 0): "|0>",
            ("Z", 1): "|1>",
            ("X", 0): "|+>",
            ("X", 1): "|->",
            ("Y", 0): "|+i>",
            ("Y", 1): "|-i>",
        }

        return mapping[(basis.upper(), bit)]