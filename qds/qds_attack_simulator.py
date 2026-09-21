import copy


class QDSAttackSimulator:
    """
    Simulates cyber threats against the QDS workflow.

    Supported attacks:

    - forgery
    - impersonation
    - replay
    - unauthorized_verification
    - quantum_channel_manipulation
    """

    @staticmethod
    def apply_attack(
        signature,
        attack_type="none"
    ):

        attacked_signature = copy.deepcopy(
            signature
        )

        attack_metadata = {

            "attack_type":
                attack_type,

            "attacked":
                False,

            "description":
                "No attack applied"
        }

        # -----------------------------------------
        # NO ATTACK
        # -----------------------------------------

        if attack_type == "none":

            return (
                attacked_signature,
                attack_metadata
            )

        # -----------------------------------------
        # SIGNATURE FORGERY
        # -----------------------------------------

        elif attack_type == "forgery":

            attacked_signature[
                "signature_valid"
            ] = False

            attacked_signature[
                "message"
            ] = (
                attacked_signature["message"]
                + " [MODIFIED]"
            )

            attack_metadata = {

                "attack_type":
                    "forgery",

                "attacked":
                    True,

                "description":
                    "Digital signature forgery and "
                    "message modification simulated"
            }

        # -----------------------------------------
        # IMPERSONATION
        # -----------------------------------------

        elif attack_type == "impersonation":

            attacked_signature[
                "signer_id"
            ] = "ATTACKER"

            attacked_signature[
                "signature_valid"
            ] = False

            attack_metadata = {

                "attack_type":
                    "impersonation",

                "attacked":
                    True,

                "description":
                    "Unauthorized entity attempted "
                    "to impersonate legitimate signer"
            }

        # -----------------------------------------
        # REPLAY
        # -----------------------------------------

        elif attack_type == "replay":

            attack_metadata = {

                "attack_type":
                    "replay",

                "attacked":
                    True,

                "description":
                    "Previously transmitted signature "
                    "is replayed"
            }

        # -----------------------------------------
        # UNAUTHORIZED VERIFICATION
        # -----------------------------------------

        elif (
            attack_type
            == "unauthorized_verification"
        ):

            attack_metadata = {

                "attack_type":
                    "unauthorized_verification",

                "attacked":
                    True,

                "description":
                    "Unauthorized verifier attempted "
                    "signature verification"
            }

        else:

            raise ValueError(
                f"Unsupported QDS attack: "
                f"{attack_type}"
            )

        return (
            attacked_signature,
            attack_metadata
        )