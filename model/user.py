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

        self.ecc_private_key = None
        self.ecc_public_key = None

        self.rsa_private_key = None
        self.rsa_public_key = None

        self.token = None

    def __repr__(self):
        return self.username
