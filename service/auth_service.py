
import settings
from crypto.crypto import generate_ecc_signature


def sign_challenge_using_ecc_public_key(challenge):
    ecc_private_key = settings.encryptionKeyPair["eccKeyPair"]["privateKey"]
    return generate_ecc_signature(ecc_private_key, challenge)