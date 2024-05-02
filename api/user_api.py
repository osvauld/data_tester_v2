import requests

import settings
from utils.api_validator import check_api_success


def create_user_api(name, username, temp_password, admin_token):
    api_url = f"{settings.API_BASE_URL}/user"

    payload = {
        "name": name,
        "username": username,
        "tempPassword": temp_password,
        "type": "admin",
    }

    headers = {
        "Authorization": f"Bearer {admin_token}",
    }

    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()

    response_json = response.json()
    if not check_api_success(response_json):
        raise ValueError("API response is not successful")

    return response.json()


def temp_login_user_api(username, temp_password):
    api_url = f"{settings.API_BASE_URL}/user/temp-login"

    payload = {
        "username": username,
        "tempPassword": temp_password,
    }

    response = requests.post(api_url, json=payload)
    response.raise_for_status()

    response_json = response.json()
    if not check_api_success(response_json):
        raise ValueError("API response is not successful")

    return response.json()


def register_user_api(user, signature):
    api_url = f"{settings.API_BASE_URL}/user/register"

    payload = {
        "username": user.username,
        "signature": signature,
        "deviceKey": user.device_public_key,
        "encryptionKey": user.encryption_public_key,
    }

    response = requests.post(api_url, json=payload)
    response.raise_for_status()

    response_json = response.json()
    if not check_api_success(response_json):
        raise ValueError("API response is not successful")

    return response.json()


def get_challenge_api(device_public_key):
    api_url = f"{settings.API_BASE_URL}/user/challenge"

    payload = {
        "publicKey": device_public_key,
    }

    response = requests.post(api_url, json=payload)
    response.raise_for_status()

    response_json = response.json()
    if not check_api_success(response_json):
        raise ValueError("API response is not successful")

    return response.json()


def verify_challenge_api(device_public_key, signature):
    api_url = f"{settings.API_BASE_URL}/user/verify"

    payload = {"publicKey": device_public_key, "signature": signature}

    response = requests.post(api_url, json=payload)
    response.raise_for_status()

    response_json = response.json()
    if not check_api_success(response_json):
        raise ValueError("API response is not successful")

    return response.json()
