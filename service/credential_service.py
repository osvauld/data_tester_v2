import uuid

from model.user import User
from model.credential import Field, UserFields, Credential

from utils.crypto import encrypt_text

from api.credential_api import (
    create_credential_api,
    get_credential_data_api,
    get_credential_fields_by_ids_api,
    get_sensitive_fields_by_id_api,
    get_all_users_with_credential_access_api,
    edit_credential_api,
)
from service.folder_service import get_users_with_folder_access

from factories.credential import CredentialFactory, UserFieldsFactory, FieldFactory
from copy import deepcopy

import faker

fake = faker.Faker()


def encrypt_fields(fields: list[Field], public_key: str) -> list[Field]:
    encrypted_fields = deepcopy(fields)
    for field in encrypted_fields:
        field.field_value = encrypt_text(field.field_value, public_key)

    return encrypted_fields


def create_random_credential(folder_id: uuid.UUID, user: User) -> Credential:

    original_fields = [FieldFactory() for _ in range(5)]

    user_fields = UserFieldsFactory(user=user)
    credential = CredentialFactory(
        folder_id=folder_id, user=user, user_fields=[user_fields]
    )

    folder_users = get_users_with_folder_access(folder_id, user)

    encrypted_user_fields = []
    for folder_user in folder_users:

        user_encrypted_fields = encrypt_fields(
            original_fields, folder_user["publicKey"]
        )
        user_encrypted_fields = UserFields(user=user, fields=user_encrypted_fields)
        encrypted_user_fields.append(user_encrypted_fields)

    credential.user_fields = encrypted_user_fields

    response = create_credential_api(
        credential=credential,
        user=user,
    )

    credential.credential_id = response["data"]["credentialId"]

    return credential


def get_credential_data(credential_id: uuid.UUID, user: User):

    credential_data = get_credential_data_api(
        credential_id=credential_id,
        user=user,
    )["data"]

    field_objs = [Field.from_dict(field) for field in credential_data["fields"]]

    credential_obj = Credential.from_dict(
        credential_dict=credential_data, user_fields=field_objs, user=user
    )

    return credential_obj


def get_credential_data_with_sensitive_fields(credential_id: uuid.UUID, user: User):

    credential_data = get_credential_data(credential_id, user)
    sensitive_fields = get_sensitive_fields_by_id_api(credential_id, user)["data"]

    # add field type to sensitive fields
    for field in sensitive_fields:
        field["fieldType"] = "sensitive"

    sensitive_field_objs = [Field.from_dict(field) for field in sensitive_fields]

    credential_data.user_fields[0].fields.extend(sensitive_field_objs)

    return credential_data


def get_credential_fields_by_ids(credential_ids: list[int], user: User):

    return get_credential_fields_by_ids_api(credential_ids=credential_ids, user=user)[
        "data"
    ]


def edit_credential(
    credential_id: uuid.UUID,
    updated_details: dict,
    fields: list[Field],
    caller: User,
) -> Credential:

    payload = {
        "name": updated_details["name"],
        "description": updated_details["description"],
        "credentialType": updated_details["credentialType"],
        "userFields": [],
    }

    all_users = get_all_users_with_credential_access_api(credential_id, caller)["data"]

    for user in all_users:

        new_fields_for_user = {
            "userId": user["id"],
            "fields": [],
        }
        for field in fields:
            field = {
                "fieldName": field.field_name,
                "fieldValue": encrypt_text(field.field_value, user["publicKey"]),
                "fieldType": field.field_type,
            }
            new_fields_for_user["fields"].append(field)

        payload["userFields"].append(new_fields_for_user)

    response = edit_credential_api(
        credential_id=credential_id, payload=payload, user=caller
    )

    return response
