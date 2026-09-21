from qiskit import QuantumCircuit


class QuantumAttackSimulator:
    """
    Applies controlled adversarial operations to a quantum circuit.

    Supported attacks:
    - none
    - pauli_x
    - pauli_y
    - pauli_z
    - entanglement_disruption
    """

    VALID_ATTACKS = {
        "none",
        "pauli_x",
        "pauli_y",
        "pauli_z",
        "entanglement_disruption"
    }

    @staticmethod
    def validate_attack(attack_type):

        if attack_type not in (
            QuantumAttackSimulator.VALID_ATTACKS
        ):
            raise ValueError(
                f"Unsupported attack type: {attack_type}"
            )

    @staticmethod
    def apply_attack(
        circuit,
        attack_type="none",
        target_qubit=2
    ):
        """
        Apply attack directly to the quantum circuit.

        target_qubit:
        In the teleportation circuit, qubit 2 is the
        receiver's recovered quantum state.
        """

        QuantumAttackSimulator.validate_attack(
            attack_type
        )

        if attack_type == "none":
            return circuit

        if attack_type == "pauli_x":
            circuit.x(target_qubit)

        elif attack_type == "pauli_y":
            circuit.y(target_qubit)

        elif attack_type == "pauli_z":
            circuit.z(target_qubit)

        elif attack_type == "entanglement_disruption":
            """
            Simulate disruption by introducing a Hadamard
            operation followed by a bit flip.

            This deliberately disturbs the receiver state.
            """
            circuit.h(target_qubit)
            circuit.x(target_qubit)

        return circuit