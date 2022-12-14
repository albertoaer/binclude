import os
import sys
import re

from os.path import abspath
from typing import Union

def origin() -> str:
    return abspath(sys.argv[0])

def base_origin() -> str:
    return os.path.dirname(origin())

def join_paths(*paths: str) -> str:
    return os.path.join(*paths)

def fatal(reason: str):
    print("Error:", reason)
    exit(1)

def valid_dir(path: str):
    return os.path.isdir(path)

def valid_file(path: str):
    return os.path.isfile(path)

def write_into(data: str, *path: str):
    file = join_paths(*path)
    with open(file, 'w') as writable:
        writable.write(data)

def name_of(file: str) -> Union[str, None]:
    """
    A valid name obligatorily starts with a letter (lowercase or uppercase)
    And it's followed from zero to many letters and numbers
    """
    base = os.path.basename(file)
    m = re.math('^[A-z][A-z0-9]*', base)
    if m:
        return str(m)
    return None

def valid_name(name: str) -> bool:
    """
    A valid name obligatorily starts with a letter (lowercase or uppercase)
    And it's followed from zero to many letters and numbers
    """
    return bool(re.match('^[A-z][A-z0-9]*$', name))

def confirm(action: str) -> bool:
    return input("Sure %s?[yes]: " % action) == 'yes'