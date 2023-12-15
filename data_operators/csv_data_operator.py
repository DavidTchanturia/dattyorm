from data_operators.base_data_operator import BaseDataOperator
import pandas as pd
from utils.helpers import create_data_file, validate_file_path


class CSVDataOperator(BaseDataOperator):
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def get_data(self):
        """simply read data from csv file"""
        try:
            self.df = pd.read_csv(self.file_path)
        except FileNotFoundError:
            print("file at given path does not exist, creating new one")
            self.file_path = validate_file_path(self.file_path)  # to update new file path if name validated
            create_data_file(self.file_path)
            self.df = pd.DataFrame()

    def insert_data(self, data: dict) -> None:
        """gets data as a dict, converts to dataframe and concatenates to existing df"""
        new_data = pd.DataFrame([data])
        if self.df.empty:
            self.df = new_data
        else:
            self.df = pd.concat((self.df, new_data), ignore_index=True)

    def update_data(self, index, **kwargs) -> None:
        # TODO: validate the column types being updated
        """find row with index, and updates those columns that have been passed as a keyword argument"""
        for key, value in kwargs.items():
            self.df.at[index, key] = value

    def delete_data(self, index) -> None:
        self.df.drop(index, inplace=True)

    def commit_to_file(self) -> None:
        self.df.to_csv(self.file_path)


person = {
    "name": "kako",
    "last_name": "kak",
    "age": 23,
    "sex": "male"
}
