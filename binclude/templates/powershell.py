from typing import List, Set

from .common import Template


template = """& "{target}" $args
exit $LASTEXITCODE"""

class PowershellTemplate(Template):
    @property
    def extension(self) -> str:
        return '.ps1'
        
    @property
    def consumed(self) -> Set[str]:
        return set()

    def process(self, target: List[str]) -> str:
        return template.format(target=' '.join(target))