from typing import List, Tuple

from .utils import join_paths, write_into
from .db import useDB
from .templates import templates

def save_link(
    name: str,
    program: str,
    file: str,
    interpreter: str,
    attribs: List[str],
    protect: bool
):
    db = useDB()
    dir = db.get_bin_dir()
    db.add_link(
        name, file, program, dir, interpreter, ','.join(attribs), int(protect)
    )

def args_of_link(name: str) -> List[str]:
    db = useDB()
    args = db.active_arguments_of(name)
    return list(map(lambda a: a[0], args))
    

def build_link(name: str) -> Tuple[str, str]:
    db = useDB()
    links = db.link_by_name(name, ['program', 'file', 'attribs', 'interpreter', 'dir', 'name'], False)
    if not links:
        raise ValueError(f'{name} is not a valid link')
    program, file, attribs, interpreter, *ln = links[0]
    args = args_of_link(name)
    cmd = list(filter(lambda x: bool(x), [program, file]))
    template = templates[interpreter](attribs.split(','))
    return template.process(cmd + args), join_paths(*ln)

def write_link(name: str):
    data, link = build_link(name)
    write_into(data, link)