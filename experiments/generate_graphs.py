import pandas as pd
import matplotlib.pyplot as plt


def generate_graphs():

    print()
    print("=" * 70)
    print("Q-SHIELD")
    print("PHASE 4C: EXPERIMENTAL RESULTS VISUALIZATION")
    print("=" * 70)

    data = pd.read_csv(
        "experiments/noise_statistics.csv"
    )

    bases = ["Z", "X", "Y"]

    # ============================================================
    # GRAPH 1: FIDELITY VS NOISE
    # ============================================================

    plt.figure(figsize=(8, 5))

    for basis in bases:

        subset = data[
            data["basis"] == basis
        ]

        plt.errorbar(
            subset["noise_probability"],
            subset["mean_fidelity"],
            yerr=subset["std_fidelity"],
            marker="o",
            capsize=4,
            label=f"{basis}-Basis"
        )

    plt.xlabel(
        "Depolarizing Noise Probability"
    )

    plt.ylabel(
        "Mean Teleportation Fidelity"
    )

    plt.title(
        "Q-SHIELD: Fidelity Under Depolarizing Noise"
    )

    plt.grid(True)

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        "experiments/fidelity_vs_noise.png",
        dpi=300
    )

    plt.close()

    # ============================================================
    # GRAPH 2: MISMATCH RATE VS NOISE
    # ============================================================

    plt.figure(figsize=(8, 5))

    for basis in bases:

        subset = data[
            data["basis"] == basis
        ]

        plt.plot(
            subset["noise_probability"],
            subset["mean_mismatch"],
            marker="o",
            label=f"{basis}-Basis"
        )

    plt.xlabel(
        "Depolarizing Noise Probability"
    )

    plt.ylabel(
        "Mean Mismatch Rate"
    )

    plt.title(
        "Q-SHIELD: Quantum State Mismatch Under Noise"
    )

    plt.grid(True)

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        "experiments/mismatch_vs_noise.png",
        dpi=300
    )

    plt.close()

    # ============================================================
    # GRAPH 3: BASIS ROBUSTNESS COMPARISON
    # ============================================================

    high_noise = data[
        data["noise_probability"] == 0.20
    ]

    plt.figure(figsize=(7, 5))

    plt.bar(
        high_noise["basis"],
        high_noise["mean_fidelity"]
    )

    plt.xlabel(
        "Measurement Basis"
    )

    plt.ylabel(
        "Mean Fidelity"
    )

    plt.title(
        "Q-SHIELD: Basis Robustness at Noise = 0.20"
    )

    plt.ylim(
        0,
        1.05
    )

    plt.tight_layout()

    plt.savefig(
        "experiments/basis_robustness.png",
        dpi=300
    )

    plt.close()

    print()
    print("Graphs generated successfully:")
    print(
        "1. experiments/fidelity_vs_noise.png"
    )
    print(
        "2. experiments/mismatch_vs_noise.png"
    )
    print(
        "3. experiments/basis_robustness.png"
    )

    print()
    print("=" * 70)
    print("PHASE 4C COMPLETED")
    print("=" * 70)


if __name__ == "__main__":

    generate_graphs()