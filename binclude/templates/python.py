from typing import List, Set

from .common import WINDOW_FLAG, Template

def escape(_str: str):
    return _str.replace('\\', '\\\\')

template_base = """from subprocess import run
from sys import argv

program = [{target}]

code = run(program + argv[1:]).returncode
exit(code)
"""

python = '#!python\n' + template_base
pythonw = '#!pythonw\n' + template_base

class PythonTemplate(Template):
    @property
    def extension(self) -> str:
        return '.pyw' if WINDOW_FLAG in self.attrs else '.py'

    @property
    def allow_no_extension(self) -> bool:
        return True

    @property
    def consumed(self) -> Set[str]:
        res = set()
        if WINDOW_FLAG in self.attrs:
            res.add(WINDOW_FLAG)
        return res

    def process(self, target: List[str]) -> str:
        template = pythonw if WINDOW_FLAG in self.attrs else python
        return template.format(target=', '.join(map(lambda c: f"'{escape(c)}'", target)))