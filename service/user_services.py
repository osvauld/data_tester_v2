from faker import Faker

from api.user_api import (
    create_user_api,
    register_user_api,
    get_challenge_api,
    verify_challenge_api,
)
from model.user import User
from utils.crypto import (
    generate_ecc_key_pair,
    generate_rsa_key_pair,
    sign_message_ecdsa,
    remove_pem_header,
)

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


def register_user(user, temp_password):
    ecc_private_key, ecc_public_key = generate_ecc_key_pair()
    rsa_private_key, rsa_public_key = generate_rsa_key_pair()

    user.rsa_public_key = rsa_public_key
    user.rsa_private_key = rsa_private_key
    user.ecc_public_key = ecc_public_key
    user.ecc_private_key = ecc_private_key

    response = register_user_api(user, temp_password=temp_password)
    return user, response["data"]


def login(user):
    pem_removed_ecc_public_key = remove_pem_header(user.ecc_public_key)

    response = get_challenge_api(pem_removed_ecc_public_key)
    challenge = response["data"]["challenge"]

    sign = sign_message_ecdsa(user.ecc_private_key, challenge)

    response = verify_challenge_api(pem_removed_ecc_public_key, sign)
    token = response["data"]["token"]

    user.token = token


def create_and_login_random_user():
    user, temp_password = create_random_user()
    user, token = register_user(user, temp_password)
    login(user)
    return user
