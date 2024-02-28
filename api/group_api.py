import requests
import settings
from utils.api_validator import check_api_success


def create_group_api(group_name, description, token):
    api_url = f"{settings.API_BASE_URL}/group"

    payload = {
        "name": group_name,
        "description": description,
    }

    headers = {
        "Authorization": f"Bearer {token}",
    }

    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()

    response_json = response.json()
    if not check_api_success(response_json):
        raise ValueError("API response is not successful")

    return response.json()


def fetch_all_group_users_api(group_id, user):
    api_url = f"{settings.API_BASE_URL}/folder/{group_id}/users"

    headers = {
        "Authorization": f"Bearer {user.token}",
    }

    response = requests.get(api_url, headers=headers)
    response.raise_for_status()

    response_json = response.json()
    if not check_api_success(response_json):
        raise ValueError("API response is not successful")

    return response.json()


def fetch_all_user_groups_api(user):
    api_url = f"{settings.API_BASE_URL}/groups"

    headers = {
        "Authorization": f"Bearer {user.token}",
    }

    response = requests.get(api_url, headers=headers)
    response.raise_for_status()

    response_json = response.json()
    if not check_api_success(response_json):
        raise ValueError("API response is not successful")

    return response.json()

