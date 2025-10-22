import os
from pathlib import Path

import ugit.data as data

def write_tree(directory='.'):
    with os.scandir(directory) as it:
        for entry in it:
            full = os.path.join(directory, entry.name)
            if is_ignored(full):
                continue
            if entry.is_file(follow_symlinks=False):
                print(f"File: {full}")
            elif entry.is_dir(follow_symlinks=False):
                write_tree(full)

def is_ignored(path):
    if '.ugit' in Path(path).parts:
        return True
    elif '.git' in Path(path).parts:
        return True
    elif '__pycache__' in Path(path).parts:
        return True
    elif 'ugit.egg-info' in Path(path).parts:
        return True
    else:
        return False