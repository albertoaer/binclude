import os
import sys

from os.path import abspath

def origin() -> str:
    return abspath(sys.argv[0])

def base_origin() -> str:
    return os.path.dirname(origin())

def join_paths(*paths: str) -> str:
    return os.path.join(*paths)

def fatal(reason: str):
    print("Error:", reason)
    exit(-1)

def valid_dir(path: str):
    return os.path.isdir(path)

def valid_file(path: str):
    return os.path.isfile(path)

def write_into(data: str, *path: str):
    file = join_paths(*path)
    with open(file, 'w') as writable:
        writable.write(data)