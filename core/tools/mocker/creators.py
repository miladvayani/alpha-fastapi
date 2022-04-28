from typing import List, Union
from typing import Generic
from typing import Type
from typing import Tuple
from typing import TypeVar
from typing import Sequence
from typing import Any

from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import AsyncMock
from unittest.mock import patch

from . import MockCreatorInterface


class BaseMockCreator(MockCreatorInterface):
    def create_mocks(self):
        mocks: List[str] = self.__dict__.keys()
        for mock in mocks:
            PatchObject = patch(self.path + mock)
            self.patch_list.append(PatchObject)
            MockObject = PatchObject.start()
            setattr(self, mock, MockObject)

    def reset_mocks(self) -> None:
        for patch in self.patch_list:
            patch.stop()
