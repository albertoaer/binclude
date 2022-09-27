from typing import Union

from ..db import useDB
from tabulate import tabulate

class SessionController:
    def enable(self, interpreter: str):
        db = useDB()
        db.enable_interpreter(interpreter, True)
        db.commit()

    def disable(self, interpreter: str):
        db = useDB()
        db.enable_interpreter(interpreter, False)
        db.commit()

    def get(self, active: Union[bool, None] = None):
        data = useDB().get_interpreters(active)
        print(tabulate(data, headers=('interpreter', 'is active?')))