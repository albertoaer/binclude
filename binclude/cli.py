import os
from typing import Set, Union
from tabulate import tabulate

from .utils import abspath, base_origin, join_paths, origin, valid_dir, write_into
from .templates import templates, TemplateResult
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
        self.add(origin(), BIN_NAME, 'python', protect=True)

    def add(
        self,
        file: str,
        name: str,
        uses: Union[str, None] = None,
        attribs: Union[Set[str], None] = None,
        protect: bool = False
    ):
        db = useDB()

        # Create the required data
        cmd = [abspath(file)]
        if uses:
            cmd.insert(0, uses)
        if not attribs:
            attribs = {}
        dir = db.get_bin_dir()
        interpreters = ['bash', 'python', 'cmd', 'powershell']

        registered_names = []

        for target in interpreters:
            if target in templates:
                result: TemplateResult = templates[target](cmd, attribs)
                lnname = name
                if not result.allow_no_extension or name in registered_names:
                    lnname += result.extension
                registered_names.append(lnname)
                link = join_paths(dir, lnname)

                # If there is an error in the database like repeated name,
                # the file won't be written
                db.add_link(
                    lnname, cmd[-1], cmd[0], link,
                    target, ','.join(result.attributes), 1 if protect else 0
                )
                write_into(result.output, link)
                db.commit()

    def restore(self, name: str):
        db = useDB()
        res = db.link_by_name(name, ['program', 'file', 'link', 'interpreter', 'attribs'])
        if not res:
            raise Exception(f'Not found: {name}')
        cmd = res[:2]
        if cmd[0] == cmd[1]:
            cmd = cmd[:1]
        link = res[2]
        interpreter = res[3]
        attribs = res[4].split(',')
        result: TemplateResult = templates[interpreter](cmd, attribs)
        write_into(result.output, link)

    def remove(self, name: str, force: bool = False):
        pass

    def repair(self):
        pass

    def list(self, short: bool = False):
        """
        Get all the links

        list() prints all the links registered in the db
        """
        headers = 'name', 'file', 'program', 'link', 'interpreter', 'attribs', 'state'
        if short:
            headers = 'name', 'file', 'link', 'state'
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
