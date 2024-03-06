import random
import unittest

from service.access_removal_service import remove_user_access_for_credential
from service.credential_service import (create_random_credential,
                                        get_credential_data)
from service.folder_service import create_random_folder
from service.share_credential_service import (share_credentials_with_users,
                                              share_folder_with_users)
from service.user_services import create_and_login_random_user


class TestCredentialAccessRemovalForUser(unittest.TestCase):

    def setUp(self):
        pass

    def test_access_removal(self):
        self.share_from_user = create_and_login_random_user()
        self.share_to_user = create_and_login_random_user()

        self.folder_id = create_random_folder(self.share_from_user)

        credential = create_random_credential(
            folder_id=self.folder_id, user=self.share_from_user
        )

        share_to_user = {
            "user_details": self.share_to_user,
            "access_type": random.choice(["read", "write", "owner"]),
        }
        response = share_credentials_with_users(
            credential_ids=[credential.credential_id],
            share_to_users_with_permission=[share_to_user],
            share_from_user=self.share_from_user,
        )

        self.assertTrue(response["success"])

        # Check shared credential is accessible for the shared user

        fetched_credential = get_credential_data(
            credential_id=credential.credential_id, user=self.share_to_user
        )

        self.assertEqual(credential.credential_id, fetched_credential.credential_id)
        self.assertEqual(share_to_user["access_type"], fetched_credential.access_type)

        # Remove access for the shared user
        response = remove_user_access_for_credential(
            credential_id=credential.credential_id,
            remove_for_users=[self.share_to_user],
            caller=self.share_from_user,
        )

        self.assertTrue(response["success"])

        with self.assertRaises(Exception) as exc:
            get_credential_data(
                credential_id=credential.credential_id, user=self.share_to_user
            )

        # check the exception is an HTTPError with status code 401
        self.assertEqual(exc.exception.response.status_code, 401)

    def test_access_removal_with_multiple_access(self):
        self.share_from_user = create_and_login_random_user()
        self.share_to_user = create_and_login_random_user()

        self.folder_id = create_random_folder(self.share_from_user)

        credential = create_random_credential(
            folder_id=self.folder_id, user=self.share_from_user
        )

        share_credential_to_user = {
            "user_details": self.share_to_user,
            "access_type": "write",
        }

        # share credential with user
        response = share_credentials_with_users(
            credential_ids=[credential.credential_id],
            share_to_users_with_permission=[share_credential_to_user],
            share_from_user=self.share_from_user,
        )

        self.assertTrue(response["success"])

        share_folder_to_user = {
            "user_details": self.share_to_user,
            "access_type": "read",
        }

        # share folder with user
        response = share_folder_with_users(
            folder_id=self.folder_id,
            share_from_user=self.share_from_user,
            share_to_users_with_permission=[share_folder_to_user],
        )

        # Check shared credential is accessible for the shared user

        fetched_credential = get_credential_data(
            credential_id=credential.credential_id, user=self.share_to_user
        )

        # should have the highest access
        self.assertEqual(fetched_credential.access_type, "write")

        # Remove credential access for the shared user
        response = remove_user_access_for_credential(
            credential_id=credential.credential_id,
            remove_for_users=[self.share_to_user],
            caller=self.share_from_user,
        )

        self.assertTrue(response["success"])

        fetched_credential_again = get_credential_data(
            credential_id=credential.credential_id, user=self.share_to_user
        )

        # should have the next highest access
        self.assertEqual(fetched_credential_again.access_type, "read")
