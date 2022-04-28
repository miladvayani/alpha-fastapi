from abc import ABC
from abc import abstractmethod
from unittest.mock import _patch


class MockCreatorInterface(ABC):

    path: str = ...
    patch_list: list[_patch] = []

    @abstractmethod
    def create_mocks(self) -> None:
        ...

    @abstractmethod
    def reset_mocks(self) -> None:
        ...
