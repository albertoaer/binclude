from typing import List, Set

from .common import WINDOW_FLAG, TemplateResult

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


def build_template(target: List[str], attrs: Set[str]) -> TemplateResult:
    res: Set[str] = {}
    template = python
    ext = '.py'
    if WINDOW_FLAG in attrs:
        res.add(WINDOW_FLAG)
        template = pythonw
        ext = '.pyw'
    formatted = template.format(target=', '.join(map(lambda c: f"'{escape(c)}'", target)))
    return TemplateResult(formatted, res, ext, True)
