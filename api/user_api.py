import requests
import settings


def create_user_api(user_details):
    api_url = f"{settings.API_BASE_URL}/user"

    response = requests.post(api_url, json=user_details)
    response.raise_for_status()

    return response.json()
