import os
import hashlib

GIT_DIR = '.ugit'

def init():
    os.makedirs(GIT_DIR)
    os.makedirs(os.path.join(GIT_DIR, 'objects'))
    
def hash_object(data,type_='blob'):
    obj = type_.encode() + b'\x00' + data
    oid = hashlib.sha1(obj).hexdigest()
    with open(os.path.join(GIT_DIR, 'objects', oid), 'wb') as out:
        out.write(obj)
    return oid

def get_object(oid, expected='blob'):
    with open(os.path.join(GIT_DIR, 'objects', oid), 'rb') as f:
        obj = f.read()
        
    type_, _, content = obj.partition(b'\x00')
    type_ = type_.decode()
    
    if expected and type_ != expected:
        raise Exception(f'Expected object of type {expected}, got {type_}')
    
    return content

def update_ref(ref,oid):
    ref_path = os.path.join(GIT_DIR,ref)
    os.makedirs(os.path.dirname(ref_path),exist_ok=True)
    with open(ref_path,'w') as f:
        f.write(oid)  
        
def get_ref(ref):
    ref_path = os.path.join(GIT_DIR,ref)
    if not os.path.exists(ref_path):
        return None
    if os.path.isfile(ref_path):
        with open(ref_path,'r') as f:
            return f.read().strip()

