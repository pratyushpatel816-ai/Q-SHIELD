from experiments.qshield_qds_security_demo import (
    QShieldQDSSecuritySystem
)


# ============================================================
# HELPER FUNCTION
# ============================================================

def print_result(result):

    print(
        f"Final Decision: "
        f"{result['final_decision']}"
    )

    print(
        f"QDS Attack: "
        f"{result['qds_attack']['attack_type']}"
    )

    print(
        f"QDS Verification: "
        f"{result['qds_verification']['final_decision']}"
    )

    print(
        f"Q-SHIELD Decision: "
        f"{result['qshield_result']['decision']}"
    )

    print(
        f"Severity: "
        f"{result['qshield_result']['severity']}"
    )

    print(
        f"Security Score: "
        f"{result['qshield_result']['security_score']}"
    )

    print(
        f"Adaptive Threshold: "
        f"{result['qshield_result']['adaptive_threshold']}"
    )


# ============================================================
# MAIN VALIDATION
# ============================================================

def main():

    system = QShieldQDSSecuritySystem(
        shots=1024
    )

    # ========================================================
    # SCENARIO 1
    # LEGITIMATE QDS COMMUNICATION
    # ========================================================

    print("=" * 70)
    print("SCENARIO 1: LEGITIMATE QDS COMMUNICATION")
    print("=" * 70)

    result = system.run(
        message="INSTALL_FIRMWARE",
        signer_id="ALICE",
        authorized_verifiers=["BOB"],
        verifier_id="BOB",
        qds_attack="none",
        quantum_attack="none",
        noise_type="none",
        noise_probability=0.0
    )

    print_result(result)

    assert (
        result["qds_verification"]["final_decision"]
        == "ACCEPT"
    )

    assert (
        result["qshield_result"]["decision"]
        == "NORMAL"
    )

    assert (
        result["final_decision"]
        == "SECURE COMMUNICATION"
    )

    print("Scenario 1 validation: PASSED")
    print()


    # ========================================================
    # SCENARIO 2
    # LEGITIMATE NOISY CHANNEL
    # ========================================================

    print("=" * 70)
    print("SCENARIO 2: LEGITIMATE NOISY CHANNEL")
    print("=" * 70)

    result = system.run(
        message="INSTALL_FIRMWARE",
        signer_id="ALICE",
        authorized_verifiers=["BOB"],
        verifier_id="BOB",
        qds_attack="none",
        quantum_attack="none",
        noise_type="depolarizing",
        noise_probability=0.10
    )

    print_result(result)

    assert (
        result["qds_verification"]["final_decision"]
        == "ACCEPT"
    )

    assert (
        result["final_decision"]
        == "SECURE COMMUNICATION"
    )

    print("Scenario 2 validation: PASSED")
    print()


    # ========================================================
    # SCENARIO 3
    # DIGITAL SIGNATURE FORGERY
    # ========================================================

    print("=" * 70)
    print("SCENARIO 3: DIGITAL SIGNATURE FORGERY")
    print("=" * 70)

    result = system.run(
        message="INSTALL_FIRMWARE",
        signer_id="ALICE",
        authorized_verifiers=["BOB"],
        verifier_id="BOB",
        qds_attack="forgery",
        quantum_attack="none",
        noise_type="none",
        noise_probability=0.0
    )

    print_result(result)

    assert (
        result["qds_verification"]["final_decision"]
        == "REJECT"
    )

    assert (
        result["final_decision"]
        == "SECURITY THREAT DETECTED"
    )

    print("Scenario 3 validation: PASSED")
    print()


    # ========================================================
    # SCENARIO 4
    # SIGNER IMPERSONATION
    # ========================================================

    print("=" * 70)
    print("SCENARIO 4: SIGNER IMPERSONATION")
    print("=" * 70)

    result = system.run(
        message="INSTALL_FIRMWARE",
        signer_id="ALICE",
        authorized_verifiers=["BOB"],
        verifier_id="BOB",
        qds_attack="impersonation",
        quantum_attack="none",
        noise_type="none",
        noise_probability=0.0
    )

    print_result(result)

    assert (
        result["qds_verification"]["final_decision"]
        == "REJECT"
    )

    assert (
        result["final_decision"]
        == "SECURITY THREAT DETECTED"
    )

    print("Scenario 4 validation: PASSED")
    print()


    # ========================================================
    # SCENARIO 5
    # REPLAY ATTACK
    # ========================================================

    print("=" * 70)
    print("SCENARIO 5: REPLAY ATTACK")
    print("=" * 70)

    replay_system = QShieldQDSSecuritySystem(
        shots=1024
    )

    # --------------------------------------------------------
    # Generate ONE signature
    # --------------------------------------------------------

    signature = (
        replay_system.qds_protocol.generate_signature(
            message="INSTALL_FIRMWARE",
            signer_id="ALICE",
            authorized_verifiers=["BOB"]
        )
    )

    # --------------------------------------------------------
    # FIRST VERIFICATION
    # --------------------------------------------------------

    first_verification = (
        replay_system.qds_protocol.verify_signature(
            signature,
            verifier_id="BOB"
        )
    )

    print(
        f"First verification: "
        f"{first_verification['final_decision']}"
    )

    # --------------------------------------------------------
    # REPLAY THE EXACT SAME SIGNATURE
    # --------------------------------------------------------

    second_verification = (
        replay_system.qds_protocol.verify_signature(
            signature,
            verifier_id="BOB"
        )
    )

    print(
        f"Second verification: "
        f"{second_verification['final_decision']}"
    )

    print(
        f"Replay detected: "
        f"{second_verification['replay_detected']}"
    )

    # --------------------------------------------------------
    # REPLAY VALIDATION
    # --------------------------------------------------------

    assert (
        first_verification["final_decision"]
        == "ACCEPT"
    )

    assert (
        second_verification["final_decision"]
        == "REJECT"
    )

    assert (
        second_verification["replay_detected"]
        is True
    )

    print("Replay validation: PASSED")
    print()


    # ========================================================
    # SCENARIO 6
    # UNAUTHORIZED VERIFICATION
    # ========================================================

    print("=" * 70)
    print("SCENARIO 6: UNAUTHORIZED VERIFICATION")
    print("=" * 70)

    result = system.run(
        message="INSTALL_FIRMWARE",
        signer_id="ALICE",
        authorized_verifiers=["BOB"],
        verifier_id="EVE",
        qds_attack="unauthorized_verification",
        quantum_attack="none",
        noise_type="none",
        noise_probability=0.0
    )

    print_result(result)

    assert (
        result["qds_verification"]["final_decision"]
        == "REJECT"
    )

    assert (
        result["final_decision"]
        == "SECURITY THREAT DETECTED"
    )

    print("Scenario 6 validation: PASSED")
    print()


    # ========================================================
    # SCENARIO 7
    # QUANTUM CHANNEL MANIPULATION
    # ========================================================

    print("=" * 70)
    print("SCENARIO 7: QUANTUM CHANNEL MANIPULATION")
    print("=" * 70)

    result = system.run(
        message="INSTALL_FIRMWARE",
        signer_id="ALICE",
        authorized_verifiers=["BOB"],
        verifier_id="BOB",
        qds_attack="none",
        quantum_attack="pauli_x",
        noise_type="none",
        noise_probability=0.0
    )

    print_result(result)

    assert (
        result["qds_verification"]["final_decision"]
        == "ACCEPT"
    )

    assert (
        result["qshield_result"]["attack_detected"]
        is True
    )

    assert (
        result["final_decision"]
        == "SECURITY THREAT DETECTED"
    )

    print("Scenario 7 validation: PASSED")
    print()


    # ========================================================
    # FINAL SIH MATRIX VALIDATION
    # ========================================================

    print("=" * 70)
    print("SIH ATTACK MATRIX VALIDATION")
    print("=" * 70)

    print()
    print("1/7  Legitimate QDS Communication       : PASSED")
    print("2/7  Legitimate Noisy Channel            : PASSED")
    print("3/7  Digital Signature Forgery           : PASSED")
    print("4/7  Signer Impersonation                : PASSED")
    print("5/7  Replay Attack                       : PASSED")
    print("6/7  Unauthorized Verification           : PASSED")
    print("7/7  Quantum Channel Manipulation        : PASSED")

    print()
    print("=" * 70)
    print("SIH ATTACK MATRIX: 7/7 COMPLETE")
    print("Q-SHIELD QDS VALIDATION: PASSED")
    print("=" * 70)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()