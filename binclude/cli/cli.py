import os
from typing import Set, Union
from tabulate import tabulate

from .args import ArgsController
from .session import SessionController

from ..links import save_link, rebuild_link, write_link
from ..utils import abspath, base_origin, confirm, name_of, origin, valid_dir, valid_name, write_into
from ..templates import templates
from ..db import createDB, useDB

BIN_NAME: str = 'binclude'

class CLIController:
    def __init__(self) -> None:
        self.session = SessionController()
        self.args = ArgsController()

    def init(self, dir: str):
        dir = abspath(dir)
        if not valid_dir(dir):
            raise Exception('Expecting valid directory')
        db = createDB()
        db.add_bin_dir(dir)
        db.commit()
        self.add(origin(), BIN_NAME, 'python', p=True)

    def add(self, file: str, n: str = "", u: str = "", a: Set = set(), p: bool = False):
        db = useDB()
        name = n or name_of(file)
        if not name or not valid_name(name):
            raise ValueError('Invalid name, format: (letter)[... letters and numbers]')
        # Create the required data
        cmd = [u if u else abspath(file)]
        attrs = a or {}
        active_interpreters = db.get_interpreters(True)
        valid_interpreters = filter(lambda x: x in templates, map(lambda x: x[0], active_interpreters))

        registered_names = []

        for interpreter_name in valid_interpreters:
            template = templates[interpreter_name](attrs)
            lnname = name
            if not template.allow_no_extension or name in registered_names:
                lnname += template.extension
            registered_names.append(lnname)
            # If there is an error in the database like repeated name, the file won't be written
            link = save_link(lnname, cmd, interpreter_name, attrs, p)
            write_link(template.process(cmd), link)
            db.commit()

    def restore(self, name: str, deep: bool = False):
        """
        Restores a physical link file from the database
        Arguments:
            name: the link name
        """
        db = useDB()
        res = db.link_by_name(name, ['program', 'file', 'dir', 'interpreter', 'attribs'], deep)
        if not res:
            raise Exception(f'Not found: {name}')
        for x in res:
            if not res:
                raise Exception(f'Not found: {name}')
            output, link = rebuild_link(*x)
            write_into(output, link)

    def repair(self):
        """
        Restores al the links stored in the database
        """
        db = useDB()
        for res in db.links(['program', 'file', 'dir', 'interpreter', 'attribs']):
            output, link = rebuild_link(*res)
            write_into(output, link)

    def remove(self, name: str, force: bool = False, deep: bool = False, purge: bool = False):
        """
        Removes the physical file associated to a name
        The link will remain in the database
        Arguments:
            name: the link name
            force: force the remove (used for protected links)
        """
        db = useDB()
        res = db.link_by_name(name, ['dir', 'state'], deep)
        if not res:
            raise Exception(f'Not found: {name}')
        for x in res:
            #The link must not be protected or the removal must be forced to proceed
            if x[1] == 1 and not force:
                raise Exception('Trying to remove protected link, use --force if you are sure')
            try:
                os.remove(x[0])
                print("Removed", x[0])
            except Exception as e:
                print("INFO ERR:", e)
        if purge:
            db.remove_link(name, deep)
            if confirm('purge'):
                db.commit()
                print("Purged", name, 'deep' if deep else '')

    def ls(self, short: bool = False):
        """
        Get all the links

        list() prints all the links registered in the db
        """
        headers = 'name', 'file', 'program', 'dir', 'interpreter', 'attribs', 'state'
        if short:
            headers = 'name', 'file', 'dir', 'state'
        links = useDB().links(headers)
        print(tabulate(links, headers=headers))

    def cwd(self):
        """
        Binclude cwd

        cwd() prints the current working directory
        """
        print(os.getcwd())

    def whereis(self):
        """
        Binclude location

        whereis() prints the binclude's location
        """
        print(base_origin())

    def repldb(self):
        """
        REPL with the sqlite3 DB

        repldb() opens a REPL and executes the input in the database
        In order to exit just input empty
        """
        db = useDB()
        query: str = '.'
        while query:
            print('sqlite3 > ', end='')
            query = input()
            if query:
                print(db.execute(query))
