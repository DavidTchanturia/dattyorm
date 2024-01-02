import os
from datetime import datetime
from data_operators.base_file_info_validation import BaseFileInfo


def parse_file_path(file_path: str) -> tuple[str, str, str]:
    """given the absolute or relative path of a file, returns its

    directory

    name without the extension

    and the extension either csv or json
    """
    directory_path = os.path.dirname(file_path)
    file_name, file_extension = os.path.splitext(os.path.basename(file_path))

    return directory_path, file_name, file_extension[1:]


def validate_file_path(file_path: str) -> str:
    """given the full path of a file, returns validated path"""
    directory_path, file_name, file_extension = parse_file_path(file_path)
    file = BaseFileInfo(file_name=file_name, file_extension=file_extension)

    validated_path = os.path.join(directory_path, f"{file.file_name}.{file.file_extension}")
    return validated_path


def create_data_file(file_path: str) -> None:
    """creates file at the given location"""
    valid_file_path = validate_file_path(file_path)

    if not os.path.exists(valid_file_path):
        with open(valid_file_path, "w"):
            pass


def get_metadata(file_path):
    """
    returns the dictionary that contains file size and creation date
    :param file_path:
    """
    try:
        # Get file size in kilobytes
        file_size = round((os.path.getsize(file_path) / 1024.0), 5)

        # get file creation date
        creation_time = os.path.getctime(file_path)
        date_created = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')

        # get file modification date
        modification_time = os.path.getmtime(file_path)
        date_modified = datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d %H:%M:%S')
        details_dict = {"file_size": file_size, "date_created": date_created, "date_modified": date_modified}
        return details_dict
    except FileNotFoundError:
        return None, None


def update_date_modified(func):
    def wrapper(self, *args, **kwargs):
        self.file_metadata.date_modified = datetime.now()
        result = func(self, *args, **kwargs)
        return result
    return wrapper
