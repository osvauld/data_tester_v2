import settings

from api.auth_api import create_challenge, verify_user
from service.auth_service import sign_challenge_using_ecc_public_key


def authenticate_dummy_user():
    publicKey = settings.encryptionKeyPair.eccKeyPair.publicKey
    challenge = create_challenge(publicKey)
    signedChallenge = sign_challenge_using_ecc_public_key(challenge)
    token = verify_user(signedChallenge,settings.encryptionKeyPair.eccKeyPair.publicKey)
    return token