import requests
import settings

def create_folder_api(folder_details, token):
    api_url = f"{settings.API_BASE_URL}/folder"

    response = requests.post(api_url, json=folder_details, headers={"Authorization": f"Bearer {token}"})
    response.raise_for_status()

    return response.json()