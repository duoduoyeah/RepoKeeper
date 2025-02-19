import sqlite3
from pathlib import Path
import hashlib

def code_to_db(repo_path: str, db_path: str) -> None:
    """
    Convert a repository into a SQLite database of code files.

    Args:
        repo_path: Path to the repository.
        db_path: Path to the SQLite database.

    Returns:
        None
    """
    # Create/connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table for code files
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS code_files (
            id TEXT PRIMARY KEY,
            file_path TEXT,
            content TEXT,
            language TEXT,
            size INTEGER
        )
    ''')
    
    # Walk through repository
    for file_path in Path(repo_path).rglob('*'):
        if file_path.is_file() and not str(file_path).startswith('.'):
            try:
                # Read file content
                content = file_path.read_text()
                
                # Generate unique ID
                file_id = hashlib.md5(str(file_path).encode()).hexdigest()
                
                # Guess language from extension
                language = file_path.suffix.lstrip('.')
                
                # Insert into database
                cursor.execute(
                    'INSERT OR REPLACE INTO code_files VALUES (?, ?, ?, ?, ?)',
                    (file_id, str(file_path), content, language, len(content))
                )
                
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
    
    conn.commit()
    conn.close()

# Usage example
repo_path = "./tinycc"
db_path = "./data/code_database.sqlite"
code_to_db(repo_path, db_path)