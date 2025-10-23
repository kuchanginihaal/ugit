import os
from pathlib import Path

import ugit.data as data

def write_tree(directory='.'):
    entries = []
    with os.scandir(directory) as it:
        for entry in it:
            full = os.path.join(directory, entry.name)
            if is_ignored(full):
                continue
            if entry.is_file(follow_symlinks=False):
                type_ = 'blob'
                with open(full, 'rb') as f:
                    oid = data.hash_object(f.read())
            elif entry.is_dir(follow_symlinks=False):
                type_ = 'tree'
                oid = write_tree(full)
            entries.append((entry.name, oid, type_))
            
    tree = "".join(f"{type_} {oid} {name}\n" for name, oid, type_ in sorted(entries)).encode()
    return data.hash_object(tree, type_='tree')

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

def _iter_tree_entries(oid):
    if not oid:
        return
    tree_data = data.get_object(oid, expected='tree')
    for entry in tree_data.decode().splitlines():
        type_, oid, name = entry.split(' ', 2)  
        yield type_, oid, name
        
def get_tree(oid,base_path = ''):
    result = {}
    for type_,oid,name in _iter_tree_entries(oid):
        assert'/' not in name
        assert name not in ('.','..')
        path = base_path+name
        if type_ == 'blob':
            result[path] = oid
        elif type_ == 'tree':
            result.update(get_tree(oid,f'{path}/'))
        else:
            raise Exception(f'Unknown tree entry type {type_}')
    return result


def read_tree(tree_oid):
    _empty_current_directory()
    for path,oid in get_tree(tree_oid,base_path='./').items():
        os.makedirs(os.path.dirname(path),exist_ok=True)
        with open(path,'wb') as f:
            f.write(data.get_object(oid))
            
def _empty_current_directory():
    for root,dirnames,filenames in os.walk('.',topdown=False):
        for filename in filenames:
            path = os.path.join(root,filename)
            if is_ignored(path) or not os.path.isfile(path):
                continue
            os.remove(path)
        
        for dirname in dirnames:
            path =  os.path.join(root,dirname)
            if is_ignored(path):    
                continue
            try:
                os.rmdir(path)
            except (FileNotFoundError,OSError):
                pass


          
def commit(message):
    commit = f"tree {write_tree()}\n"
    commit += f"\n{message}\n"
    oid = data.hash_object(commit.encode(),type_='commit')
    data.set_HEAD(oid)
    return oid