class User:
    def __init__(
        self,
        username,
        user_id=None,
        name=None,
    ):
        self.user_id = user_id
        self.name = name
        self.username = username

        self.device_public_key = None
        self.device_private_key = None

        self.encryption_private_key = None
        self.encryption_public_key = None

        self.token = None

    def __repr__(self):
        return self.username
