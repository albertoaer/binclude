import os
import sys

def abs(path: str) -> str:
    return os.path.abspath(path)

def origin() -> str:
    return abs(sys.argv[0])

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