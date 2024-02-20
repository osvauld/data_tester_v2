from service.user_services import create_random_user, register_user, login, fetch_all_users
import unittest
from utils.test_utils import is_valid_uuid


class TestUserLogin(unittest.TestCase):
    def test_create_user(self):
        user, _temp_password = create_random_user()
        self.assertTrue(is_valid_uuid(user.user_id))

    def test_register_user(self):
        user, temp_password = create_random_user()
        self.assertTrue(is_valid_uuid(user.user_id))

        user, response_bool = register_user(user, temp_password)
        self.assertTrue(response_bool)

    def test_login_user(self):
        user, temp_password = create_random_user()
        user, response_bool = register_user(user, temp_password)

        login(user)
        self.assertTrue(user.token)

    def test_create_folder(self):

        user, temp_password = create_random_user()
        user, response_bool = register_user(user, temp_password)
        login(user)

        self.assertTrue(user.token)

    def test_fetch_all_users(self):

        user, temp_password = create_random_user()
        user, response_bool = register_user(user, temp_password)
        login(user)
        result = fetch_all_users(user)
        self.assertTrue(user.token)

