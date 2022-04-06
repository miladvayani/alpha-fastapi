from typing import Tuple
from unittest.mock import patch
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import Mock
from pytest import fixture
from pytest import mark
from pytest import raises
from configs import Development as Test
from UserMS.core.contrib import test_tools
from UserMS.core.contrib import babel

async_mark = mark.asyncio
parameters = mark.parametrize

from UserMS import create_app as setup

# Setup the project
setup(Test())
babel.locale = "en"
from UserMS.data.implements import MongoUserDataLayer


class DataLayerLogicMocks(test_tools.BaseMockCreator):

    path: str = "UserMS.data.implements."

    def __init__(self) -> None:
        self.MongoUserDataLayer: MongoUserDataLayer = ...

    def create_mocks(self):
        super().create_mocks()
        self.MongoUserDataLayer: MongoUserDataLayer = self.MongoUserDataLayer()


mock_manager: test_tools.MockManager[
    Tuple[DataLayerLogicMocks]
] = test_tools.MockManager()

data_layer_mocks: int = 0
