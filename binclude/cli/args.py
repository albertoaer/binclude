from tabulate import tabulate

from ..db import useDB

class ArgsCreator:
    def start(self, matcher: str, value: str):
        self.at(0, matcher, value)

    def middle(self, matcher: str, value: str):
        self.at(1, matcher, value)
    
    def end(self, matcher: str, value: str):
        self.at(2, matcher, value)

    def at(self, position: int, matcher: str, value: str):
        db = useDB()
        if value:
            db.add_argument(matcher, position, value)
        db.commit()

class ArgsController:
    def __init__(self) -> None:
        self.new = ArgsCreator()

    def ls(self):
        args = map(
            lambda x: (x[0], x[1], bool(x[2])),
            useDB().arguments(["linkname||':'||position||':'||relative", 'value', 'active'])
        )
        print(tabulate(args, ['identifier', 'value', 'is active?']))

    def update(self, id: str, value: str):
        db = useDB()
        if not value:
            db.remove_argument(id)
        else:
            db.update_argument(id, value)
        db.commit()

    def enable(self, id: str):
        db = useDB()
        db.enable_interpreter(id, True)
        db.commit()

    def disable(self, id: str):
        db = useDB()
        db.enable_interpreter(id, False)
        db.commit()