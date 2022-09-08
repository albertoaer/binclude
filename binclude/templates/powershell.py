from typing import List, Set

from .common import TemplateResult


template = """& "{target}" $args
exit $LASTEXITCODE"""

def build_template(target: List[str], attrs: Set[str]) -> TemplateResult:
    return TemplateResult(template.format(target=' '.join(target)), {}, '.ps1', False)