import unittest

from faker import Faker
from service.group_services import (
    create_group_service,
    create_random_group,
    fetch_all_group_users_service,
    fetch_all_user_groups_service,
)
from service.user_services import (
    create_random_user,
    register_user, login,
    fetch_all_users,
    create_and_login_random_user,
)
from utils.test_utils import is_valid_uuid

fake = Faker()


class TestFolder(unittest.TestCase):

    def setUp(self):
        self.user, temp_password = create_random_user()
        register_user(self.user, temp_password)
        login(self.user)

    def test_create_group(self):
        group_name = fake.file_name()
        description = fake.text()
        group_id = create_group_service(self.user, group_name, description)

        self.assertTrue(is_valid_uuid(group_id))

    # def test_add_users_to_group(self):
    #     group_owner = create_and_login_random_user()
    #     new_member = create_and_login_random_user()
    #     group_id = create_random_group(group_owner)
    #     users_list = fetch_all_users(self.user)
    #     result=users_list[1]['name']
    #     add_user_to_group_service(group_id=group_id,user=self.user)

    def test_fetch_all_group_users(self):
        group_owner = create_and_login_random_user()
        group_id = create_random_group(group_owner)
        group_members = fetch_all_group_users_service(group_id=group_id, user=group_owner)

    def test_fetch_all_user_groups(self):
        user = create_and_login_random_user()
        group_id_1 = create_random_group(user)
        group_id_2 = create_random_group(user)
        user_groups = fetch_all_user_groups_service(user)
