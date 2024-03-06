import uuid
from uuid import uuid4

from api.share_credential_api import (share_credentials_for_users_api,
                                      share_credentials_with_groups_api,
                                      share_folder_with_groups_api,
                                      share_folder_with_users_api)
from model.user import User
from service.credential_service import get_credential_fields_by_ids
from service.folder_service import credential_fields_for_folder_id
from service.group_service import get_groups_members
from utils.crypto import encrypt_text


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


def share_folder_with_users(
    folder_id: uuid.UUID, share_from_user: User, share_to_users_with_permission
):
    """
    Share folder with users
    """

    credential_fields = credential_fields_for_folder_id(
        folder_id=folder_id, user=share_from_user
    )["data"]

    all_user_data = []
    for user in share_to_users_with_permission:

        user_data = []
        for credential in credential_fields:
            fields = credential["fields"]
            credential_fields = []

            for field in fields:

                new_field = {
                    "fieldId": field["fieldId"],
                    "fieldValue": encrypt_text(
                        field["fieldValue"], user["user_details"].encryption_public_key
                    ),
                }

                credential_fields.append(new_field)

            user_data.append(
                {
                    "credentialId": credential["credentialId"],
                    "fields": credential_fields,
                }
            )

        all_user_data.append(
            {
                "userId": user["user_details"].user_id,
                "accessType": user["access_type"],
                "credentials": user_data,
            }
        )

    payload = {"folderId": folder_id, "userData": all_user_data}

    response = share_folder_with_users_api(payload=payload, user=share_from_user)

    return response


def share_credentials_with_groups(
    credential_ids: list[uuid4],
    share_from_user: User,
    share_to_groups_with_permission: User,
):
    """
    Share credentials with group
    """

    credential_fields = get_credential_fields_by_ids(credential_ids, share_from_user)

    group_ids = [
        share_to_group["group_id"] for share_to_group in share_to_groups_with_permission
    ]
    group_members = get_groups_members(group_ids=group_ids, user=share_from_user)

    group_member_map = {}
    for member in group_members:
        group_member_map[member["groupId"]] = member["userDetails"]

    group_data = []
    for share_to_group in share_to_groups_with_permission:
        group_members_credentials = []
        group_members = group_member_map[share_to_group["group_id"]]

        for member in group_members:

            user_credentials = []
            for credential_dict in credential_fields:
                encrypted_fields = []
                for field in credential_dict["fields"]:
                    encrypted_field = {
                        "fieldId": field["fieldId"],
                        "fieldValue": encrypt_text(
                            field["fieldValue"],
                            member["publicKey"],
                        ),
                    }
                    encrypted_fields.append(encrypted_field)

                user_credentials.append(
                    {
                        "credentialId": credential_dict["credentialId"],
                        "fields": encrypted_fields,
                    }
                )

            group_members_credentials.append(
                {
                    "userId": member["id"],
                    "credentials": user_credentials,
                }
            )

        group_data.append(
            {
                "groupId": share_to_group["group_id"],
                "accessType": share_to_group["access_type"],
                "userData": group_members_credentials,
            }
        )

    payload = {"groupData": group_data}
    response = share_credentials_with_groups_api(payload, share_from_user)

    return response


def share_folder_with_groups(
    folder_id: uuid.UUID, share_from_user: User, share_to_groups_with_permission
):
    """
    Share folder with groups
    """

    credential_fields = credential_fields_for_folder_id(
        folder_id=folder_id, user=share_from_user
    )["data"]

    group_ids = [
        share_to_group["group_id"] for share_to_group in share_to_groups_with_permission
    ]
    group_members = get_groups_members(group_ids=group_ids, user=share_from_user)

    group_member_map = {}
    for member in group_members:
        group_member_map[member["groupId"]] = member["userDetails"]

    group_data = []
    for share_to_group in share_to_groups_with_permission:
        group_members_credentials = []
        group_members = group_member_map[share_to_group["group_id"]]

        for member in group_members:

            user_credentials = []
            for credential in credential_fields:
                fields = credential["fields"]
                new_credential_fields = []

                for field in fields:

                    new_field = {
                        "fieldId": field["fieldId"],
                        "fieldValue": encrypt_text(
                            field["fieldValue"], member["publicKey"]
                        ),
                    }

                    new_credential_fields.append(new_field)

                user_credentials.append(
                    {
                        "credentialId": credential["credentialId"],
                        "fields": new_credential_fields,
                    }
                )

            group_members_credentials.append(
                {
                    "userId": member["id"],
                    "credentials": user_credentials,
                }
            )

        group_data.append(
            {
                "groupId": share_to_group["group_id"],
                "accessType": share_to_group["access_type"],
                "userData": group_members_credentials,
            }
        )

    payload = {"folderId": folder_id, "groupData": group_data}
    response = share_folder_with_groups_api(payload=payload, user=share_from_user)

    return response
