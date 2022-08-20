import os
from typing import Union
from .utils import abspath, base_origin, join_paths, origin, valid_dir, write_into
from .builder import create_for_python
from .db import createDB, useDB

BIN_NAME: str = 'binclude'

class CLIController:
    def init(self, dir: str):
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

    def remove(self, file: str):
        pass

    def list(self):
        pass

    def cwd(self):
        print(os.getcwd())

    def whereis(self):
        print(base_origin())

    def repldb(self):
        """
        REPL with the sqlite3 DB

        Opens a REPL and executes the input in the database
        In order to exit just input empty
        """
        db = useDB()
        query: str = '.'
        while query:
            print('sqlite3 > ', end='')
            query = input()
            if query:
                print(db.execute(query))