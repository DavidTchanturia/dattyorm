import os
from data_operators.base_data_operator import BaseFileInfo

def parse_file_path(file_path: str) -> tuple[str, str, str]:
    directory_path = os.path.dirname(file_path)
    file_name, file_extension = os.path.splitext(os.path.basename(file_path))

    return directory_path, file_name, file_extension[1:]


def validate_file_path(file_path: str) -> str:
    directory_path, file_name, file_extension = parse_file_path(file_path)
    file = BaseFileInfo(file_name=file_name, file_extension=file_extension)

    validated_path = os.path.join(directory_path, f"{file.file_name}.{file.file_extension}")
    return validated_path


def create_data_file(file_path: str) -> None:
    valid_file_path = validate_file_path(file_path)

    if not os.path.exists(valid_file_path):
        with open(valid_file_path, "w"):
            pass

