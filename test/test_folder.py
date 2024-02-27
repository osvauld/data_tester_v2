import unittest

from service.folder_service import create_folder_service, get_users_with_folder_access
from service.user_services import create_and_login_random_user
from utils.test_utils import is_valid_uuid

from faker import Faker

fake = Faker()


class TestFolder(unittest.TestCase):
    def setUp(self):
        self.user = create_and_login_random_user()

    def test_create_folder(self):
        folder_name = fake.name()
        description = fake.text()
        folder_id = create_folder_service(self.user, folder_name, description)

        self.assertTrue(is_valid_uuid(folder_id))

    def test_get_users_with_folder_access(self):
        folder_name = "test_folder"
        description = "test_description"
        folder_id = create_folder_service(self.user, folder_name, description)

        users = get_users_with_folder_access(folder_id, self.user)

        self.assertEqual(users[0]["id"], self.user.user_id)
