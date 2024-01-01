from abc import ABC, abstractmethod
from utils.helpers import parse_file_path, get_metadata
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

    def insert_data(self, data_list: list[dict]) -> None:
        """inserts multiple rows of data (list of dicts) into the data attribute"""
        try:
            starting_index = len(self.data)  # Get the starting index for the new entries
            for idx, data in enumerate(data_list):
                self.data[starting_index + idx] = data
        finally:
            self._update_file_metadata()   # if data is inserted in an empty file get the metadata

    def update_data(self, conditions_to_meet: dict, new_data: dict) -> None:
        """find rows that match the conditions and update with new_data"""
        indices = self._find_matching_rows_for_conditions(conditions_to_meet)

        for index in indices:
            row_data = self.data[index]
            for key, value in new_data.items():
                row_data[key] = value

    def add_new_column(self, column_name: str, default_value=None) -> None:
        """ddd a new column to all existing data with the specified default value"""
        for row_data in self.data.values():
            row_data[column_name] = default_value

        self._update_file_metadata()

    def delete_data(self, conditions_to_meet_to_delete: dict) -> None:
        """Remove rows from self.data that match the given conditions"""
        indices = self._find_matching_rows_for_conditions(conditions_to_meet_to_delete)

        for index in indices:
            del self.data[index]

    def _dict_headers_types(self):
        """to get headers and types of the dictionary"""
        if not self.data:
            return {}

        first_entry = next(iter(self.data.values()))
        headers_and_types = {column: type(value).__name__ for column, value in first_entry.items()}
        return headers_and_types

    def _update_file_metadata(self) -> None:
        """assign the actual metadata to self.file_metadata

        will be called after the initial creation of the file"""
        _, file_name, file_extension = parse_file_path(self.file_path)
        file_info = get_metadata(self.file_path)

        # create BaseFileInfo object
        self.file_metadata = BaseFileInfo(file_name=file_name, file_extension=file_extension, **file_info)

        # update headers and types
        self.file_metadata.headers_and_types = self._dict_headers_types()

    def _find_matching_rows_for_conditions(self, conditions: dict) -> list:
        indices = []
        for index, row_data in self.data.items():
            matched = True
            for key, value in conditions.items():
                if row_data.get(key) != value:
                    matched = False
                    break  # break the loop if any condition doesn't match
            if matched:
                indices.append(index)
        return indices
