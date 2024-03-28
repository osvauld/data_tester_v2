import random
import unittest

from service.access_removal_service import (
    remove_user_access_for_credential,
    remove_user_access_for_folder,
    remove_group_access_for_credential,
    remove_group_access_for_folder,
)
from service.credential_service import create_random_credential, get_credential_data
from service.folder_service import create_random_folder
from service.group_service import create_random_group, add_member_to_group
from service.share_credential_service import (
    share_credentials_with_users,
    share_folder_with_users,
    share_credentials_with_groups,
    share_folder_with_groups,
)
from service.user_services import create_and_login_random_user


class TestCredentialAccessRemovalForUser(unittest.TestCase):

    def setUp(self):
        self.share_from_user = create_and_login_random_user()
        self.share_to_user = create_and_login_random_user()

        self.folder_id = create_random_folder(self.share_from_user)

        self.credential = create_random_credential(
            folder_id=self.folder_id, user=self.share_from_user
        )

    def test_access_removal(self):

        share_to_user = {
            "user_details": self.share_to_user,
            "access_type": random.choice(["reader", "manager"]),
        }
        response = share_credentials_with_users(
            credential_ids=[self.credential.credential_id],
            share_to_users_with_permission=[share_to_user],
            share_from_user=self.share_from_user,
        )

        self.assertTrue(response["success"])

        # Check shared credential is accessible for the shared user

        fetched_credential = get_credential_data(
            credential_id=self.credential.credential_id, user=self.share_to_user
        )

        self.assertEqual(
            self.credential.credential_id, fetched_credential.credential_id
        )
        self.assertEqual(share_to_user["access_type"], fetched_credential.access_type)

        # Remove access for the shared user
        response = remove_user_access_for_credential(
            credential_id=self.credential.credential_id,
            remove_for_users=[self.share_to_user],
            caller=self.share_from_user,
        )

        self.assertTrue(response["success"])

        with self.assertRaises(Exception) as exc:
            get_credential_data(
                credential_id=self.credential.credential_id, user=self.share_to_user
            )

        # check the exception is an HTTPError with status code 401
        self.assertEqual(exc.exception.response.status_code, 401)

    def test_access_removal_with_multiple_access(self):

        share_credential_to_user = {
            "user_details": self.share_to_user,
            "access_type": "manager",
        }

        # share credential with user
        response = share_credentials_with_users(
            credential_ids=[self.credential.credential_id],
            share_to_users_with_permission=[share_credential_to_user],
            share_from_user=self.share_from_user,
        )

        self.assertTrue(response["success"])

        share_folder_to_user = {
            "user_details": self.share_to_user,
            "access_type": "reader",
        }

        # share folder with user
        response = share_folder_with_users(
            folder_id=self.folder_id,
            share_from_user=self.share_from_user,
            share_to_users_with_permission=[share_folder_to_user],
        )

        # Check shared credential is accessible for the shared user

        fetched_credential = get_credential_data(
            credential_id=self.credential.credential_id, user=self.share_to_user
        )

        # should have the highest access
        self.assertEqual(fetched_credential.access_type, "manager")

        # Remove credential access for the shared user
        response = remove_user_access_for_credential(
            credential_id=self.credential.credential_id,
            remove_for_users=[self.share_to_user],
            caller=self.share_from_user,
        )

        self.assertTrue(response["success"])

        fetched_credential_again = get_credential_data(
            credential_id=self.credential.credential_id, user=self.share_to_user
        )

        # should have the next highest access
        self.assertEqual(fetched_credential_again.access_type, "reader")


