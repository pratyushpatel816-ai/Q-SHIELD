class IdentityRegistry:
    """
    Maintains registered entities in the Q-SHIELD ecosystem.

    Prototype implementation uses an in-memory registry.
    Later this will be migrated to SQLite/PostgreSQL.
    """

    def __init__(self):

        self.senders = {
            "CITY_CONTROL_CENTER": {
                "role": "SIGNER",
                "authorized": True
            }
        }

        self.receivers = {
            "TRAFFIC_GATEWAY_01": {
                "role": "RECEIVER",
                "authorized": True
            }
        }

        self.devices = {
            "SMART_TRAFFIC_GATEWAY_01": {
                "authorized": True
            }
        }

    def register_sender(
        self,
        sender_id,
        role="SIGNER"
    ):

        self.senders[sender_id] = {
            "role": role,
            "authorized": True
        }

    def register_receiver(
        self,
        receiver_id
    ):

        self.receivers[receiver_id] = {
            "role": "RECEIVER",
            "authorized": True
        }

    def register_device(
        self,
        device_id
    ):

        self.devices[device_id] = {
            "authorized": True
        }

    def validate_sender(
        self,
        sender_id
    ):

        sender = self.senders.get(
            sender_id
        )

        if sender is None:
            return False

        return sender.get(
            "authorized",
            False
        )

    def validate_receiver(
        self,
        receiver_id
    ):

        receiver = self.receivers.get(
            receiver_id
        )

        if receiver is None:
            return False

        return receiver.get(
            "authorized",
            False
        )

    def validate_device(
        self,
        device_id
    ):

        device = self.devices.get(
            device_id
        )

        if device is None:
            return False

        return device.get(
            "authorized",
            False
        )