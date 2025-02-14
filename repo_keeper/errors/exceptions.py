class RepoUpdateError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class FileSystemError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class FileUpdateError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class ContentUpdateError(Exception):
    def __init__(self, message: str):
        super().__init__(message)