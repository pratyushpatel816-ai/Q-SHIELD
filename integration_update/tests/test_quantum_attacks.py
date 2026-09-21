from qshield.quantum.teleportation import (
    TeleportationEngine
)


def test_no_attack_high_fidelity():

    engine = TeleportationEngine(
        shots=512
    )

    result = engine.run(
        bit=0,
        basis="Z",
        attack_type="none"
    )

    assert result["fidelity_proxy"] > 0.95


def test_pauli_x_detected_z_basis():

    engine = TeleportationEngine(
        shots=512
    )

    clean = engine.run(
        bit=0,
        basis="Z",
        attack_type="none"
    )

    attacked = engine.run(
        bit=0,
        basis="Z",
        attack_type="pauli_x"
    )

    assert (
        attacked["match_rate"]
        < clean["match_rate"]
    )


def test_pauli_z_detected_x_basis():

    engine = TeleportationEngine(
        shots=512
    )

    clean = engine.run(
        bit=0,
        basis="X",
        attack_type="none"
    )

    attacked = engine.run(
        bit=0,
        basis="X",
        attack_type="pauli_z"
    )

    assert (
        attacked["match_rate"]
        < clean["match_rate"]
    )


def test_pauli_y_detected_z_basis():

    engine = TeleportationEngine(
        shots=512
    )

    attacked = engine.run(
        bit=0,
        basis="Z",
        attack_type="pauli_y"
    )

    assert attacked["mismatch_rate"] > 0.5


def test_attack_metadata():

    engine = TeleportationEngine(
        shots=128
    )

    result = engine.run(
        bit=0,
        basis="Z",
        attack_type="pauli_x"
    )

    assert result["attack_type"] == (
        "pauli_x"
    )