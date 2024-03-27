import random
import unittest

from faker import Faker

from service.credential_service import (
    create_random_credential,
    get_credential_data,
    get_credential_data_with_sensitive_fields,
)
from service.folder_service import create_random_folder, get_folder_credentials
from service.group_service import add_member_to_group, create_random_group
from service.share_credential_service import (
    share_credentials_with_groups,
    share_credentials_with_users,
    share_folder_with_groups,
    share_folder_with_users,
)
from service.user_services import create_and_login_random_user

fake = Faker()


class TestShareCredentialsWithUsers(unittest.TestCase):

    def setUp(self):

        self.share_from_user = create_and_login_random_user()
        self.share_to_user = create_and_login_random_user()

        self.folder_id = create_random_folder(self.share_from_user)

    def test_share_credentials_to_single_user(self):

        credentials = []
        for _ in range(3):
            credential = create_random_credential(
                folder_id=self.folder_id, user=self.share_from_user
            )
            credentials.append(credential)

        credential_ids_to_share = [
            credential.credential_id for credential in credentials
        ]

        share_to = {
            "user_details": self.share_to_user,
            "access_type": random.choice(["reader", "manager"]),
        }

        _response = share_credentials_with_users(
            credential_ids=credential_ids_to_share,
            share_to_users_with_permission=[share_to],
            share_from_user=self.share_from_user,
        )

        for credential in credentials:

            fetched_credential = get_credential_data_with_sensitive_fields(
                credential_id=credential.credential_id, user=self.share_to_user
            )

            self.assertEqual(credential.credential_id, fetched_credential.credential_id)
            self.assertEqual(credential.folder_id, fetched_credential.folder_id)
            self.assertEqual(credential.description, fetched_credential.description)
            self.assertEqual(credential.name, fetched_credential.name)
            self.assertEqual(
                credential.credential_type, fetched_credential.credential_type
            )
            self.assertEqual(share_to["access_type"], fetched_credential.access_type)

            expected_fields = credential.user_fields[0].fields
            actual_fields = fetched_credential.user_fields[0].fields

            self.assertCountEqual(expected_fields, actual_fields)

    def test_share_credential_to_multiple_users(self):

        credentials = []
        for _ in range(3):
            credential = create_random_credential(
                folder_id=self.folder_id, user=self.share_from_user
            )
            credentials.append(credential)

        credential_ids_to_share = [
            credential.credential_id for credential in credentials
        ]

        share_to_users_with_permission = []

        for _ in range(3):
            share_to_user = create_and_login_random_user()
            share_to_users_with_permission.append(
                {
                    "user_details": share_to_user,
                    "access_type": random.choice(["reader", "manager"]),
                }
            )

        response = share_credentials_with_users(
            credential_ids=credential_ids_to_share,
            share_to_users_with_permission=share_to_users_with_permission,
            share_from_user=self.share_from_user,
        )

        self.assertTrue(response["success"])

        for share_to_user in share_to_users_with_permission:

            for credential in credentials:

                fetched_credential = get_credential_data_with_sensitive_fields(
                    credential_id=credential.credential_id,
                    user=share_to_user["user_details"],
                )

                self.assertEqual(
                    credential.credential_id, fetched_credential.credential_id
                )
                self.assertEqual(credential.folder_id, fetched_credential.folder_id)
                self.assertEqual(credential.description, fetched_credential.description)
                self.assertEqual(credential.name, fetched_credential.name)
                self.assertEqual(
                    credential.credential_type, fetched_credential.credential_type
                )
                self.assertEqual(
                    share_to_user["access_type"], fetched_credential.access_type
                )

                expected_fields = credential.user_fields[0].fields
                actual_fields = fetched_credential.user_fields[0].fields

                self.assertCountEqual(expected_fields, actual_fields)


