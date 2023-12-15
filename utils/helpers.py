import os


def parse_file_path(file_path: str) -> tuple[str, str, str]:
    directory_path = os.path.dirname(file_path)
    file_name, file_extension = os.path.splitext(os.path.basename(file_path))

    return directory_path, file_name, file_extension[1:]