class TestFolderAccessRemovalForUser(unittest.TestCase):

    def setUp(self):
        self.share_from_user = create_and_login_random_user()
        self.share_to_user = create_and_login_random_user()

        self.folder_id = create_random_folder(self.share_from_user)

        self.credentials = [
            create_random_credential(
                folder_id=self.folder_id, user=self.share_from_user
            )
            for _ in range(3)
        ]

    def test_access_removal(self):

        share_to_user = {
            "user_details": self.share_to_user,
            "access_type": random.choice(["reader", "manager"]),
        }
        response = share_folder_with_users(
            folder_id=self.folder_id,
            share_from_user=self.share_from_user,
            share_to_users_with_permission=[share_to_user],
        )

        self.assertTrue(response["success"])

        # Remove access for the shared user
        response = remove_user_access_for_folder(
            folder_id=self.folder_id,
            remove_for_users=[self.share_to_user],
            caller=self.share_from_user,
        )

        self.assertTrue(response["success"])

        with self.assertRaises(Exception) as exc:
            get_credential_data(
                credential_id=self.credentials[0].credential_id, user=self.share_to_user
            )

        # check the exception is an HTTPError with status code 401
        self.assertEqual(exc.exception.response.status_code, 401)

    def test_access_removal_with_multiple_access(self):

        share_credential_to_user = {
            "user_details": self.share_to_user,
            "access_type": "reader",
        }

        # share credential with user
        response = share_credentials_with_users(
            credential_ids=[
                credential.credential_id for credential in self.credentials
            ],
            share_to_users_with_permission=[share_credential_to_user],
            share_from_user=self.share_from_user,
        )
        self.assertTrue(response["success"])

        share_folder_to_user = {
            "user_details": self.share_to_user,
            "access_type": "manager",
        }

        # share folder with user
        response = share_folder_with_users(
            folder_id=self.folder_id,
            share_from_user=self.share_from_user,
            share_to_users_with_permission=[share_folder_to_user],
        )
        self.assertTrue(response["success"])

        # Check shared credential is accessible for the shared user
        fetched_credential = get_credential_data(
            credential_id=self.credentials[0].credential_id, user=self.share_to_user
        )

        # should have the highest access
        self.assertEqual(fetched_credential.access_type, "manager")

        # Remove credential access for the shared user
        response = remove_user_access_for_folder(
            folder_id=self.folder_id,
            remove_for_users=[self.share_to_user],
            caller=self.share_from_user,
        )

        self.assertTrue(response["success"])

        fetched_credential_again = get_credential_data(
            credential_id=self.credentials[0].credential_id, user=self.share_to_user
        )

        # should have the next highest access
        self.assertEqual(fetched_credential_again.access_type, "reader")


class TestCredentialAccessRemovalForGroup(unittest.TestCase):

    def setUp(self):
        self.share_from_user = create_and_login_random_user()
        self.share_to_user = create_and_login_random_user()

        self.folder_id = create_random_folder(self.share_from_user)

        self.credential = create_random_credential(
            folder_id=self.folder_id, user=self.share_from_user
        )

        self.group_id = create_random_group(self.share_from_user)
        add_member_to_group(
            group_id=self.group_id,
            new_member=self.share_to_user,
            caller=self.share_from_user,
        )

    def test_access_removal(self):
        share_to_group_with_permission = {
            "group_id": self.group_id,
            "access_type": random.choice(["reader", "manager"]),
        }
        response = share_credentials_with_groups(
            credential_ids=[self.credential.credential_id],
            share_to_groups_with_permission=[share_to_group_with_permission],
            share_from_user=self.share_from_user,
        )

        self.assertTrue(response["success"])

        # Check shared credential is accessible for the shared user
        fetched_credential = get_credential_data(
            credential_id=self.credential.credential_id, user=self.share_to_user
        )

        # should have the highest access
        self.assertEqual(
            fetched_credential.access_type,
            share_to_group_with_permission["access_type"],
        )

        # Remove access for the shared user
        response = remove_group_access_for_credential(
            credential_id=self.credential.credential_id,
            remove_for_groups=[self.group_id],
            caller=self.share_from_user,
        )

        self.assertTrue(response["success"])

        with self.assertRaises(Exception) as exc:
            get_credential_data(
                credential_id=self.credential.credential_id, user=self.share_to_user
            )

        # check the exception is an HTTPError with status code 401
        self.assertEqual(exc.exception.response.status_code, 401)

    def test_access_removal_with_multiple_access(self):
        share_credential_to_group = {
            "group_id": self.group_id,
            "access_type": "manager",
        }

        # share credential with user
        response = share_credentials_with_groups(
            credential_ids=[self.credential.credential_id],
            share_to_groups_with_permission=[share_credential_to_group],
            share_from_user=self.share_from_user,
        )
        self.assertTrue(response["success"])

        # Check shared credential is accessible for the shared user
        fetched_credential = get_credential_data(
            credential_id=self.credential.credential_id, user=self.share_to_user
        )

        # should have the highest access
        self.assertEqual(
            fetched_credential.access_type, share_credential_to_group["access_type"]
        )

        share_folder_to_group = {
            "group_id": self.group_id,
            "access_type": "reader",
        }

        # share folder with user
        response = share_folder_with_groups(
            folder_id=self.folder_id,
            share_from_user=self.share_from_user,
            share_to_groups_with_permission=[share_folder_to_group],
        )
        self.assertTrue(response["success"])

        # Check shared credential is accessible for the shared user
        fetched_credential = get_credential_data(
            credential_id=self.credential.credential_id, user=self.share_to_user
        )

        # should have the highest access
        self.assertEqual(fetched_credential.access_type, "manager")

        # Remove credential access for the shared user
        response = remove_group_access_for_credential(
            credential_id=self.credential.credential_id,
            remove_for_groups=[self.group_id],
            caller=self.share_from_user,
        )

        self.assertTrue(response["success"])

        fetched_credential_again = get_credential_data(
            credential_id=self.credential.credential_id, user=self.share_to_user
        )

        # should have the next highest access
        self.assertEqual(fetched_credential_again.access_type, "reader")


