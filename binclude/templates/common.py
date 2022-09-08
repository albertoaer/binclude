from dataclasses import dataclass
from typing import List, Set

#The window flag indicate whether you like not to see the console, used for gui programs
WINDOW_FLAG = 'win'

def wrap_args(args: List[str]) -> List[str]:
    nargs = []
    for arg in args:
        nargs.append(f'"{arg}"')
    return nargs

@dataclass
class TemplateResult():
    """
    The result of building a template, including the formatted template in a string,
    The consumed parameters, the extension that should have the template, and if the result can have no extension
    """
    output: str
    attributes: Set[str]
    extension: str
    allow_no_extension: bool