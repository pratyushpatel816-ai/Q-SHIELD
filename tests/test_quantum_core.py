import pytest

from qshield.quantum.teleportation import (
    TeleportationEngine
)

from qshield.quantum.bell import (
    BellPairAnalyzer
)


@pytest.fixture
def engine():
    return TeleportationEngine(shots=1024)


@pytest.mark.parametrize(
    "bit,basis",
    [
        (0, "Z"),
        (1, "Z"),
        (0, "X"),
        (1, "X"),
        (0, "Y"),
        (1, "Y")
    ]
)
def test_all_pauli_eigenstates(
    engine,
    bit,
    basis
):

    result = engine.run(
        bit=bit,
        basis=basis
    )

    assert result["match_rate"] > 0.95


def test_bell_pair_correlation():

    analyzer = BellPairAnalyzer(
        shots=1024
    )

    result = analyzer.correlation_test()

    assert result["correlation_rate"] > 0.95


def test_noise_increases_error(engine):

    clean = engine.run(
        bit=0,
        basis="Z",
        noise_type="none"
    )

    noisy = engine.run(
        bit=0,
        basis="Z",
        noise_type="depolarizing",
        noise_probability=0.10
    )

    assert (
        noisy["mismatch_rate"]
        >= clean["mismatch_rate"]
    )