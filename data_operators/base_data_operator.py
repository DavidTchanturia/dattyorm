from abc import ABC, abstractmethod
from utils.helpers import parse_file_path, get_metadata
import pandas as pd
from data_operators.base_file_info_validation import BaseFileInfo


class BaseDataOperator(ABC):
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = {}
        self.file_metadata = None

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def commit_to_file(self) -> None:
        pass

    def insert_data(self, data: dict) -> None:
        """gets data as a dict, converts to dataframe and concatenates to existing df"""
        try:
            idx = len(self.data)  # Get the next index for the new entry
            self.data[idx] = data
        except:
            ...
        # finally:
        #     self._update_file_metadata()  # if data is inserted in an empty file get the metadata

    def update_data(self, identifier_column, identifier_value, new_data: dict) -> None:
        """Find rows that match the identifier and update columns with kwargs"""
        matching_indices = []

        for index, row_data in self.data.items():
            if row_data.get(identifier_column) == identifier_value:
                matching_indices.append(index)

        for index in matching_indices:
            row_data = self.data[index]
            for key, val in new_data.items():
                row_data[key] = val

    def delete_data(self, identifier_column, identifier_value) -> None:
        """remove data from self.df, original file not affected until committing to it"""
        indices_to_remove = []

        for index, row_data in self.data.items():
            if row_data.get(identifier_column) == identifier_value:
                indices_to_remove.append(index)

        for index in indices_to_remove:
            del self.data[index]
    #
    # def _df_headers_types(self):
    #     """to get headers and types of the dataframe"""
    #     if self.df.empty:
    #         return {}
    #
    #     columns = self.df.columns
    #     types = self.df.dtypes
    #     headers_and_types = {column: str(dtype) for column, dtype in zip(columns, types)}
    #     return headers_and_types

    # def _update_file_metadata(self) -> None:
    #     """assign the actual metadata to self.df
    #
    #     will be called after the initial creation of the file"""
    #     # since the first variable is directory path, no need for it
    #     _, file_name, file_extension = parse_file_path(self.file_path)
    #     file_info = get_metadata(self.file_path)
    #     self.file_metadata = BaseFileInfo(file_name=file_name, file_extension=file_extension, **file_info)
    #     self.file_metadata.headers_and_types = self._df_headers_types()



