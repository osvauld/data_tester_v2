import unittest

from factories.credential import FieldFactory
from service.folder_service import create_random_folder
from service.user_services import create_and_login_random_user
from service.credential_service import (
    create_random_credential,
    get_credential_data,
    get_credential_data_with_sensitive_fields,
    edit_credential,
)
from service.share_credential_service import share_credentials_with_users
from utils.test_utils import is_valid_uuid, is_valid_timestamp

from faker import Faker

fake = Faker()


class TestCredential(unittest.TestCase):
    def setUp(self):
        self.user = create_and_login_random_user()

    def test_create_credential(self):

        folder_id = create_random_folder(self.user)

        credential = create_random_credential(folder_id=folder_id, user=self.user)

        self.assertTrue(is_valid_uuid(credential.credential_id))

    def test_get_credential_data_by_id(self):
        folder_id = create_random_folder(self.user)

        created_credential = create_random_credential(
            folder_id=folder_id, user=self.user
        )

        fetched_credential = get_credential_data(
            credential_id=created_credential.credential_id, user=self.user
        )

        self.assertEqual(
            created_credential.credential_id, fetched_credential.credential_id
        )
        self.assertEqual(created_credential.folder_id, fetched_credential.folder_id)
        self.assertEqual(created_credential.description, fetched_credential.description)
        self.assertEqual(created_credential.name, fetched_credential.name)
        self.assertEqual(
            created_credential.credential_type, fetched_credential.credential_type
        )
        self.assertEqual("owner", fetched_credential.access_type)
        self.assertEqual(self.user.user_id, fetched_credential.created_by)
        self.assertTrue(is_valid_timestamp(fetched_credential.created_at))
        self.assertTrue(is_valid_timestamp(fetched_credential.updated_at))

        expected_fields = [
            i
            for i in created_credential.user_fields[0].fields
            if i.field_type != "sensitive"
        ]
        actual_fields = fetched_credential.user_fields[0].fields

        self.assertCountEqual(expected_fields, actual_fields)


class TestEditCredential(unittest.TestCase):
    def setUp(self):
        self.user = create_and_login_random_user()
        self.another_user = create_and_login_random_user()

        folder_id = create_random_folder(self.user)

        self.created_credential = create_random_credential(
            folder_id=folder_id, user=self.user
        )

        user_data_with_permission = {
            "user_details": self.another_user,
            "access_type": "write",
        }

        share_credentials_with_users(
            credential_ids=[self.created_credential.credential_id],
            share_to_users_with_permission=[user_data_with_permission],
            share_from_user=self.user,
        )

    def test_edit_credential_edit_details(self):

        update_credential_name = fake.name()
        update_credential_description = fake.text()
        update_credential_type = (
            "other" if self.created_credential.credential_type == "login" else "login"
        )

        response = edit_credential(
            credential_id=self.created_credential.credential_id,
            updated_details={
                "name": update_credential_name,
                "description": update_credential_description,
                "credentialType": update_credential_type,
            },
            fields=[],
            caller=self.user,
        )

        self.assertTrue(response["success"])

        # Check values for the user who shared the credentials
        fetched_credential_details = get_credential_data(
            credential_id=self.created_credential.credential_id, user=self.user
        )

        self.assertEqual(fetched_credential_details.name, update_credential_name)
        self.assertEqual(
            fetched_credential_details.description, update_credential_description
        )
        self.assertEqual(
            fetched_credential_details.credential_type, update_credential_type
        )

        # Check values for shared used
        fetched_credential_details_another_user = get_credential_data(
            credential_id=self.created_credential.credential_id, user=self.another_user
        )

        self.assertEqual(
            fetched_credential_details_another_user.name, update_credential_name
        )
        self.assertEqual(
            fetched_credential_details_another_user.description,
            update_credential_description,
        )
        self.assertEqual(
            fetched_credential_details_another_user.credential_type,
            update_credential_type,
        )

    def test_edit_credential_edit_fields(self):

        all_fields = (
            get_credential_data_with_sensitive_fields(
                credential_id=self.created_credential.credential_id, user=self.user
            )
            .user_fields[0]
            .fields
        )

        edit_fields = all_fields[:2]

        for field in edit_fields:
            field.field_name = fake.word()
            field.field_value = fake.password()
            field.field_type = "other"

        response = edit_credential(
            credential_id=self.created_credential.credential_id,
            updated_details={
                "name": self.created_credential.name,
                "description": self.created_credential.description,
                "credentialType": self.created_credential.credential_type,
            },
            fields=all_fields,
            caller=self.user,
        )

        self.assertTrue(response["success"])

        # Check values for the user who shared the credentials
        fetched_fields_for_user = (
            get_credential_data_with_sensitive_fields(
                credential_id=self.created_credential.credential_id, user=self.user
            )
            .user_fields[0]
            .fields
        )

        self.assertCountEqual(fetched_fields_for_user, all_fields)

        # Check values for shared used
        fetched_fields_for_another_user = (
            get_credential_data_with_sensitive_fields(
                credential_id=self.created_credential.credential_id,
                user=self.another_user,
            )
            .user_fields[0]
            .fields
        )

        self.assertCountEqual(fetched_fields_for_another_user, all_fields)

    def test_edit_credential_add_fields(self):

        all_fields = (
            get_credential_data_with_sensitive_fields(
                credential_id=self.created_credential.credential_id, user=self.user
            )
            .user_fields[0]
            .fields
        )

        new_fields = [FieldFactory() for _ in range(3)]
        all_fields = all_fields + new_fields
        response = edit_credential(
            credential_id=self.created_credential.credential_id,
            updated_details={
                "name": self.created_credential.name,
                "description": self.created_credential.description,
                "credentialType": self.created_credential.credential_type,
            },
            fields=all_fields,
            caller=self.user,
        )

        self.assertTrue(response["success"])

        fetched_fields_for_user = (
            get_credential_data_with_sensitive_fields(
                credential_id=self.created_credential.credential_id, user=self.user
            )
            .user_fields[0]
            .fields
        )

        self.assertCountEqual(fetched_fields_for_user, all_fields)

        fetched_fields_for_another_user = (
            get_credential_data_with_sensitive_fields(
                credential_id=self.created_credential.credential_id,
                user=self.another_user,
            )
            .user_fields[0]
            .fields
        )

        self.assertCountEqual(fetched_fields_for_another_user, all_fields)
