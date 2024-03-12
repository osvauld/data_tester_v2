import random
import uuid

import faker

from api.group_api import (
    add_members_to_group_api,
    create_group_api,
    get_group_credential_fields_api,
    get_groups_members_api,
    get_users_without_group_access_api,
)
from model.user import User
from utils.crypto import encrypt_text

fake = faker.Faker()


def create_random_group(user: User) -> uuid.UUID:

    payload = {
        "name": fake.name(),
    }

    response = create_group_api(
        payload=payload,
        user=user,
    )

    return response["data"]["groupId"]


def get_users_without_group_access(group_id: uuid.UUID, caller: User):

    response = get_users_without_group_access_api(
        group_id=group_id,
        user=caller,
    )

    return response["data"]


def get_group_credential_fields(group_id: uuid.UUID, user: User):

    response = get_group_credential_fields_api(
        group_id=group_id,
        user=user,
    )

    return response["data"]


def add_member_to_group(group_id: uuid.UUID, new_member: User, caller: User):

    group_credentials = get_group_credential_fields(group_id=group_id, user=caller)

    all_credentials = []
    for credential in group_credentials:

        credential_fields = []
        for field in credential["fields"]:

            new_field = {
                "fieldId": field["fieldId"],
                "fieldValue": encrypt_text(
                    field["fieldValue"], new_member.encryption_public_key
                ),
            }
            credential_fields.append(new_field)

        all_credentials.append(
            {
                "credentialId": credential["credentialId"],
                "fields": credential_fields,
            }
        )

    payload = {
        "groupId": group_id,
        "memberId": new_member.user_id,
        "memberRole": random.choice(["member", "manager"]),
        "credentials": all_credentials,
    }

    response = add_members_to_group_api(
        payload=payload,
        user=caller,
    )

    return response


def get_groups_members(group_ids: uuid.UUID, user: User):

    response = get_groups_members_api(group_ids=group_ids, user=user)
    return response["data"]
