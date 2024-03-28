import uuid

from api.remove_access_api import (remove_group_access_for_credential_api,
                                   remove_group_access_for_folder_api,
                                   remove_user_access_for_credential_api,
                                   remove_user_access_for_folder_api)
from model.user import User


def remove_user_access_for_credential(
    credential_id: uuid.UUID, remove_for_users: list[User], caller: User
):
    """
    Remove user access for a credential
    """

    remove_for_user_ids = [user.user_id for user in remove_for_users]
    response = remove_user_access_for_credential_api(
        credential_id=credential_id, remove_for_users=remove_for_user_ids, caller=caller
    )

    return response


def remove_user_access_for_folder(
    folder_id: uuid.UUID, remove_for_users: list[User], caller: User
):
    """
    Remove user access for a folder
    """

    remove_for_user_ids = [user.user_id for user in remove_for_users]
    response = remove_user_access_for_folder_api(
        folder_id=folder_id, remove_for_users=remove_for_user_ids, caller=caller
    )

    return response


def remove_group_access_for_credential(
    credential_id: uuid.UUID, remove_for_groups: list[uuid.UUID], caller: User
):
    """
    Remove group access for a credential
    """

    response = remove_group_access_for_credential_api(
        credential_id=credential_id, remove_for_groups=remove_for_groups, caller=caller
    )

    return response


# remove group access for folder api
def remove_group_access_for_folder(
    folder_id: uuid.UUID, remove_for_groups: list[uuid.UUID], caller: User
):
    """
    Remove group access for a folder
    """

    response = remove_group_access_for_folder_api(
        folder_id=folder_id, remove_for_groups=remove_for_groups, caller=caller
    )

    return response
