import os
from data_operators.base_data_operator import BaseDataOperator, BaseFileInfo
import pandas as pd
from utils.helpers import create_data_file, validate_file_path, parse_file_path, get_metadata


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
            print("file at given path does not exist, creating new one")
            self.file_path = validate_file_path(self.file_path)  # to update new file path if name validated
            create_data_file(self.file_path)
        except pd.errors.EmptyDataError: # to handle empty files
            print("no data in the file")
        finally:
            self._update_file_metadata()  # get theaders and types

    def insert_data(self, data: dict) -> None:
        """gets data as a dict, converts to dataframe and concatenates to existing df"""
        try:
            new_data = pd.DataFrame([data])
            if self.df.empty:
                self.df = new_data
            else:
                self.df = pd.concat((self.df, new_data), ignore_index=True)
        finally:
            self._update_file_metadata()  # if data is inserted in an empty file get the metadata

    def update_data(self, index, **kwargs) -> None:
        # TODO: validate the column types being updated
        """find row with index, and updates those columns that have been passed as a keyword argument"""
        for key, value in kwargs.items():
            self.df.at[index, key] = value

    def delete_data(self, index) -> None:
        """remove data from self.df, original file not affected unitll commiting to it"""
        self.df.drop(index, inplace=True)

    def commit_to_file(self) -> None:
        """saves modified self.df to to the file"""
        self.df.to_csv(self.file_path, index=False)

    def write_data_into_json(self, path_to_json_location):
        """convert dataframe to json and save to json

        if json does not exist, create with validating the name"""
        validated_json_path = validate_file_path(path_to_json_location)
        self.df.to_json(validated_json_path, index=False, orient='records', indent=4, force_ascii=False)

    def _df_headers_types(self):
        """to get headers and types of the dataframe"""
        if self.df.empty:
            return {}

        columns = self.df.columns
        types = self.df.dtypes
        headers_and_types = {column: str(dtype) for column, dtype in zip(columns, types)}
        return headers_and_types

    def _update_file_metadata(self) -> None:
        """assign the actual metadata to self.df

        will be called after the initial creation of the file"""
        # since the first variable is directory path, no need for it
        _, file_name, file_extension = parse_file_path(self.file_path)
        file_info = get_metadata(self.file_path)
        self.file_metadata = BaseFileInfo(file_name=file_name, file_extension=file_extension, **file_info)
        self.file_metadata.headers_and_types = self._df_headers_types()


