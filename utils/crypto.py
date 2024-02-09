import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec, rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature

import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError


def remove_pem_header(pem_content):

    lines = pem_content.splitlines()

    # Remove lines that are headers or footers
    stripped_lines = [
        line
        for line in lines
        if not (line.startswith("-----BEGIN ") or line.startswith("-----END "))
    ]

    # Join the remaining lines back into a single string
    stripped_key = "".join(stripped_lines)

    return stripped_key


def generate_ecc_key_pair():
    # Generate an ECC private key for use in key exchange.
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())

    # Generate the public key for the private key.
    public_key = private_key.public_key()

    # Serialize the private key to PEM format
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")

    # Serialize the public key to PEM format
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("utf-8")

    return private_key_pem, public_key_pem


def generate_rsa_key_pair(key_size=2048):
    # Generate an RSA private key
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=key_size, backend=default_backend()
    )

    # Generate the public key for the private key
    public_key = private_key.public_key()

    # Serialize the private key to PEM format
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")

    # Serialize the public key to PEM format
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("utf-8")

    return private_key_pem, public_key_pem


def sign_message_ecdsa(private_key_pem, message):
    # Load the private key from the PEM file
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode("utf-8"), password=None, backend=default_backend()
    )

    # Sign the message using the private key
    signature = private_key.sign(message.encode("utf-8"), ec.ECDSA(hashes.SHA256()))

    # Decode the signature from DER to (r, s)
    r, s = decode_dss_signature(signature)

    # Convert r and s into 32-byte components
    r_bytes = r.to_bytes(32, byteorder="big")
    s_bytes = s.to_bytes(32, byteorder="big")

    # Concatenate r_bytes and s_bytes to get the 64-byte signature
    signature_64_bytes = r_bytes + s_bytes

    signature_base64 = base64.b64encode(signature_64_bytes).decode("utf-8")

    return signature_base64


def is_valid_jwt(token, secret_key):
    """Check if the JWT token is valid."""
    try:
        jwt.decode(token, secret_key, algorithms=["HS256"])
        return True
    except (DecodeError, ExpiredSignatureError):
        # If there's a decode error or the token is expired, it's not a valid JWT
        return False
