import requests
import settings

from utils.api_validator import check_api_success
from utils.crypto import remove_pem_header


def create_user_api(name, username, temp_password):
    api_url = f"{settings.API_BASE_URL}/user"

    payload = {
        "name": name,
        "username": username,
        "tempPassword": temp_password,
    }

    response = requests.post(api_url, json=payload)
    response.raise_for_status()

    response_json = response.json()
    if not check_api_success(response_json):
        raise ValueError("API response is not successful")

    return response.json()


def register_user_api(user, temp_password):

    api_url = f"{settings.API_BASE_URL}/user/register"

    payload = {
        "username": user.username,
        "password": temp_password,
        "eccKey": remove_pem_header(user.ecc_public_key),
        "rsaKey": remove_pem_header(user.rsa_public_key),
    }

    response = requests.post(api_url, json=payload)
    response.raise_for_status()

    response_json = response.json()
    if not check_api_success(response_json):
        raise ValueError("API response is not successful")

    return response.json()


def get_challenge_api(ecc_pulic_key):
    api_url = f"{settings.API_BASE_URL}/user/challenge"

    payload = {
        "publicKey": ecc_pulic_key,
    }

    response = requests.post(api_url, json=payload)
    response.raise_for_status()

    response_json = response.json()
    if not check_api_success(response_json):
        raise ValueError("API response is not successful")

    return response.json()


def verify_challenge_api(ecc_public_key, signature):
    api_url = f"{settings.API_BASE_URL}/user/verify"

    payload = {"publicKey": ecc_public_key, "signature": signature}

    response = requests.post(api_url, json=payload)
    response.raise_for_status()

    response_json = response.json()
    if not check_api_success(response_json):
        raise ValueError("API response is not successful")

    return response.json()
