from unittest import TestCase

from service.credential_service import create_random_credential
from service.folder_service import create_random_folder
from service.get_access import get_users_with_direct_access
from service.share_credential_service import share_credentials_with_users
from service.user_services import create_and_login_random_user


class TestGetCredentialAccess(TestCase):

    def setUp(self):
        self.user = create_and_login_random_user()

        folder_id = create_random_folder(self.user)

        self.created_credential = create_random_credential(
            folder_id=folder_id, user=self.user
        )

    def test_direct_acquired_access(self):

        share_to_users = [
            create_and_login_random_user() for _ in range(3)
        ]

        share_credentials_with_users(
            credential_ids=[self.created_credential.credential_id],
            share_to_users_with_permission=[
                {"user_details": user, "access_type": "manager"} for user in share_to_users
            ],
            share_from_user=self.user,
        )

        fetched_users = get_users_with_direct_access(
            credential_id=self.created_credential.credential_id, user=self.user
        )

        share_to_user_ids = [user.user_id for user in share_to_users] + [self.user.user_id]
        for user in fetched_users:
            self.assertIn(user["id"], share_to_user_ids)
            self.assertEqual("manager", user["accessType"])
            self.assertEqual("acquired", user["accessSource"])