class TestFolderAccessRemovalForGroup(unittest.TestCase):

    def setUp(self):
        self.share_from_user = create_and_login_random_user()
        self.share_to_user = create_and_login_random_user()

        self.folder_id = create_random_folder(self.share_from_user)

        self.credentials = [
            create_random_credential(
                folder_id=self.folder_id, user=self.share_from_user
            )
            for _ in range(3)
        ]

        self.group_id = create_random_group(self.share_from_user)
        add_member_to_group(
            group_id=self.group_id,
            new_member=self.share_to_user,
            caller=self.share_from_user,
        )

    def test_access_removal(self):
        share_to_group_with_permission = {
            "group_id": self.group_id,
            "access_type": random.choice(["reader", "manager"]),
        }
        response = share_folder_with_groups(
            folder_id=self.folder_id,
            share_from_user=self.share_from_user,
            share_to_groups_with_permission=[share_to_group_with_permission],
        )

        self.assertTrue(response["success"])

        # Check shared credential is accessible for the shared user
        fetched_credential = get_credential_data(
            credential_id=self.credentials[0].credential_id, user=self.share_to_user
        )

        # should have the highest access
        self.assertEqual(
            fetched_credential.access_type,
            share_to_group_with_permission["access_type"],
        )

        # Remove access for the shared user
        response = remove_group_access_for_folder(
            folder_id=self.folder_id,
            remove_for_groups=[self.group_id],
            caller=self.share_from_user,
        )

        self.assertTrue(response["success"])

        with self.assertRaises(Exception) as exc:
            get_credential_data(
                credential_id=self.credentials[0].credential_id, user=self.share_to_user
            )

        # check the exception is an HTTPError with status code 401
        self.assertEqual(exc.exception.response.status_code, 401)

    def test_access_removal_with_multiple_access(self):
        share_credential_to_group = {
            "group_id": self.group_id,
            "access_type": "reader",
        }

        # share credential with user
        response = share_credentials_with_groups(
            credential_ids=[
                credential.credential_id for credential in self.credentials
            ],
            share_to_groups_with_permission=[share_credential_to_group],
            share_from_user=self.share_from_user,
        )
        self.assertTrue(response["success"])

        share_folder_to_group = {
            "group_id": self.group_id,
            "access_type": "manager",
        }

        # share folder with user
        response = share_folder_with_groups(
            folder_id=self.folder_id,
            share_from_user=self.share_from_user,
            share_to_groups_with_permission=[share_folder_to_group],
        )

        self.assertTrue(response["success"])

        # Check shared credential is accessible for the shared user
        fetched_credential = get_credential_data(
            credential_id=self.credentials[0].credential_id, user=self.share_to_user
        )

        # should have the highest access
        self.assertEqual(fetched_credential.access_type, "manager")

        # Remove credential access for the shared user
        response = remove_group_access_for_folder(
            folder_id=self.folder_id,
            remove_for_groups=[self.group_id],
            caller=self.share_from_user,
        )

        self.assertTrue(response["success"])

        fetched_credential_again = get_credential_data(
            credential_id=self.credentials[0].credential_id, user=self.share_to_user
        )

        # should have the next highest access
        self.assertEqual(fetched_credential_again.access_type, "reader")
