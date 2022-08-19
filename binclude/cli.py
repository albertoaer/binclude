from typing import List
from .utils import fatal, base_origin, origin
from .builder import create

class CLIController:
    def init(self, folder: str):
        payload = create(['python', origin()], 'python')
        print(payload)

    def add(self, cmd: List[str], test: bool = False, hide: bool = False):
        pass

    def remove(self, file: str):
        pass

    def list(self):
        pass

    def whereis(self):
        print(base_origin())