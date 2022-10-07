from typing import List, Set

from .common import Template, wrap_args

def replace_slash(items: List[str]) -> List[str]:
    narr = []
    for v in items:
        narr.append(v.replace('\\', '/'))
    return narr

template = """#!/bin/sh
{target} "$@"
exit $?"""

class BashTemplate(Template):
    @property
    def extension(self) -> str:
        return '.sh'

    @property
    def allow_no_extension(self) -> bool:
        return True

    @property
    def consumed(self) -> Set[str]:
        return set()

    def process(self, target: List[str]) -> str:
        args = wrap_args(replace_slash(target))
        return template.format(target=' '.join(args))