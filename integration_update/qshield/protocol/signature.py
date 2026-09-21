from qshield.quantum.teleportation import (
    TeleportationEngine
)

from .payload import CanonicalPayload


class SignatureGenerator:
    """
    Generates a teleportation-based QDS signature.

    The classical payload is bound to a SHA-256 hash.
    Hash bits deterministically generate Pauli basis
    and eigenstate schedules.
    """

    VALID_LENGTHS = [
        8,
        16,
        32,
        64,
        128
    ]

    BASIS_MAPPING = {
        "00": "Z",
        "01": "X",
        "10": "Y",
        "11": "Z"
    }

    def __init__(self, shots=256):

        self.shots = shots

        self.quantum_engine = TeleportationEngine(
            shots=shots
        )

    @staticmethod
    def hex_to_binary(hex_hash):

        return bin(
            int(hex_hash, 16)
        )[2:].zfill(
            len(hex_hash) * 4
        )

    def derive_schedule(
        self,
        payload_hash,
        signature_length
    ):
        """
        Derive deterministic quantum signature schedule.

        Each position contains:
        - basis
        - logical bit
        """

        if signature_length not in self.VALID_LENGTHS:

            raise ValueError(
                f"Signature length must be one of "
                f"{self.VALID_LENGTHS}"
            )

        binary_hash = self.hex_to_binary(
            payload_hash
        )

        schedule = []

        hash_length = len(binary_hash)

        for position in range(signature_length):

            start = (
                position * 3
            ) % hash_length

            bits = ""

            for offset in range(3):

                index = (
                    start + offset
                ) % hash_length

                bits += binary_hash[index]

            basis_bits = bits[:2]
            state_bit = int(bits[2])

            basis = self.BASIS_MAPPING[
                basis_bits
            ]

            schedule.append({
                "position": position,
                "basis": basis,
                "bit": state_bit
            })

        return schedule

    def generate(
        self,
        payload,
        signature_length=16
    ):
        """
        Generate complete QDS signature.
        """

        payload_hash = (
            CanonicalPayload.hash_payload(
                payload
            )
        )

        schedule = self.derive_schedule(
            payload_hash,
            signature_length
        )

        positions = []

        for item in schedule:

            quantum_result = (
                self.quantum_engine.run(
                    bit=item["bit"],
                    basis=item["basis"],
                    noise_type="none"
                )
            )

            positions.append({
                "position": item["position"],
                "basis": item["basis"],
                "expected_bit": item["bit"],
                "expected_state":
                    quantum_result[
                        "expected_state"
                    ],
                "generation_match_rate":
                    quantum_result[
                        "match_rate"
                    ],
                "generation_fidelity_proxy":
                    quantum_result[
                        "fidelity_proxy"
                    ]
            })

        signature = {
            "signature_type":
                "Q-SHIELD_TELEPORTATION_QDS",

            "signature_length":
                signature_length,

            "payload_hash":
                payload_hash,

            "session_id":
                payload["session_id"],

            "sender_id":
                payload["sender_id"],

            "positions":
                positions
        }

        return signature