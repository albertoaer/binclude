import os
from typing import Union
from tabulate import tabulate

from .utils import abspath, base_origin, join_paths, origin, valid_dir, write_into
from .builder import create_for_python
from .db import createDB, useDB

BIN_NAME: str = 'binclude'

class CLIController:
    def init(self, dir: str):
        dir = abspath(dir)
        if not valid_dir(dir):
            raise Exception('Expecting valid directory')
        db = createDB()
        db.add_bin_dir(dir)
        db.commit()
        self.add(origin(), BIN_NAME, 'python', False, False)

    def add(self, file: str, name: str, uses: Union[str, None] = None, test: bool = False, hide: bool = False):
        db = useDB()
        cmd = [abspath(file)]
        if uses:
            cmd.insert(0, uses)
        payload, interpreter = create_for_python(cmd, hide)
        dir = db.get_bin_dir()
        link = join_paths(dir, name)
        db.add_link(name, cmd[len(cmd)-1], cmd[0], link, interpreter, 0)
        write_into(payload, link)
        db.commit()

    def restore(self, name: str):
        pass

    def remove(self, name: str, force: bool = False):
        pass

    def repair(self):
        pass

    def list(self):
        """
        Get all the links

        list() prints all the links registered in the db
        """
        links = useDB().links()
        print(tabulate(links, headers=('name', 'file', 'program', 'link', 'interpreter', 'state')))

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