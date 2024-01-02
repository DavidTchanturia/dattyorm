from data_operators.base_data_operator import BaseDataOperator
from utils.helpers import create_data_file, validate_file_path, update_date_modified
from utils.orm_logger import setup_logging
from utils.constants import BACKUP_FILE_NAME
import logging
import os
import json
import csv

setup_logging()
logger = logging.getLogger(__name__)


class JsonDataOperator(BaseDataOperator):
    CURRENT_WORKING_DIRECTORY = os.getcwd()
    BACKUP_FILE_PATH = os.path.join(CURRENT_WORKING_DIRECTORY, f"{BACKUP_FILE_NAME}.json")

    def __init__(self, file_path=BACKUP_FILE_PATH):
        super().__init__(file_path=file_path)

    def get_data(self):
        """Read data from a JSON file and assign it to self.data"""
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                for idx, row in enumerate(data):
                    self.data[idx] = row
        except FileNotFoundError:
            logger.error("file at the given path does not exist, creating a new one.")
            self.file_path = validate_file_path(self.file_path)
            create_data_file(self.file_path)
        except json.decoder.JSONDecodeError:
            logger.info(f"file {validate_file_path(self.file_path)} is empty.")
        finally:
            self._update_file_metadata()

    @update_date_modified
    def commit_to_file(self) -> None:
        """Save modified self.data to the JSON file"""
        try:
            with open(self.file_path, 'w') as jsonfile:
                json.dump(list(self.data.values()), jsonfile, indent=4)
        except IOError as e:
            logger.error(f"error writing to JSON file: {e}")

    def write_data_into_csv(self, path_to_csv_location):
        """Convert data to CSV and save to a CSV file"""
        try:
            if not self.data:
                logger.warning("No data to write to CSV.")
                return

            validated_csv_path = validate_file_path(path_to_csv_location)

            with open(validated_csv_path, 'w', newline='') as csvfile:
                csv_writer = csv.DictWriter(csvfile, fieldnames=self._get_fieldnames())

                # Write header
                if self.data:
                    csv_writer.writeheader()

                    # Write rows
                    for row_data in self.data.values():
                        csv_writer.writerow(row_data)
        except IOError as e:
            logger.error(f"error writing to CSV file: {e}")

    def _get_fieldnames(self):
        if not self.data:
            return []
        return list(self.data[0].keys())
