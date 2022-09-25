from typing import Union

from binclude.db import useDB
from tabulate import tabulate

class SessionController:
    def use(self, interpreter: str):
        db = useDB()
        db.use_interpreter(interpreter, True)
        db.commit()

    def unuse(self, interpreter: str):
        db = useDB()
        db.use_interpreter(interpreter, False)
        db.commit()

    def get(self, active: Union[bool, None] = None):
        data = useDB().get_interpreters(active)
        print(tabulate(data, headers=('interpreter', 'is active?')))