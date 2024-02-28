from api.group_api import create_group_api, fetch_all_group_users_api, fetch_all_user_groups_api

from faker import Faker

fake = Faker()


def create_group_service(user, group_name, description):
    token = user.token
    response = create_group_api(
        group_name=group_name,
        description=description,
        token=token,
    )
    return response["data"]["groupId"]


def create_random_group(user):
    group_name = fake.name()
    description = fake.text()
    group_id = create_group_service(user, group_name, description)

    return group_id


# def add_users_to_group_service()

def fetch_all_group_users_service(group_id, user):
    response = fetch_all_group_users_api(group_id=group_id, user=user)
    return response["data"]


def fetch_all_user_groups_service(user):
    response = fetch_all_user_groups_api(user)
    return response["data"]

