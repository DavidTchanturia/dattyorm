from abc import ABC, abstractmethod
from pydantic import BaseModel, Field, field_validator
from typing import Literal, Dict
from datetime import datetime
import re
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


class BaseFileInfo(BaseModel):
    file_name: str
    file_extension: Literal["csv", "json"]
    file_size: float = 0
    date_created: datetime = Field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    headers_and_types: Dict[str, str] = {} # if file is not empty, will contain column/types, key/types

    @field_validator("file_name")
    def validate_name(cls, value: str):
        """validates name agains illegal characters, if there are some, cleans them
        tes&t_fil*e -> test_file
        """
        if not value:
            raise ValueError("name not valid")
        return cls._clean_file_name(value)

    @field_validator("file_extension")
    def valid_file_extension(cls, value: str):
        """if the extension is not csv or json, raises error

        cant be forced to validate"""
        if not value or value not in ["csv", "json"]:
            raise ValueError("not valid file extension")
        return value

    @staticmethod
    def _clean_file_name(file_name: str) -> str:
        # in case file name contains any illegal characters replace them with ""
        cleaned_file_name = re.sub(r'[^\w.-]', '', file_name)
        return cleaned_file_name




