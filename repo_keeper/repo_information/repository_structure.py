from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime
import os
from ..utils import *

from ..errors import *

@dataclass
class Content:
    """
    Represents the content of a file.
    """
    content: str
    file: Optional["File"] = None
    folder: Optional["Folder"] = None

@dataclass
class File:
    """Represents a file in a repository.

    Args:
        name: File name with extension
        path: Full path to file
        size: Size in bytes
        last_modified: Last modification timestamp
        content: Optional file content

    Raises:
        FileUpdateError
        ContentUpdateError
    """

    name: str
    folder: Optional["Folder"] = None
    size: int
    last_modified: datetime
    content: Optional[Content] = None

    @exception_handler(FileUpdateError)
    def update_file(
        self,
        new_name: Optional[str] = None,
        new_size: Optional[int] = None,
        new_last_modified: Optional[datetime] = None,
        modify_content: Optional[bool] = False,
    ):
        if new_name:
            self.name = new_name
        if new_size:
            self.size = new_size
        if new_last_modified:
            self.last_modified = new_last_modified
        if modify_content:
            self.update_content(self.path)

    @exception_handler(ContentUpdateError)
    def update_content(self):
        path = os.path.join(self.folder.path, self.name)
        self.content = Content(get_file_content(path))

    def __post_init__(self):
        if not self.name:
            raise FileUpdateError("Name must not be empty")


@dataclass
class Folder:
    """Represents a folder in a repository.

    Args:
        name: Folder name
        path: Full path to folder
        files: Dict mapping filename to File objects
        subfolders: Dict mapping folder name to Folder objects

    Returns:
        Folder object

    Raises:
        ValueError: If path or name is empty
    """
    name: str
    path: str
    files: Dict[str, File] = field(default_factory=dict)
    subfolders: Dict[str, "Folder"] = field(default_factory=dict)
    last_modified: Optional[datetime] = None

    @exception_handler(FileUpdateError)
    def update_folder(self):
        """
        Updates the folder by checking for new or modified files and subfolders.
        """
        # update files
        files_list = get_all_files(self.path)
        for file_name in files_list:
            file_path = os.path.join(self.path, file_name)
            file_size = os.path.getsize(file_path)
            last_modified_date = get_last_modified_date(file_path)
            if file_name in self.files and last_modified_date == self.files[file_name].last_modified:
                continue
            elif file_name not in self.files:
                file_size = os.path.getsize(file_path)
                last_modified = get_last_modified_date(file_path)
                self.files[file_name] = File(
                    name=file_name, 
                    folder=self,
                    size=file_size,
                    last_modified=last_modified,
                    content=get_file_content(file_path)
                )
            elif file_size != self.files[file_name].size:
                self.files[file_name].update_file(
                    new_size=file_size,
                    new_last_modified=last_modified,
                    modify_content=True,
                )
        # update subfolders
        folder_list = get_all_folders(self.path)
        for folder_name in folder_list:
            folder_path = os.path.join(self.path, folder_name)
            modified_date = get_last_modified_date(folder_path)
            if folder_name not in self.subfolders:
                self.subfolders[folder_name] = Folder(
                    name=folder_name,
                    path=folder_path,
                    last_modified=modified_date
                )
            
            if modified_date != self.subfolders[folder_name].last_modified:
                self.subfolders[folder_name].update_folder()

    def get_file(self, filename: str) -> Optional[File]:
        """Get a File object by its filename.

        Args:
            filename: Name of the file to retrieve

        Returns:
            File object if found, None otherwise
        """
        return self.files.get(filename)

    def get_subfolder(self, folder_name: str) -> Optional["Folder"]:
        """Get a Folder object by its name.

        Args:
            folder_name: Name of the folder to retrieve

        Returns:
            Folder object if found, None otherwise
        """
        return self.subfolders.get(folder_name)

    def __post_init__(self):
        if not self.path or not self.name:
            raise FileUpdateError("Path and name must not be empty")



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
            raise RepoUpdateError("Repository name and root_folder must not be empty")


# Delete later
if __name__ == "__main__":
    # Create example Folder and File objects

    example_file = File(
        name="example.txt", 
        size=1024,
        last_modified=datetime.now(),
        folder=example_folder,
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