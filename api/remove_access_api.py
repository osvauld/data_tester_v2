import uuid

import requests

import settings
from model.user import User
from utils.api_validator import check_api_success


def remove_user_access_for_credential_api(
    credential_id: uuid.UUID, remove_for_users: User, user: User
):
    """
    Remove user access for a credential
    """

    api_url = f"{settings.API_BASE_URL}/credential/{credential_id}/remove-access"

    headers = {
        "Authorization": f"Bearer {user.token}",
    }

    payload = {"userIds": remove_for_users}

    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()

    response_json = response.json()

    if not check_api_success(response_json):
        raise ValueError("API response is not successful")

    return response_json
