import unittest

from service.user_services import (create_random_user, login, register_user,
                                   temp_login_user)
from utils.test_utils import is_valid_uuid


class TestUserLogin(unittest.TestCase):
    def test_create_user(self):
        user, _temp_password = create_random_user()
        self.assertTrue(is_valid_uuid(user.user_id))

    def test_temp_login(self):
        user, temp_password = create_random_user()
        challenge = temp_login_user(user, temp_password)
        self.assertIsInstance(challenge, str)

    def test_register_user(self):

        user, temp_password = create_random_user()
        challenge = temp_login_user(user, temp_password)

        user, response_bool = register_user(user, challenge)
        self.assertTrue(response_bool)

    def test_login_user(self):
        user, temp_password = create_random_user()
        challenge = temp_login_user(user, temp_password)
        user, response_bool = register_user(user, challenge)

        login(user)
        self.assertTrue(user.token)
