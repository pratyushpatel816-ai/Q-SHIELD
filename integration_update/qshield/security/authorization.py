class AuthorizationManager:
    """
    Role-Based Access Control for QDS operations.
    """

    VALID_ROLES = {
        "SIGNER",
        "VERIFIER",
        "ADMIN",
        "OBSERVER"
    }

    VERIFY_ROLES = {
        "VERIFIER",
        "ADMIN"
    }

    def __init__(self):

        self.users = {
            "CITY_SECURITY_VERIFIER": {
                "role": "VERIFIER",
                "authorized": True
            },

            "QSHIELD_ADMIN": {
                "role": "ADMIN",
                "authorized": True
            },

            "TRAFFIC_OPERATOR": {
                "role": "OBSERVER",
                "authorized": True
            }
        }

    def register_user(
        self,
        user_id,
        role
    ):

        if role not in self.VALID_ROLES:
            raise ValueError(
                f"Invalid role: {role}"
            )

        self.users[user_id] = {
            "role": role,
            "authorized": True
        }

    def can_verify(
        self,
        user_id
    ):

        user = self.users.get(
            user_id
        )

        if user is None:
            return False

        if not user.get(
            "authorized",
            False
        ):
            return False

        return user["role"] in (
            self.VERIFY_ROLES
        )

    def get_role(
        self,
        user_id
    ):

        user = self.users.get(
            user_id
        )

        if user is None:
            return None

        return user["role"]