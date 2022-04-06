from typing import List, Tuple
from typing import Any
from typing import TypeVar
from typing import Generic
from .interface import MockCreatorInterface

MOCKCREATOR = TypeVar("MOCKCREATOR")


class MockManager(Generic[MOCKCREATOR]):

    created: bool = False

    def __init__(self) -> None:
        self.__mock_creators: MOCKCREATOR = []
        MockManager.created = True

    def add_creator(self, creator: MOCKCREATOR) -> None:
        if not MockManager.created:
            self.__mock_creators.append(creator())

    def build(self):
        if not MockManager.created:
            for creator in self.__mock_creators:
                creator.create_mocks()

    def reset(self):
        if not MockManager.created:
            for creator in self.__mock_creators:
                creator.reset_mocks()
        self.__mock_creators.clear()
        MockManager.created = False

    @property
    def mocks(self) -> MOCKCREATOR:
        return self.__mock_creators
