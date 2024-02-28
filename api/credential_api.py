import settings

import requests

from model.credential import Credential
from model.user import User
from utils.api_validator import check_api_success


def create_credential_api(credential: Credential, user: User):
    api_url = f"{settings.API_BASE_URL}/credential"

    payload = {
        "name": credential.name,
        "description": credential.description,
        "folderId": credential.folder_id,
        "credentialType": credential.credential_type,
        "userFields": [],
    }

    for user_field in credential.user_fields:
        payload["userFields"].append(
            {
                "userId": user_field.user.user_id,
                "fields": [
                    {
                        "fieldName": field.field_name,
                        "fieldValue": field.field_value,
                        "fieldType": field.field_type,
                    }
                    for field in user_field.field
                ],
            }
        )

    headers = {
        "Authorization": f"Bearer {user.token}",
    }

    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()

    response_json = response.json()
    if not check_api_success(response_json):
        raise ValueError("API response is not successful")

    return response.json()


def get_credential_data_api(credential_id, user):
    api_url = f"{settings.API_BASE_URL}/credential/{credential_id}"

    headers = {
        "Authorization": f"Bearer {user.token}",
    }

    response = requests.get(api_url, headers=headers)
    response.raise_for_status()

    response_json = response.json()
    if not check_api_success(response_json):
        raise ValueError("API response is not successful")

    return response.json()


def get_credential_fields_by_ids_api(credential_ids: list[int], user: User):
    api_url = f"{settings.API_BASE_URL}/credentials/fields"

    payload = {
        "credentialIds": credential_ids,
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


def get_sensitive_fields_by_id_api(credential_id: str, user: User):
    api_url = f"{settings.API_BASE_URL}/credential/{credential_id}/sensitive"

    headers = {
        "Authorization": f"Bearer {user.token}",
    }

    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    response_json = response.json()
    if not check_api_success(response_json):
        raise ValueError("API response is not successful")

    return response.json()


def get_credentials_by_folder_api(folder_id, user):
    api_url = f"{settings.API_BASE_URL}/folder/{folder_id}/credential"

    headers = {
        "Authorization": f"Bearer{user.token}",
    }

    response = requests.get(api_url, headers=headers)
    response.raise_for_status()

    response_json = response.json()
    if not check_api_success(response_json):
        raise ValueError("API response is not successful")

    return response.json()
