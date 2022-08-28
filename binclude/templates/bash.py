from typing import List, Set

from .common import TemplateResult

def replace_slash(items: List[str]):
    narr = []
    for v in items:
        narr.append(v.replace('\\', '/'))
    return narr

template = """#!/bin/sh
{target} "$@"
exit $?"""

def build_template(target: List[str], attrs: Set[str]) -> TemplateResult:
    formatted = template.format(target=' '.join(replace_slash(target)))
    return TemplateResult(formatted, {}, '.sh', True)
