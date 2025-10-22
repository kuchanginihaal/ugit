import argparse
import os
import ugit.data as data
import sys

def main():
    args = parse_args()
    args.func(args)

#Initialize the Command Parser and assign the function  
def parse_args():
    parser = argparse.ArgumentParser()
    
    commands = parser.add_subparsers(dest='command')
    commands.required = True
    
    init_parser = commands.add_parser('init')
    init_parser.set_defaults(func=init)
    
    hash_object_parser = commands.add_parser('hash-object')
    hash_object_parser.set_defaults(func=hash_object)
    hash_object_parser.add_argument('file')
    
    cat_file_parser = commands.add_parser('cat-file')
    cat_file_parser.set_defaults(func=cat_file)
    cat_file_parser.add_argument('object')
    
    return parser.parse_args()

#Command handler for 'init' command
def init(args):
    data.init()
    print(f"Initialized empty ugit repository in {os.path.abspath(data.GIT_DIR)}")
    
def hash_object(args):
    with open(args.file, 'rb') as f:
        print(f"Hash of the file content: {data.hash_object(f.read())}")
        
def cat_file(args):
    sys.stdout.flush()
    sys.stdout.buffer.write(data.get_object(args.object))
    