from typing import Type, Dict
from .python import PythonTemplate
from .cmd import CmdTemplate
from .bash import BashTemplate
from .powershell import PowershellTemplate

from .common import Template

"""
Templates availables for generating the links
"""
templates: Dict[str, Type[Template]] = {
    'python': PythonTemplate,
    'cmd': CmdTemplate,
    'bash': BashTemplate,
    'powershell': PowershellTemplate
}
