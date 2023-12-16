from data_operators.base_data_operator import BaseDataOperator
from utils.helpers import create_data_file, validate_file_path
import os
import pandas as pd
import json

class JsonDataOperator(BaseDataOperator):
    CURRENT_WORKING_DIRECTORY = os.getcwd()
    BACKUP_FILE_PATH = os.path.join(CURRENT_WORKING_DIRECTORY, "this_is_a_backup_file.json")

    def __init__(self, file_path=BACKUP_FILE_PATH):
        super().__init__(file_path=file_path)

    def get_data(self):
        try:
            #to handle json files that might have nested data
            with open(self.file_path, 'r') as file:
                data = json.load(file)

            # Normalize the JSON data into a DataFrame
            self.df = pd.json_normalize(data, record_path=None) # to try to normalize all the nested json data
            self.df.to_csv("test_files/json_to_csv.csv", index=False)
        except FileNotFoundError:
            self.file_path = validate_file_path(self.file_path)  # to update new file path if name validated
            create_data_file(self.file_path)
        except pd.errors.EmptyDataError:
            print("no data in the file")
        finally:
            self._update_file_metadata()

    def insert_data(self, data: pd.DataFrame) -> None:
        pass

    def update_data(self, index, **kwargs) -> None:
        pass

    def delete_data(self, index) -> None:
        pass

    def commit_to_file(self) -> None:
        pass