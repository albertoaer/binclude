from typing import List, Set

from .common import TemplateResult, wrap_args

def replace_slash(items: List[str]) -> List[str]:
    narr = []
    for v in items:
        narr.append(v.replace('\\', '/'))
    return narr

template = """#!/bin/sh
{target} "$@"
exit $?"""

def build_template(target: List[str], _: Set[str]) -> TemplateResult:
    args = wrap_args(replace_slash(target))
    formatted = template.format(target=' '.join(args))
    return TemplateResult(formatted, {}, '.sh', True)
