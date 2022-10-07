from typing import List, Tuple, Union
import os
import sqlite3
from .utils import base_origin, join_paths

DB_FILE: str = 'binclude.db'

def db_path():
    return join_paths(base_origin(), DB_FILE)

class DBException(Exception):
    pass

class DB:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.cur = self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def execute(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()

    def execute_script(self, name):
        script = join_paths(base_origin(), 'sql', name)
        with open(script) as file:
            self.cur.executescript(file.read())
        self.commit()

    def setup(self):
        self.execute_script('setup.sql')

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def add_bin_dir(self, route: str):
        self.cur.execute('INSERT INTO bin_dirs VALUES(?)', (route,))

    def get_bin_dir(self) -> str:
        self.cur.execute('SELECT route FROM bin_dirs')
        return self.cur.fetchone()[0]

    def add_link(self, name: str, file: str, program: str, dir: str, interpreter: str, attributes: str, state: int):
        self.cur.execute('INSERT INTO links VALUES(?, ?, ?, ?, ?, ?, ?)',
                         (name, file, program, dir, interpreter, attributes, state))

    def links(self, columns: List[str]) -> list:
        self.cur.execute(f"SELECT {', '.join(columns)} FROM links")
        return self.cur.fetchall()

    def link_by_name(self, name: str, columns: List[str], also_like: bool) -> list:
        query = f"SELECT {', '.join(columns)} FROM links WHERE name = ?"
        items = [name,]
        if also_like:
            query += ' OR name LIKE ?'
            items.append(name + ".%")
        self.cur.execute(query, items)
        return self.cur.fetchall()

    def remove_link(self, name: str, also_like: bool):
        query = 'DELETE FROM links WHERE name = ?'
        items = [name,]
        if also_like:
            query += ' OR name LIKE ?'
            items.append(name + '.%')
        self.cur.execute(query, items)

    def enable_interpreter(self, name: str, do: bool):
        self.cur.execute('UPDATE interpreters SET active = ? WHERE name = ?', (int(do), name))

    def get_interpreters(self, filter: Union[bool, None] = None) -> List[Tuple[str, bool]]:
        query = 'SELECT name, active FROM interpreters'
        items = []
        if filter != None:
            query += ' WHERE active = ?'
            items.append(int(filter))
        self.cur.execute(query, items)
        return list(map(lambda f: (f[0], bool(f[1])), self.cur.fetchall()))

    def add_argument(self, linkname: str, position: int, value: str):
        self.cur.execute(
            'SELECT MAX(relative) FROM arguments WHERE linkname = ? AND position = ?',
            (linkname, position)
        )
        elem = self.cur.fetchone()
        relative = 0 if elem[0] is None else elem[0] + 1
        self.cur.execute('INSERT INTO arguments VALUES(?,?,?,?,?)', (linkname, position, relative, value, 1))

    def arguments(self, columns: List[str]) -> list:
        self.cur.execute(f"SELECT {', '.join(columns)} FROM arguments")
        return self.cur.fetchall()

    def remove_argument(self, id: str):
        self.cur.execute(
            "DELETE FROM arguments WHERE linkname||':'||position||':'||relative = ?",
            (id,)
        )

    def update_argument(self, id: str, value: str):
        self.cur.execute(
            "UPDATE arguments SET value = ? WHERE linkname||':'||position||':'||relative = ?",
            (value, id)
        )

    def enable_interpreter(self, id: str, do: bool):
        self.cur.execute(
            "UPDATE arguments SET active = ? WHERE linkname||':'||position||':'||relative = ?",
            (int(do), id)
        )

openedDB: Union[DB, None] = None

def createDB() -> DB:
    global openedDB
    if openedDB or os.path.exists(db_path()):
        raise DBException('Database aready created')
    openedDB = DB(db_path())
    openedDB.setup()
    return openedDB


def useDB() -> DB:
    global openedDB
    if openedDB:
        return openedDB
    if not os.path.exists(db_path()):
        raise DBException('No database created')
    openedDB = DB(db_path())
    return openedDB
