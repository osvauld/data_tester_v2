from model.user import User

from api.share_credential_api import share_credentials_for_users_api

from service.credential_service import (
    get_credential_fields_by_ids,
)

from utils.crypto import encrypt_text

from uuid import uuid4


def share_credentials_with_users(
    credential_ids: list[uuid4],
    share_from_user: User,
    share_to_users_with_permission: User,
):

    user_data = []

    credential_fields = get_credential_fields_by_ids(credential_ids, share_from_user)

    for share_to_user in share_to_users_with_permission:
        user_credentials = []

        for credential_dict in credential_fields:

            encrypted_fields = []
            for field in credential_dict["fields"]:
                encrypted_field = {
                    "fieldId": field["fieldId"],
                    "fieldValue": encrypt_text(
                        field["fieldValue"],
                        share_to_user["user_details"].encryption_public_key,
                    ),
                }
                encrypted_fields.append(encrypted_field)

            user_credentials.append(
                {
                    "credentialId": credential_dict["credentialId"],
                    "fields": encrypted_fields,
                }
            )

        user_data.append(
            {
                "userId": share_to_user["user_details"].user_id,
                "accessType": share_to_user["access_type"],
                "credentials": user_credentials,
            }
        )

    payload = {"userData": user_data}

    response = share_credentials_for_users_api(payload, share_from_user)

    return response
