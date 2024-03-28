import requests

import settings
from model.user import User
from utils.api_validator import check_api_success


def get_users_with_direct_access_api(credential_id: str, user: User):

    api_url = f"{settings.API_BASE_URL}/credential/{credential_id}/users"

    headers = {
        "Authorization": f"Bearer {user.token}",
    }

    response = requests.get(api_url, headers=headers)
    response.raise_for_status()

    response_json = response.json()
    if not check_api_success(response_json):
        raise ValueError("API response is not successful")

    return response.json()
