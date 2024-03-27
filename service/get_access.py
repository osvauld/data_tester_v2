from api.get_access_api import get_users_with_direct_access_api
from model.user import User


def get_users_with_direct_access(credential_id: str, user: User):

    response = get_users_with_direct_access_api(
        credential_id=credential_id,
        user=user,
    )

    return response["data"]

