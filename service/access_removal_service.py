import uuid

from model.user import User
from api.remove_access_api import remove_user_access_for_credential_api


def remove_user_access_for_credential(
    credential_id: uuid.UUID, remove_for_users: list[User], caller: User
):
    """
    Remove user access for a credential
    """

    remove_for_user_ids = [user.user_id for user in remove_for_users]
    response = remove_user_access_for_credential_api(
        credential_id=credential_id, remove_for_users=remove_for_user_ids, user=caller
    )

    return response
