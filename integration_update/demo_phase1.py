from qshield.quantum.teleportation import (
    TeleportationEngine
)

from qshield.quantum.bell import (
    BellPairAnalyzer
)


def print_separator():
    print("\n" + "=" * 60)


def main():

    print_separator()

    print("Q-SHIELD")
    print("PHASE 1: QUANTUM TELEPORTATION ENGINE")

    print_separator()

    # ---------------------------------------
    # BELL PAIR TEST
    # ---------------------------------------

    print("\n[1] BELL PAIR CORRELATION TEST")

    bell = BellPairAnalyzer(shots=1024)

    bell_result = bell.correlation_test()

    print("Counts:")
    print(bell_result["counts"])

    print(
        "Correlation Rate:",
        bell_result["correlation_rate"]
    )

    print(
        "Channel Healthy:",
        bell_result["healthy"]
    )

    # ---------------------------------------
    # TELEPORTATION TEST
    # ---------------------------------------

    engine = TeleportationEngine(
        shots=2048
    )

    test_cases = [
        (0, "Z"),
        (1, "Z"),
        (0, "X"),
        (1, "X"),
        (0, "Y"),
        (1, "Y")
    ]

    print_separator()

    print("[2] PAULI EIGENSTATE TELEPORTATION")

    for bit, basis in test_cases:

        result = engine.run(
            bit=bit,
            basis=basis,
            noise_type="none"
        )

        print_separator()

        print(
            f"State: {result['expected_state']}"
        )

        print(
            f"Basis: {result['basis']}"
        )

        print(
            f"Expected Bit: "
            f"{result['expected_bit']}"
        )

        print(
            f"Match Rate: "
            f"{result['match_rate']}"
        )

        print(
            f"Mismatch Rate: "
            f"{result['mismatch_rate']}"
        )

        print(
            f"Fidelity Proxy: "
            f"{result['fidelity_proxy']}"
        )

    # ---------------------------------------
    # NOISE DEMONSTRATION
    # ---------------------------------------

    print_separator()

    print("[3] DEPOLARIZING NOISE TEST")

    clean = engine.run(
        bit=0,
        basis="X",
        noise_type="none"
    )

    noisy = engine.run(
        bit=0,
        basis="X",
        noise_type="depolarizing",
        noise_probability=0.10
    )

    print("\nCLEAN CHANNEL")
    print(
        "Mismatch:",
        clean["mismatch_rate"]
    )

    print(
        "Fidelity:",
        clean["fidelity_proxy"]
    )

    print("\nNOISY CHANNEL")
    print(
        "Mismatch:",
        noisy["mismatch_rate"]
    )

    print(
        "Fidelity:",
        noisy["fidelity_proxy"]
    )

    print_separator()

    print(
        "PHASE 1 DEMONSTRATION COMPLETED"
    )


if __name__ == "__main__":
    main()