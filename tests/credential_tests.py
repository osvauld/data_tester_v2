import unittest

from factories.credential import FieldFactory
from service.folder_service import create_random_folder
from service.user_services import create_random_user, register_user, login
from service.credential_service import create_random_credential, get_credential_data
from utils.test_utils import is_valid_uuid, is_valid_timestamp

from faker import Faker

fake = Faker()


class TestCredential(unittest.TestCase):
    def setUp(self):
        self.user, temp_password = create_random_user()
        register_user(self.user, temp_password)
        login(self.user)

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
            created_credential.credential_id, fetched_credential["credentialId"]
        )
        self.assertEqual(created_credential.folder_id, fetched_credential["folderId"])
        self.assertEqual(
            created_credential.description, fetched_credential["description"]
        )
        self.assertEqual(created_credential.name, fetched_credential["name"])
        self.assertEqual(
            created_credential.credential_type, fetched_credential["credentialType"]
        )
        self.assertEqual("owner", fetched_credential["accessType"])
        self.assertEqual(self.user.user_id, fetched_credential["createdBy"])
        self.assertTrue(is_valid_timestamp(fetched_credential["createdAt"]))
        self.assertTrue(is_valid_timestamp(fetched_credential["updatedAt"]))

        fetched_field_values = [
            {
                "fieldName": field["fieldName"],
                "fieldValue": field["fieldValue"],
                "fieldType": field["fieldType"],
            }
            for field in fetched_credential["fields"]
        ]

        for field in created_credential.user_fields[0].field:
            if field.field_type == "sensitive":
                continue

            expected_dict = {
                "fieldType": field.field_type,
                "fieldName": field.field_name,
                "fieldValue": field.field_value,
            }
            self.assertIn(expected_dict, fetched_field_values)
