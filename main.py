#!python
from binclude import *
import fire

if __name__ == '__main__':
    try:
        fire.Fire(CLIController)
    except Exception as e:
        fatal(e)