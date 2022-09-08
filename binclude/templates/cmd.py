from typing import List, Set

from .common import TemplateResult


template = """@ECHO off
"{target}" %*
EXIT /b %errorlevel%
"""

def build_template(target: List[str], attrs: Set[str]) -> TemplateResult:
    return TemplateResult(template.format(target=' '.join(target)), {}, '.cmd', False)
