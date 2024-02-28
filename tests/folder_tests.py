import unittest

from service.folder_service import (
    create_folder_service,
    get_users_with_folder_access,
    create_random_folder,
    fetch_all_folders_service
)
from service.user_services import (
    create_random_user,
    register_user,
    login, create_and_login_random_user
)
from service.group_services import  create_random_group
from utils.test_utils import is_valid_uuid

from faker import Faker

fake = Faker()


class TestFolder(unittest.TestCase):
    def setUp(self):
        self.user, temp_password = create_random_user()
        register_user(self.user, temp_password)
        login(self.user)

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

    def test_fetch_all_folders(self):
        user = create_and_login_random_user()
        folder_id = create_random_folder(user)
        folders = fetch_all_folders_service(user)


    # def test_fetch_all_folder_groups(self):
    #     user = create_and_login_random_user()
    #     folder_id = create_random_folder(user)
    #     group_id = create_random_group(user)
    #     folders =
