import requests
import settings



def create_challenge(publicKey):
    api_url = f"{settings.API_BASE_URL}/user/challenge"
    response = requests.post(api_url, json={"publicKey": publicKey})
    response.raise_for_status()

    return response.json()

def verify_user(signedChallenge, publicKey):
    api_url = f"{settings.API_BASE_URL}/user/verify"
    response = requests.post(api_url, json={ "signature": signedChallenge,"publicKey": publicKey})
    response.raise_for_status()
    return response.json()