class TestShareFolderWithUsers(unittest.TestCase):
    def setUp(self):
        self.share_from_user = create_and_login_random_user()
        self.share_to_user = create_and_login_random_user()

    def test_share_folder_with_users(self):
        folder_id = create_random_folder(self.share_from_user)

        credential_1 = create_random_credential(
            folder_id=folder_id, user=self.share_from_user
        )
        credential_2 = create_random_credential(
            folder_id=folder_id, user=self.share_from_user
        )

        share_to_users = [
            {
                "user_details": self.share_to_user,
                "access_type": random.choice(["reader", "manager"]),
            }
        ]
        response = share_folder_with_users(
            folder_id=folder_id,
            share_from_user=self.share_from_user,
            share_to_users_with_permission=share_to_users,
        )

        self.assertTrue(response["success"])

        folder_credentials = get_folder_credentials(
            folder_id=folder_id, user=self.share_to_user
        )

        expected_credential_ids = [
            credential_1.credential_id,
            credential_2.credential_id,
        ]
        actual_credential_ids = [
            credential["credentialId"] for credential in folder_credentials
        ]

        self.assertCountEqual(expected_credential_ids, actual_credential_ids)


class TestShareCredentialWithGroup(unittest.TestCase):

    def setUp(self):

        self.share_from_user = create_and_login_random_user()
        self.folder_id = create_random_folder(self.share_from_user)
        self.credentials = [
            create_random_credential(
                folder_id=self.folder_id, user=self.share_from_user
            )
            for _ in range(3)
        ]

        self.group = create_random_group(self.share_from_user)
        self.user_2 = create_and_login_random_user()

        add_member_to_group(
            group_id=self.group, new_member=self.user_2, caller=self.share_from_user
        )

    def test_share_credentials_with_group(self):

        share_to_group_with_permission = {
            "group_id": self.group,
            "access_type": random.choice(["reader", "manager"]),
        }

        response = share_credentials_with_groups(
            credential_ids=[
                credential.credential_id for credential in self.credentials
            ],
            share_to_groups_with_permission=[share_to_group_with_permission],
            share_from_user=self.share_from_user,
        )

        self.assertTrue(response["success"])

        fetched_credential = get_credential_data_with_sensitive_fields(
            credential_id=self.credentials[0].credential_id,
            user=self.user_2,
        )

        self.assertEqual(
            fetched_credential.credential_id, self.credentials[0].credential_id
        )
        self.assertEqual(
            share_to_group_with_permission["access_type"],
            fetched_credential.access_type,
        )

        expected_fields = self.credentials[0].user_fields[0].fields
        actual_fields = fetched_credential.user_fields[0].fields

        self.assertCountEqual(expected_fields, actual_fields)


class TestShareFolderWithGroup(unittest.TestCase):

    def setUp(self):

        self.share_from_user = create_and_login_random_user()
        self.folder_id = create_random_folder(self.share_from_user)
        self.credentials = [
            create_random_credential(
                folder_id=self.folder_id, user=self.share_from_user
            )
            for _ in range(3)
        ]

        self.group = create_random_group(self.share_from_user)
        self.user_2 = create_and_login_random_user()

        add_member_to_group(
            group_id=self.group, new_member=self.user_2, caller=self.share_from_user
        )

    def test_share_folder_with_group(self):

        share_to_group_with_permission = {
            "group_id": self.group,
            "access_type": random.choice(["reader", "manager"]),
        }

        response = share_folder_with_groups(
            folder_id=self.folder_id,
            share_to_groups_with_permission=[share_to_group_with_permission],
            share_from_user=self.share_from_user,
        )

        self.assertTrue(response["success"])

        folder_credentials = get_folder_credentials(
            folder_id=self.folder_id, user=self.user_2
        )

        expected_credential_ids = [
            credential.credential_id for credential in self.credentials
        ]
        actual_credential_ids = [
            credential["credentialId"] for credential in folder_credentials
        ]

        self.assertCountEqual(expected_credential_ids, actual_credential_ids)
