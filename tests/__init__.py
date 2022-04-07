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

# Setup the project
from UserMS import create_app as setup

setup(Test())
babel.locale = "en"
# Mock Lists
from UserMS.data.implements import MongoUserDataLayer
import requests


class DataLayerLogicMocks(test_tools.BaseMockCreator):

    path: str = "UserMS.data.implements."

    def __init__(self) -> None:
        self.MongoUserDataLayer: MongoUserDataLayer = ...

    def create_mocks(self):
        super().create_mocks()
        self.MongoUserDataLayer: MongoUserDataLayer = self.MongoUserDataLayer()


async_mark = mark.asyncio
parameters = mark.parametrize
mock_manager: test_tools.MockManager[
    Tuple[DataLayerLogicMocks]
] = test_tools.MockManager()
data_layer_mocks: int = 0
