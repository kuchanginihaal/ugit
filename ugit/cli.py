import argparse
import os
import ugit.data as data

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
    
    return parser.parse_args()

#Command handler for 'init' command
def init(args):
    data.init()
    print(f"Initialized empty ugit repository in {os.path.abspath(data.GIT_DIR)}")
    