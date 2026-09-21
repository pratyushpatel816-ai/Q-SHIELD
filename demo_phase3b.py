from qshield.quantum.teleportation import (
    TeleportationEngine
)


def separator():
    print("\n" + "=" * 75)


def main():

    print("\nQ-SHIELD")
    print("PHASE 3B: QUANTUM ATTACK SIMULATION")

    separator()

    engine = TeleportationEngine(
        shots=1024
    )

    attacks = [
        "none",
        "pauli_x",
        "pauli_y",
        "pauli_z",
        "entanglement_disruption"
    ]

    # Test across different Pauli bases
    test_cases = [
        (0, "Z"),
        (0, "X"),
        (0, "Y")
    ]

    results = []

    for bit, basis in test_cases:

        print(
            f"\nINPUT STATE | "
            f"Bit={bit} | Basis={basis}"
        )

        print("-" * 75)

        for attack in attacks:

            result = engine.run(
                bit=bit,
                basis=basis,
                attack_type=attack
            )

            results.append({
                "basis": basis,
                "attack": attack,
                "match_rate":
                    result["match_rate"],
                "mismatch_rate":
                    result["mismatch_rate"],
                "fidelity":
                    result["fidelity_proxy"]
            })

            print(
                f"{attack.upper():<28} | "
                f"Match: {result['match_rate']:.4f} | "
                f"Mismatch: {result['mismatch_rate']:.4f} | "
                f"Fidelity: {result['fidelity_proxy']:.4f}"
            )

    separator()

    print("PHASE 3B ATTACK SIMULATION COMPLETED")

    separator()


if __name__ == "__main__":
    main()