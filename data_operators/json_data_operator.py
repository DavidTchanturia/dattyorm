from data_operators.base_data_operator import BaseDataOperator
from utils.helpers import create_data_file, validate_file_path
from utils.orm_logger import setup_logging
import logging
import os
import pandas as pd
import json

setup_logging()
logger = logging.getLogger(__name__)


class JsonDataOperator(BaseDataOperator):
    CURRENT_WORKING_DIRECTORY = os.getcwd()
    BACKUP_FILE_PATH = os.path.join(CURRENT_WORKING_DIRECTORY, "this_is_a_backup_file.json")

    def __init__(self, file_path=BACKUP_FILE_PATH):
        super().__init__(file_path=file_path)

    def get_data(self):
        try:
            # to handle json files that might have nested data
            with open(self.file_path, 'r') as file:
                data = json.load(file)
            # Normalize the JSON data into a DataFrame
            self.df = pd.json_normalize(data)  # to try to normalize all the nested json data
        except FileNotFoundError:
            self.file_path = validate_file_path(self.file_path)  # to update new file path if name validated
            create_data_file(self.file_path)
        except pd.errors.EmptyDataError:
            print("no data in the file")
        finally:
            self._update_file_metadata()

    def commit_to_file(self) -> None:
        """saves modified self.df  to the file"""
        self.df.to_json(self.file_path, index=False, orient="records", indent=4)

    def write_data_into_csv(self, path_to_json_location):
        """convert dataframe to json and save to json

        if json does not exist, create with validating the name"""
        validated_json_csv = validate_file_path(path_to_json_location)
        self.df.to_csv(validated_json_csv, index=False)