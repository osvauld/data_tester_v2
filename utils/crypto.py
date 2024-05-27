import base64
import hashlib
import json
import shutil
import tempfile

import gnupg
import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError

GPG_PASSPHRASE = "passphrase"


def generate_device_key():

    temp_dir = tempfile.mkdtemp()
    gpg = gnupg.GPG(gnupghome=temp_dir)

    try:
        input_data = gpg.gen_key_input(
            name_email="user@email.com",
            passphrase=GPG_PASSPHRASE,
        )
        key = gpg.gen_key(input_data)

        armored_public_key = gpg.export_keys(key.fingerprint)
        armored_public_key_b64 = base64.b64encode(
            armored_public_key.encode("utf-8")
        ).decode("utf-8")

        armored_private_key = gpg.export_keys(
            key.fingerprint, secret=True, passphrase=GPG_PASSPHRASE
        )
        armored_private_key_b64 = base64.b64encode(
            armored_private_key.encode("utf-8")
        ).decode("utf-8")

        return armored_public_key_b64, armored_private_key_b64

    finally:
        shutil.rmtree(temp_dir)


def sign_message(armored_private_key, message):

    temp_dir = tempfile.mkdtemp()
    gpg = gnupg.GPG(gnupghome=temp_dir)

    armored_private_key_decoded = base64.b64decode(
        armored_private_key.encode("utf-8")
    ).decode("utf-8")

    try:
        import_result = gpg.import_keys(armored_private_key_decoded)
        if not import_result.count:
            raise ValueError("Failed to import the private key.")

        signed_message = gpg.sign(
            message,
            passphrase=GPG_PASSPHRASE,
            keyid=import_result.fingerprints[0],
            detach=True,
        )
        armored_signature_b64 = base64.b64encode(
            str(signed_message).encode("utf-8")
        ).decode("utf-8")

        shutil.rmtree(temp_dir)

    finally:

        return armored_signature_b64


def is_valid_jwt(token, secret_key):
    """Check if the JWT token is valid."""
    try:
        jwt.decode(token, secret_key, algorithms=["HS256"])
        return True
    except (DecodeError, ExpiredSignatureError):
        # If there's a decode error or the token is expired, it's not a valid JWT
        return False


def encrypt_text(text: str, public_key: str):

    # TODO: add encryption

    return text


def hash_and_sign(json_data, private_key):

    payload_string = json.dumps(json_data)
    encoded_payload = base64.b64encode(payload_string.encode("utf-8")).decode("utf-8")
    hash_object = hashlib.sha512(encoded_payload.encode("utf-8"))
    hashed_payload = base64.b64encode(hash_object.digest()).decode("utf-8")
    signature = sign_message(private_key, hashed_payload)
    return signature


generate_device_key()
