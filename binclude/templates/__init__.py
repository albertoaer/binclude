from typing import Callable, Dict
from .python import build_template as build_template_py
from .cmd import build_template as build_template_cmd
from .bash import build_template as build_template_bash
from .powershell import build_template as build_template_powershell

from .common import TemplateResult

"""
Templates availables for generating the links
"""
templates: Dict[str, Callable] = {
    'python': build_template_py,
    'cmd': build_template_cmd,
    'bash': build_template_bash,
    'powershell': build_template_powershell
}
