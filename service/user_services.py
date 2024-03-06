from faker import Faker

from api.user_api import (create_user_api, get_challenge_api,
                          register_user_api, temp_login_user_api,
                          verify_challenge_api)
from model.user import User
from utils.crypto import generate_device_key, sign_message

fake = Faker()


def create_random_user():
    name = fake.name()
    username = fake.user_name()
    password = fake.password()

    response = create_user_api(
        name=name,
        username=username,
        temp_password=password,
    )
    user_id = response["data"]
    user = User(
        user_id=user_id,
        username=username,
        name=name,
    )
    return user, password


def temp_login_user(user, temp_password):
    response = temp_login_user_api(user.username, temp_password)
    return response["data"]["challenge"]


def register_user(user, registration_challenge):

    device_public_key, device_private_key = generate_device_key()

    user.device_public_key = device_public_key
    user.device_key_fingerprint = device_private_key
    user.encryption_public_key = "encryption public key"
    user.encryption_private_key = "encryption private key"

    challenge_signature = sign_message(device_private_key, registration_challenge)

    response = register_user_api(user, signature=challenge_signature)
    return user, response["data"]


def login(user):

    response = get_challenge_api(user.device_public_key)
    challenge = response["data"]["challenge"]

    sign = sign_message(user.device_key_fingerprint, challenge)

    response = verify_challenge_api(user.device_public_key, sign)
    token = response["data"]["token"]

    user.token = token


def create_and_login_random_user():
    user, temp_password = create_random_user()
    registration_challenge = temp_login_user(user, temp_password)
    user, token = register_user(user, registration_challenge)
    login(user)
    return user
