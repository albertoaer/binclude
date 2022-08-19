template = """#!%s
from subprocess import run
from sys import argv

program = [%s]

run(program + argv[1:])
"""