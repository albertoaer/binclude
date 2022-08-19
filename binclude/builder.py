from typing import List
from importlib import import_module

def create(command: List[str], interpreter: str, lang: str = 'python') -> str:
    """
    Using a template creates a file for running a command with a custom iterpreter
    Arguments:
        command: list of strings that conform the command
        interpreter: interpreter to run the file, example: python, pythonw
        lang: string identifier of the language template, default: python
    """
    template_path = f'templates.{lang}'
    template = import_module(template_path).template
    program = ', '.join(command)
    return template % (interpreter, program)