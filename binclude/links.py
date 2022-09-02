from typing import List, Set, Tuple

from .db import DB

from .templates import TemplateResult, templates


def build_for_target(target: str, cmd: List[str], attribs: Set[str]) -> TemplateResult:
    return templates[target](cmd, attribs)


def include_link(
    db: DB,
    name: str,
    cmd: List[str],
    link: str,
    interpreter: str,
    attribs: List[str],
    protect: bool
):
    if len(cmd) == 0 or len(cmd) > 2:
        raise ValueError('The command must have between 1 and 2 elements')
    db.add_link(
        name, cmd[-1], cmd[0], link, interpreter, ','.join(attribs), 1 if protect else 0
    )

def rebuild_link(program: str, file: str, link: str, interpreter: str, attribs: str) -> Tuple[str, str]:
    cmd = [program]
    if program != file:
        cmd.append(file)
    result = build_for_target(interpreter, cmd, attribs.split(','))
    return result.output, link