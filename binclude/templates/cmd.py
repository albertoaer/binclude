from typing import List, Set

from .common import TemplateResult, wrap_args


template = """@ECHO off
{target} %*
EXIT /b %errorlevel%
"""

def build_template(target: List[str], _: Set[str]) -> TemplateResult:
    return TemplateResult(template.format(target=' '.join(wrap_args(target))), {}, '.cmd', False)
