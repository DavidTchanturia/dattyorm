import logging
import os

CURRENT_WORKING_DIRECTORY = os.getcwd()
LOG_FILE_PATH = os.path.join(CURRENT_WORKING_DIRECTORY, "orm_log.txt")

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE_PATH),
            logging.StreamHandler()
        ]
    )