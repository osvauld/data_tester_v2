import unittest

from service.group_service import (
    add_member_to_group,
    create_random_group,
    get_users_without_group_access,
    get_groups_members,
)
from service.user_services import create_and_login_random_user
from utils.test_utils import is_valid_uuid


class TestGroup(unittest.TestCase):

    def setUp(self) -> None:
        self.user = create_and_login_random_user()

    def test_group_creation(self):

        group_id = create_random_group(user=self.user)
        self.assertTrue(is_valid_uuid(group_id))

    def test_users_without_group_access(self):

        group_id = create_random_group(user=self.user)
        # create 3 random users
        random_users = [create_and_login_random_user() for _ in range(3)]

        user_details = get_users_without_group_access(
            group_id=group_id, caller=self.user
        )

        user_ids = [user["id"] for user in user_details]

        for random_user in random_users:
            self.assertIn(random_user.user_id, user_ids)

        self.assertNotIn(self.user.user_id, user_ids)

    def test_add_member_to_group(self):

        group_id = create_random_group(user=self.user)
        new_member = create_and_login_random_user()

        add_member_to_group(group_id=group_id, new_member=new_member, caller=self.user)

        group_members = get_groups_members(group_ids=[group_id], user=self.user)

        user_ids = [user["id"] for user in group_members[0]["userDetails"]]

        self.assertIn(new_member.user_id, user_ids)
