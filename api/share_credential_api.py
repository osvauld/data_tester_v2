import requests

import settings
from model.user import User
from utils.api_validator import check_api_success


def share_credentials_for_users_api(payload: dict, user: User):

    api_url = f"{settings.API_BASE_URL}/share-credentials/users"

    headers = {
        "Authorization": f"Bearer {user.token}",
    }

    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()

    response_json = response.json()
    if not check_api_success(response_json):
        raise ValueError("API response is not successful")

    return response.json()


def share_folder_with_users_api(payload: dict, user: User):

    api_url = f"{settings.API_BASE_URL}/share-folder/users"

    headers = {
        "Authorization": f"Bearer {user.token}",
    }

    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()

    response_json = response.json()
    if not check_api_success(response_json):
        raise ValueError("API response is not successful")

    return response.json()


def share_credentials_with_groups_api(payload: dict, user: User):

    api_url = f"{settings.API_BASE_URL}/share-credentials/groups"

    headers = {
        "Authorization": f"Bearer {user.token}",
    }

    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()

    response_json = response.json()
    if not check_api_success(response_json):
        raise ValueError("API response is not successful")

    return response.json()


def share_folder_with_groups_api(payload: dict, user: User):

    api_url = f"{settings.API_BASE_URL}/share-folder/groups"

    headers = {
        "Authorization": f"Bearer {user.token}",
    }

    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()

    response_json = response.json()
    if not check_api_success(response_json):
        raise ValueError("API response is not successful")

    return response.json()
