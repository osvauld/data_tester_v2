import uuid

import faker

from model.user import User

from api.group_api import create_group_api, get_users_without_group_access_api

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
