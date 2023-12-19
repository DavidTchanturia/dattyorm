import os
from data_operators.base_data_operator import BaseDataOperator
import pandas as pd
from utils.helpers import create_data_file, validate_file_path
from utils.orm_logger import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

class CSVDataOperator(BaseDataOperator):
    CURRENT_WORKING_DIRECTORY = os.getcwd()
    BACKUP_FILE_PATH = os.path.join(CURRENT_WORKING_DIRECTORY, "this_is_a_backup_file.csv")

    # instantiate BaseDataOperator and have a backup file path if one is not provided
    def __init__(self, file_path=BACKUP_FILE_PATH):
        super().__init__(file_path=file_path)

    def get_data(self):
        """read the data from csv file assign it to self.df

        if file not found, create empty file and empty dataframe

        while creating validate name

        after creating file get its metadata
        --> file_name
        --> file_extension
        --> date_created
        --> headers and their types in pd"""
        try:
            self.df = pd.read_csv(self.file_path)
        except FileNotFoundError:
            logger.error("file at given path does not exist, creating new one")
            self.file_path = validate_file_path(self.file_path)  # to update new file path if name validated
            create_data_file(self.file_path)
        except pd.errors.EmptyDataError:  # to handle empty files
            logger.error(f'file at {validate_file_path(self.file_path)} is empty')
        finally:
            self._update_file_metadata()  # get headers and types

    def commit_to_file(self) -> None:
        """saves modified self.df  to the file"""
        self.df.to_csv(self.file_path, index=False)

    def write_data_into_json(self, path_to_json_location):
        """convert dataframe to json and save to json

        if json does not exist, create with validating the name"""
        validated_json_path = validate_file_path(path_to_json_location)
        self.df.to_json(validated_json_path, index=False, orient='records', indent=4, force_ascii=False)


