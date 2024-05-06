import base64
import hashlib
import json

import requests

import settings
from model.credential import Credential
from model.user import User
from utils.api_validator import check_api_success
from utils.crypto import hash_and_sign


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
                    for field in user_field.fields
                ],
            }
        )

    # Serialize payload consistently with JavaScript's JSON.stringify
    signature = hash_and_sign(payload, user.device_private_key)

    headers = {
        "Authorization": f"Bearer {user.token}",
        "Signature": signature,
        "Content-Type": "application/json",
    }

    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()

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


def get_all_users_with_credential_access_api(credential_id: str, user: User):
    api_url = f"{settings.API_BASE_URL}/credential/{credential_id}/users-data-sync"

    headers = {
        "Authorization": f"Bearer {user.token}",
    }

    response = requests.get(api_url, headers=headers)
    response.raise_for_status()

    response_json = response.json()
    if not check_api_success(response_json):
        raise ValueError("API response is not successful")

    return response_json


def edit_credential_api(credential_id: str, user: User, payload: dict):
    api_url = f"{settings.API_BASE_URL}/credential/{credential_id}"
    signature = hash_and_sign(payload, user.device_private_key)

    headers = {
        "Authorization": f"Bearer {user.token}",
        "Signature": signature,
        "Content-Type": "application/json",
    }
    response = requests.put(api_url, json=payload, headers=headers)
    response.raise_for_status()

    response_json = response.json()
    if not check_api_success(response_json):
        raise ValueError("API response is not successful")

    return response.json()
