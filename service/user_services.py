from faker import Faker

from api.user_api import create_user_api

fake = Faker()


def create_random_user():
    user_details = {
        "name": fake.name(),
        "username": fake.user_name(),
        "password": fake.password(),
    }

    response = create_user_api(user_details)
    return response["data"]
