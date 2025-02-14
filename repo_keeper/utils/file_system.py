import os
from datetime import datetime
from .general_decorator import exception_handler
from ..errors import FileSystemError

@exception_handler(FileSystemError)
def examine_path(path: str) -> dict:
    if os.path.isfile(path):
        return {"path": path, "type": "file"}
    elif os.path.isdir(path):
        return {"path": path, "type": "directory"}
    else:
        return {"path": path, "type": "unknown"}

@exception_handler(FileSystemError)
def get_all_folders(path: str) -> list[str]:
    return [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

@exception_handler(FileSystemError)
def get_all_files(path: str) -> list[str]:
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

@exception_handler(FileSystemError)
def get_last_modified_date(file_path) -> str:
    modified_time = os.path.getmtime(file_path)
    modified_date = datetime.fromtimestamp(modified_time)
    return modified_date.strftime("%Y-%m-%d %H:%M:%S")

@exception_handler(FileSystemError)
def get_file_content(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()

if __name__ == "__main__":
    print(get_all_folders("."))
    print(get_all_files("."))
