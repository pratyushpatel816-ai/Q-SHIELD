import csv

from qshield.quantum.teleportation import (
    TeleportationEngine
)


def run_experiment():

    print()
    print("=" * 75)
    print("Q-SHIELD")
    print("PHASE 4A: QUANTUM NOISE ROBUSTNESS EXPERIMENT")
    print("=" * 75)

    noise_levels = [
        0.00,
        0.01,
        0.03,
        0.05,
        0.10,
        0.15,
        0.20
    ]

    bases = ["Z", "X", "Y"]

    results = []

    engine = TeleportationEngine(
        shots=1024
    )

    print()
    print(
        f"{'Noise':<10}"
        f"{'Basis':<10}"
        f"{'Match':<15}"
        f"{'Mismatch':<15}"
        f"{'Fidelity':<15}"
    )

    print("-" * 75)

    for noise_probability in noise_levels:

        for basis in bases:

            result = engine.run(
                bit=0,
                basis=basis,
                noise_type="depolarizing",
                noise_probability=noise_probability,
                attack_type="none"
            )

            row = {
                "noise_probability":
                    noise_probability,

                "basis":
                    basis,

                "match_rate":
                    result["match_rate"],

                "mismatch_rate":
                    result["mismatch_rate"],

                "fidelity_proxy":
                    result["fidelity_proxy"]
            }

            results.append(row)

            print(
                f"{noise_probability:<10.2f}"
                f"{basis:<10}"
                f"{result['match_rate']:<15.6f}"
                f"{result['mismatch_rate']:<15.6f}"
                f"{result['fidelity_proxy']:<15.6f}"
            )

    with open(
        "experiments/noise_results.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "noise_probability",
                "basis",
                "match_rate",
                "mismatch_rate",
                "fidelity_proxy"
            ]
        )

        writer.writeheader()

        writer.writerows(
            results
        )

    print()
    print("=" * 75)
    print(
        "EXPERIMENT COMPLETED"
    )
    print(
        "Results saved to:"
    )
    print(
        "experiments/noise_results.csv"
    )
    print("=" * 75)


if __name__ == "__main__":

    run_experiment()