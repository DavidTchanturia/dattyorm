from abc import ABC, abstractmethod
from utils.helpers import parse_file_path, get_metadata
import pandas as pd
from data_operators.base_file_info_validation import BaseFileInfo


class BaseDataOperator(ABC):
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = pd.DataFrame()
        self.file_metadata = None

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def insert_data(self, data: pd.DataFrame) -> None:
        pass

    @abstractmethod
    def update_data(self, identifier_column, identifier_value, **kwargs) -> None:
        pass

    @abstractmethod
    def delete_data(self, index) -> None:
        pass

    @abstractmethod
    def commit_to_file(self) -> None:
        pass

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



