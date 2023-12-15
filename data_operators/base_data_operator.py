from abc import ABC, abstractmethod
import os
import pandas as pd



class BaseDataOperator(ABC):
    CURRENT_WORKING_DIRECTORY = os.getcwd()

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def insert_data(self, data: pd.DataFrame) -> None:
        pass

    @abstractmethod
    def update_data(self, index, **kwargs) -> None:
        pass

    @abstractmethod
    def delete_data(self, index) -> None:
        pass

    @abstractmethod
    def commit_to_file(self) -> None:
        pass

    @classmethod
    def write_data_into_json(cls, data: pd.DataFrame, file_path: str) -> None:
        pass

    @classmethod
    def write_data_into_csv(cls, data: pd.DataFrame, file_path: str) -> None:
        pass

    def delete_file(self):
        pass



