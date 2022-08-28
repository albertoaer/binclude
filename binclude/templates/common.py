from dataclasses import dataclass
from typing import Set

#The window flag indicate whether you like not to see the console, used for gui programs
WINDOW_FLAG = 'win'

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