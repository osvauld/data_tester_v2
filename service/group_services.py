from api.group_api import create_group_api


def create_group_service(user, group_name, description):

    token = user.token
    response = create_group_api(
        group_name=group_name,
        description=description,
        token=token,
    )
    return response["data"]["groupId"]
