from qshield.quantum.teleportation import (
    TeleportationEngine
)

from qshield.security.threat_detector import (
    QuantumThreatDetector
)


def generate_probe_results(
    attack_type
):

    engine = TeleportationEngine(
        shots=256
    )

    probes = [
        (0, "Z"),
        (1, "Z"),
        (0, "X"),
        (1, "X"),
        (0, "Y"),
        (1, "Y")
    ]

    results = []

    for bit, basis in probes:

        result = engine.run(
            bit=bit,
            basis=basis,
            attack_type=attack_type
        )

        results.append(result)

    return results


def test_clean_channel_accepted():

    detector = QuantumThreatDetector()

    results = generate_probe_results(
        "none"
    )

    analysis = detector.analyze(
        results
    )

    assert analysis["decision"] == "ACCEPT"


def test_pauli_x_rejected():

    detector = QuantumThreatDetector()

    results = generate_probe_results(
        "pauli_x"
    )

    analysis = detector.analyze(
        results
    )

    assert analysis["decision"] == "REJECT"


def test_pauli_y_rejected():

    detector = QuantumThreatDetector()

    results = generate_probe_results(
        "pauli_y"
    )

    analysis = detector.analyze(
        results
    )

    assert analysis["decision"] == "REJECT"


def test_pauli_z_rejected():

    detector = QuantumThreatDetector()

    results = generate_probe_results(
        "pauli_z"
    )

    analysis = detector.analyze(
        results
    )

    assert analysis["decision"] == "REJECT"


def test_basis_summary_present():

    detector = QuantumThreatDetector()

    results = generate_probe_results(
        "none"
    )

    analysis = detector.analyze(
        results
    )

    summary = (
        analysis["evidence"]
        ["basis_summary"]
    )

    assert "X" in summary
    assert "Y" in summary
    assert "Z" in summary


def test_invalid_thresholds():

    try:

        QuantumThreatDetector(
            warn_threshold=0.20,
            reject_threshold=0.10
        )

        assert False

    except ValueError:

        assert True