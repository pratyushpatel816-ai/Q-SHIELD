from qiskit_aer.noise import (
    NoiseModel,
    pauli_error,
    depolarizing_error,
    ReadoutError
)


class NoiseFactory:

    @staticmethod
    def none():
        return None

    @staticmethod
    def bit_flip(probability=0.05):

        noise_model = NoiseModel()

        error = pauli_error([
            ("X", probability),
            ("I", 1 - probability)
        ])

        noise_model.add_all_qubit_quantum_error(
            error,
            ["id", "x", "h"]
        )

        return noise_model

    @staticmethod
    def phase_flip(probability=0.05):

        noise_model = NoiseModel()

        error = pauli_error([
            ("Z", probability),
            ("I", 1 - probability)
        ])

        noise_model.add_all_qubit_quantum_error(
            error,
            ["id", "x", "h"]
        )

        return noise_model

    @staticmethod
    def bit_phase_flip(probability=0.05):

        noise_model = NoiseModel()

        error = pauli_error([
            ("Y", probability),
            ("I", 1 - probability)
        ])

        noise_model.add_all_qubit_quantum_error(
            error,
            ["id", "x", "h"]
        )

        return noise_model

    @staticmethod
    def depolarizing(probability=0.05):

        noise_model = NoiseModel()

        error = depolarizing_error(
            probability,
            1
        )

        noise_model.add_all_qubit_quantum_error(
            error,
            ["id", "x", "h", "s"]
        )

        return noise_model

    @staticmethod
    def readout_error(probability=0.05):

        noise_model = NoiseModel()

        error = ReadoutError([
            [1 - probability, probability],
            [probability, 1 - probability]
        ])

        noise_model.add_all_qubit_readout_error(error)

        return noise_model

    @staticmethod
    def get_noise(
        noise_type="none",
        probability=0.0
    ):

        noise_type = noise_type.lower()

        if noise_type == "none":
            return None

        if noise_type == "bit_flip":
            return NoiseFactory.bit_flip(probability)

        if noise_type == "phase_flip":
            return NoiseFactory.phase_flip(probability)

        if noise_type == "bit_phase_flip":
            return NoiseFactory.bit_phase_flip(probability)

        if noise_type == "depolarizing":
            return NoiseFactory.depolarizing(probability)

        if noise_type == "readout":
            return NoiseFactory.readout_error(probability)

        raise ValueError(
            f"Unknown noise type: {noise_type}"
        )