import unittest

from service.folder_service import create_folder_service
from service.user_services import create_random_user, register_user, login
from utils.test_utils import is_valid_uuid


class TestFolder(unittest.TestCase):

    def setUp(self):

        self.user, temp_password = create_random_user()
        register_user(self.user, temp_password)
        login(self.user)

    def test_create_folder(self):

        folder_name = "test_folder"
        description = "test_description"
        folder_id = create_folder_service(self.user, folder_name, description)

        self.assertTrue(is_valid_uuid(folder_id))
