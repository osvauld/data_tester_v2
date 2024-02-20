from api.folder_api import create_folder_api, get_users_with_folder_access_api

from faker import Faker

fake = Faker()


def create_folder_service(user, folder_name, description):
    response = create_folder_api(
        folder_name=folder_name,
        description=description,
        user=user,
    )
    return response["data"]["folderId"]


def get_users_with_folder_access(folder_id, user):
    response = get_users_with_folder_access_api(
        folder_id=folder_id,
        user=user,
    )

    return response["data"]


def create_random_folder(user):
    folder_name = fake.name()
    description = fake.text()
    folder_id = create_folder_service(user, folder_name, description)

    return folder_id
