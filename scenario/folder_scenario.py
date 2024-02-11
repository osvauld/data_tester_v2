from service.folder_service import create_folder

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_folder_for_dummy_user():
    logger.info("Creating Folder for Dummy User")
    response = create_folder()
    logger.info(f"Creating Folder Successfull. Response: {response}")
