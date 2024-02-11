from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature

import base64

def generate_ecc_signature(private_key, message):
    private_key_pem = f"""-----BEGIN EC PRIVATE KEY-----
{private_key}
-----END EC PRIVATE KEY-----"""
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode('utf-8'),
        password=None,  # No password
    )
    if isinstance(message, str):
        message = message.encode('utf-8')
    
    signature_der = private_key.sign(
        message,
        ec.ECDSA(hashes.SHA256())
    )

    r, s = decode_dss_signature(signature_der)
    
    # Ensure r and s are 32 bytes each, pad with zeros if necessary
    r_bytes = r.to_bytes(32, byteorder='big')
    s_bytes = s.to_bytes(32, byteorder='big')
    
    # Concatenate r and s for a fixed-length 64-byte signature
    fixed_length_signature = r_bytes + s_bytes

    signature_str = base64.b64encode(fixed_length_signature).decode('utf-8')

    return signature_str

