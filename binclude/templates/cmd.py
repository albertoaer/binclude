from typing import List, Set

from .common import Template, wrap_args


template = """@ECHO off
{target} %*
EXIT /b %errorlevel%
"""

class CmdTemplate(Template):
    @property
    def extension(self) -> str:
        return '.cmd'

    @property
    def consumed(self) -> Set[str]:
        return set()

    def process(self, target: List[str]) -> str:
        return template.format(target=' '.join(wrap_args(target)))