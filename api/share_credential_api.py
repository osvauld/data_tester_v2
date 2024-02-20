import settings

import requests

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
