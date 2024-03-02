import settings
import requests

from utils.api_validator import check_api_success


def create_group_api(payload, user):

    api_url = f"{settings.API_BASE_URL}/group"

    headers = {
        "Authorization": f"Bearer {user.token}",
    }

    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()
    response_json = response.json()
    if not check_api_success(response_json):
        raise ValueError("API response is not successful")

    return response.json()


def get_users_without_group_access_api(group_id, user):
    api_url = f"{settings.API_BASE_URL}/group/{group_id}/users/without-access"

    headers = {
        "Authorization": f"Bearer {user.token}",
    }

    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    response_json = response.json()
    if not check_api_success(response_json):
        raise ValueError("API response is not successful")

    return response.json()
