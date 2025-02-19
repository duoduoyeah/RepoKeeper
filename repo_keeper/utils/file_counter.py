import os
from typing import Optional

def count_files(
    path: str, 
    file_type: str,
    ignore_dirs: Optional[list[str]] = None,
    depth: int = -1,
) -> int:
    count = 0
    for root, _, files in os.walk(path):

        current_depth = root.replace(path, '').count(os.sep)
        if depth != -1 and current_depth > depth:
            continue
    
        if ignore_dirs:
            if any(ignore_dir in root for ignore_dir in ignore_dirs):
                continue

        if current_depth == depth:
            print(root, current_depth)

        for file in files:
            if file.endswith(file_type):
                count += 1
    return count

def count_lines(path: str) -> int:
    with open(path, "r") as f:
        return sum(1 for _ in f)

def count_multi_file(
    path: str,
    file_types: list[str],
    ignore_dirs: Optional[list[str]] = None,
    depth: int = -1,
) -> list[int]:
    counts: list[int] = []
    for file_type in file_types:
        counts.append(count_files(path, file_type, ignore_dirs, depth))
    return counts

if __name__ == "__main__":
    print(count_multi_file(
        "/workspaces/interesting_repo/tinycc", 
        [".cc", ".h", ".c"], 
        ignore_dirs=["astra-sim/extern", ".git"],
        depth=-1,
    ))
