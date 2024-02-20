import unittest

from faker import Faker
from service.group_services import create_group_service
from service.user_services import create_random_user, register_user, login
from utils.test_utils import is_valid_uuid

fake = Faker()


class TestFolder(unittest.TestCase):

    def setUp(self):
        self.user, temp_password = create_random_user()
        register_user(self.user, temp_password)
        login(self.user)

    def test_create_random_group(self):
        group_name = fake.file_name()
        description = fake.text()
        group_id = create_group_service(self.user, group_name, description)

        self.assertTrue(is_valid_uuid(group_id))
