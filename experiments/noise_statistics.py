import csv
import statistics

from qshield.quantum.teleportation import (
    TeleportationEngine
)


def run_statistical_experiment():

    print()
    print("=" * 80)
    print("Q-SHIELD")
    print("PHASE 4B: STATISTICAL QUANTUM NOISE ANALYSIS")
    print("=" * 80)

    noise_levels = [
        0.00,
        0.01,
        0.03,
        0.05,
        0.10,
        0.15,
        0.20
    ]

    bases = [
        "Z",
        "X",
        "Y"
    ]

    trials = 20

    engine = TeleportationEngine(
        shots=1024
    )

    results = []

    print()
    print(
        f"{'Noise':<10}"
        f"{'Basis':<8}"
        f"{'Mean Fidelity':<18}"
        f"{'Std Dev':<15}"
        f"{'Mean Mismatch':<18}"
    )

    print("-" * 80)

    for noise_probability in noise_levels:

        for basis in bases:

            fidelity_values = []
            mismatch_values = []

            for trial in range(trials):

                result = engine.run(
                    bit=0,
                    basis=basis,
                    noise_type="depolarizing",
                    noise_probability=noise_probability,
                    attack_type="none"
                )

                fidelity_values.append(
                    result["fidelity_proxy"]
                )

                mismatch_values.append(
                    result["mismatch_rate"]
                )

            mean_fidelity = statistics.mean(
                fidelity_values
            )

            std_fidelity = statistics.stdev(
                fidelity_values
            )

            mean_mismatch = statistics.mean(
                mismatch_values
            )

            row = {
                "noise_probability":
                    noise_probability,

                "basis":
                    basis,

                "trials":
                    trials,

                "mean_fidelity":
                    round(mean_fidelity, 6),

                "std_fidelity":
                    round(std_fidelity, 6),

                "min_fidelity":
                    round(
                        min(fidelity_values),
                        6
                    ),

                "max_fidelity":
                    round(
                        max(fidelity_values),
                        6
                    ),

                "mean_mismatch":
                    round(mean_mismatch, 6)
            }

            results.append(row)

            print(
                f"{noise_probability:<10.2f}"
                f"{basis:<8}"
                f"{mean_fidelity:<18.6f}"
                f"{std_fidelity:<15.6f}"
                f"{mean_mismatch:<18.6f}"
            )

    with open(
        "experiments/noise_statistics.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "noise_probability",
                "basis",
                "trials",
                "mean_fidelity",
                "std_fidelity",
                "min_fidelity",
                "max_fidelity",
                "mean_mismatch"
            ]
        )

        writer.writeheader()

        writer.writerows(
            results
        )

    print()
    print("=" * 80)
    print("STATISTICAL EXPERIMENT COMPLETED")
    print(
        f"Total configurations: {len(results)}"
    )
    print(
        f"Trials per configuration: {trials}"
    )
    print(
        f"Total experiment runs: "
        f"{len(results) * trials}"
    )
    print()
    print(
        "Results saved to:"
    )
    print(
        "experiments/noise_statistics.csv"
    )
    print("=" * 80)


if __name__ == "__main__":

    run_statistical_experiment()