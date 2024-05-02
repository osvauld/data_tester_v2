import os

from dotenv import load_dotenv

load_dotenv()


API_BASE_URL = os.getenv("API_BASE_URL")
ADMIN_DEVICE_PUBLIC_KEY = os.getenv("ADMIN_DEVICE_PUBLIC_KEY")
ADMIN_DEVICE_PRIVATE_KEY = os.getenv("ADMIN_DEVICE_PRIVATE_KEY")
