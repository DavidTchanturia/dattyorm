from data_operators.base_data_operator import BaseDataOperator
from utils.helpers import create_data_file, validate_file_path
from utils.orm_logger import setup_logging
from utils.constants import BACKUP_FILE_NAME
import logging
import json
import csv
import os

setup_logging()
logger = logging.getLogger(__name__)


class CSVDataOperator(BaseDataOperator):
    CURRENT_WORKING_DIRECTORY = os.getcwd()
    BACKUP_FILE_PATH = os.path.join(CURRENT_WORKING_DIRECTORY, f"{BACKUP_FILE_NAME}.csv")

    # instantiate BaseDataOperator and have a backup file path if one is not provided
    def __init__(self, file_path=BACKUP_FILE_PATH):
        super().__init__(file_path=file_path)

    def get_data(self):
        """read the data from csv file assign it to self.data

        if file not found, create empty file

        while creating validate name

        after creating file get its metadata
        --> file_name
        --> file_extension
        --> date_created
        --> headers and their types"""
        try:
            with open(self.file_path, 'r', newline='') as csvfile:
                csvreader = csv.DictReader(csvfile)
                for idx, row in enumerate(csvreader):
                    self.data[idx] = row
        except FileNotFoundError:
            logger.error("file at given path does not exist, creating new one")
            self.file_path = validate_file_path(self.file_path)  # to update new file path if name validated
            create_data_file(self.file_path)
        finally:
            self._update_file_metadata()  # get headers and types
            # pass

    def commit_to_file(self) -> None:
        try:
            if not self.data:
                logger.warning("no data to write to file.")
                return

            # get the names of fields from key values
            fieldnames = list(self.data[next(iter(self.data))].keys())

            with open(self.file_path, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Write header
                writer.writeheader()

                # Write rows
                for row_data in self.data.values():
                    writer.writerow(row_data)
        except IOError as e:
            logger.error(f"error writing to CSV file: {e}")

    def write_data_into_json(self, path_to_json_location):
        """convert data to JSON and save to a JSON file"""
        try:
            if not self.data:
                logger.warning("no data to write to JSON.")
                return

            validated_json_path = validate_file_path(path_to_json_location)

            with open(validated_json_path, 'w') as jsonfile:
                json.dump(list(self.data.values()), jsonfile, indent=4)
        except IOError as e:
            logger.error(f"error writing to JSON file: {e}")


