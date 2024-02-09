from api.folder_api import create_folder_api


def create_folder_service(user, folder_name, description):

    token = user.token
    response = create_folder_api(
        folder_name=folder_name,
        description=description,
        token=token,
    )
    return response["data"]["folderId"]
