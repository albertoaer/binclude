from typing import List, Tuple
from importlib import import_module

def escape(_str: str):
    return _str.replace('\\', '\\\\')

def create(command: List[str], interpreter: str, lang: str = 'python') -> str:
    """
    Using a template creates a file for running a command with a custom iterpreter
    Arguments:
        command: list of strings that conform the command
        interpreter: interpreter to run the file, example: python, pythonw
        lang: string identifier of the language template, default: python
    Returns:
        Result formatted template
    """
    template_path = f'templates.{lang}'
    template = import_module(template_path).template
    program = ', '.join(map(lambda c: f"'{escape(c)}'", command))
    return template % (interpreter, program)

def create_for_python(command: List[str], window: bool) -> Tuple[str, str]:
    """
    Abstraction of the generic create function that only targets python
    Arguments:
        command: list of strings that conform the command
        window: if it's true uses pythonw interpreter otherwise python
    Returns:
        Result Tuple[formatted template, interpreter]
    """
    interpreter = 'pythonw' if window else 'python'
    return create(command, interpreter, 'python'), interpreter