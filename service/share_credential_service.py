from model.user import User

from api.share_credential_api import share_credentials_for_users_api

from service.credential_service import (
    get_credential_fields_by_ids,
)

from utils.crypto import encrypt_text

from uuid import uuid4


def share_credentials_with_user(
    credential_ids: list[uuid4], share_from_user: User, share_to_user: User
):

    payload = {
        "userData": [
            {
                "userId": share_to_user.user_id,
                "accessType": "write",
                "credentials": [],
            }
        ]
    }

    credential_fields = get_credential_fields_by_ids(credential_ids, share_from_user)

    shared_credential_fields = []
    for credential_dict in credential_fields:

        encrypted_fields = []
        for field in credential_dict["fields"]:
            encrypted_field = {
                "fieldId": field["fieldId"],
                "fieldValue": encrypt_text(
                    field["fieldValue"], share_to_user.encryption_public_key
                ),
            }
            encrypted_fields.append(encrypted_field)

        shared_credential_fields.append(
            {
                "credentialId": credential_dict["credentialId"],
                "fields": encrypted_fields,
            }
        )

    payload["userData"][0]["credentials"] = shared_credential_fields

    response = share_credentials_for_users_api(payload, share_from_user)

    return response
