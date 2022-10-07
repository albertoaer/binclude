from typing import List, Tuple

from .utils import join_paths, write_into
from .db import useDB
from .templates import templates

def save_link(
    name: str,
    cmd: List[str],
    interpreter: str,
    attribs: List[str],
    protect: bool
) -> str:
    if len(cmd) == 0 or len(cmd) > 2:
        raise ValueError('The command must have between 1 and 2 elements')
    db = useDB()
    dir = db.get_bin_dir()
    db.add_link(
        name, cmd[-1], cmd[0], dir, interpreter, ','.join(attribs), int(protect)
    )
    return join_paths(dir, name)

def rebuild_link(program: str, file: str, link: str, interpreter: str, attribs: str) -> Tuple[str, str]:
    cmd = [program]
    if program != file:
        cmd.append(file)
    template = templates[interpreter](attribs.split(','))
    return template.process(cmd), link

def write_link(data: str, link: str):
    dir = useDB().get_bin_dir()
    write_into(data, dir, link)