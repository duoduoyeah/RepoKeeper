from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

from ..utils import examine_path, get_all_folders, get_all_files
from ..errors import RepoUpdateError

@dataclass
class File:
    """Represents a file in a repository.

    Args:
        name: File name with extension
        path: Full path to file
        size: Size in bytes
        last_modified: Last modification timestamp
        content: Optional file content

    Returns:
        File object

    Raises:
        ValueError: If path or name is empty
    """

    name: str
    size: int
    last_modified: datetime
    content: Optional[str] = None

    def __post_init__(self):
        if not self.name:
            raise ValueError("Name must not be empty")


@dataclass
class Folder:
    """Represents a folder in a repository.

    Args:
        name: Folder name
        path: Full path to folder
        files: List of File objects
        subfolders: List of Folder objects

    Returns:
        Folder object

    Raises:
        ValueError: If path or name is empty
    """

    name: str
    path: str
    files: List[File] = []
    subfolders: List["Folder"] = []

    def update_folder(self):
        self.files = get_all_files(self.path)
        self.subfolders = get_all_folders(self.path)
        for subfolder in self.subfolders:
            subfolder.update_folder()

    def __post_init__(self):
        if not self.path or not self.name:
            raise ValueError("Path and name must not be empty")
        self.files = self.files or []
        self.subfolders = self.subfolders or []


@dataclass
class GithubRepo:
    """Represents a GitHub repository structure.

    Args:
        name: Repository name
        owner: Repository owner
        root_folder: Root Folder object
        created_at: Repository creation timestamp
        last_updated: Last update timestamp

    Returns:
        GithubRepo object

    Raises:
        ValueError: If name or root_folder is empty
    """
    
    name: str
    root_folder: Folder
    
    owner: Optional[str] = None
    created_at: datetime = datetime.now()
    last_updated: datetime = datetime.now()
    last_verified: datetime = datetime.min 

    def update_repository(self):
        try:
            if examine_path(self.root_folder.path).type == "directory":
                self.root_folder.update_folder()
            else:
                raise RepoUpdateError("Root folder is not a directory")
        except Exception as e:
            raise RepoUpdateError(f"Error updating repository: {e}")

        
    def verify_repository(self):
        pass
    
    def __post_init__(self):
        if not self.name or not self.root_folder:
            raise ValueError("Repository name and root_folder must not be empty")


# Delete later
if __name__ == "__main__":
    # Create example Folder and File objects

    example_file = File(
        name="example.txt", 
        size=1024,
        last_modified=datetime.now(),
        
    )  # File object with name and size
    example_subfolder = Folder(
        name="subfolder", path="/path/to/subfolder"
    )  # Subfolder object
    example_folder = Folder(
        name="root",
        path="/path/to/root",
        files=[example_file],
        subfolders=[example_subfolder],
    )  # Root folder with a file and a subfolder

    # Create example GithubRepo object
    example_repo = GithubRepo(
        name="example-repo",
        owner="example-owner",
        root_folder=example_folder,
        created_at=datetime.now(),
        last_updated=datetime.now(),
    )  # GithubRepo object with root folder and timestamps
    print("Example repository created:", example_repo)