import requests

import settings
from model.user import User
from utils.api_validator import check_api_success


def create_folder_api(folder_name, description, user):
    api_url = f"{settings.API_BASE_URL}/folder"

    payload = {
        "name": folder_name,
        "description": description,
    }

    headers = {
        "Authorization": f"Bearer {user.token}",
    }

    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()

    response_json = response.json()
    if not check_api_success(response_json):
        raise ValueError("API response is not successful")

    return response.json()


def get_users_with_folder_access_api(folder_id, user):
    api_url = f"{settings.API_BASE_URL}/folder/{folder_id}/users-data-sync"

    headers = {
        "Authorization": f"Bearer {user.token}",
    }

    response = requests.get(api_url, headers=headers)
    response.raise_for_status()

    response_json = response.json()
    if not check_api_success(response_json):
        raise ValueError("API response is not successful")

    return response.json()


def get_credentials_fields_for_folder_api(folder_id: str, user: User):
    api_url = f"{settings.API_BASE_URL}/credentials/fields/{folder_id}"

    headers = {
        "Authorization": f"Bearer {user.token}",
    }

    response = requests.get(api_url, headers=headers)
    response.raise_for_status()

    response_json = response.json()
    if not check_api_success(response_json):
        raise ValueError("API response is not successful")

    return response_json


def get_folder_credentials_api(folder_id, user):
    api_url = f"{settings.API_BASE_URL}/folder/{folder_id}/credential"

    headers = {
        "Authorization": f"Bearer {user.token}",
    }

    response = requests.get(api_url, headers=headers)
    response.raise_for_status()

    response_json = response.json()
    if not check_api_success(response_json):
        raise ValueError("API response is not successful")

    return response_json
