from faker import Faker

from api.folder_api import create_folder_api
from scenario.auth_scenario import authenticate_dummy_user

fake = Faker()


def create_folder():
    folder_details = {
        "name": fake.name(),
        "description": fake.sentence()
    }
    token = authenticate_dummy_user()
    response = create_folder_api(folder_details= folder_details,token = token)
    return response["data"]
