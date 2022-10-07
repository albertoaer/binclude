from abc import ABC, abstractmethod
from typing import List, Set

#The window flag indicate whether you like not to see the console, used for gui programs
WINDOW_FLAG = 'win'

def wrap_args(args: List[str]) -> List[str]:
    nargs = []
    for arg in args:
        nargs.append(f'"{arg}"')
    return nargs

class Template(ABC):
    def __init__(self, attrs: Set[str]) -> None:
        self.attrs = attrs

    @property
    @abstractmethod
    def extension(self) -> str:
        pass

    @property
    def allow_no_extension(self) -> bool:
        return False

    @property
    @abstractmethod
    def consumed(self) -> Set[str]:
        pass

    @abstractmethod
    def process(self, target: List[str]) -> str:
        pass