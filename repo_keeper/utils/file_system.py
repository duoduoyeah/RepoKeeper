import os


def examine_path(path: str) -> dict:
    if os.path.isfile(path):
        return {"path": path, "type": "file"}
    elif os.path.isdir(path):
        return {"path": path, "type": "directory"}
    else:
        return {"path": path, "type": "unknown"}

def get_all_folders(path: str) -> list[str]:
    return [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

def get_all_files(path: str) -> list[str]:
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

