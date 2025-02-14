import os


def get_git_repo_structure(repo_path):
    """
    Recursively retrieve the structure of a Git repository.

    Args:
        repo_path (str): The local path of the Git repository.

    Returns:
        dict: A nested dictionary representing the directory structure
              of the repository where keys are file/folder names and values
              are either sub-dictionaries (for directories) or file sizes
              (for files).
    """
    # Initialize the structure
    repo_structure = {}

    # Verify if the provided path is a directory
    if not os.path.isdir(repo_path):
        raise ValueError("Provided path is not a valid directory.")

    # Iterate over the directory
    for entry in os.listdir(repo_path):
        entry_path = os.path.join(repo_path, entry)

        if os.path.isdir(entry_path):
            # Recursively add the directory structure
            repo_structure[entry] = get_git_repo_structure(entry_path)
        else:
            # Get the file size (or any other information if needed)
            repo_structure[entry] = os.path.getsize(entry_path)

    return repo_structure
