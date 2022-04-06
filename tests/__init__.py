from typing import Tuple
from unittest.mock import patch
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import Mock
from faker import Faker
from pytest import fixture
from pytest import mark

from configs import Development as Test
from UserMS.core.contrib import test_tools

async_mark = mark.asyncio
parameters = mark.parametrize


faker = Faker()
from UserMS import create_app as setup

# Setup the project
setup(Test())

from UserMS.data.implements import MongoUserDataLayer


class ExternalLegalLogicMocks(test_tools.BaseMockCreator):

    path: str = "UserMS.controllers.external.logic.legal."

    def __init__(self) -> None:
        self.DataLayer: MongoUserDataLayer = ...


class ExternalUserLogicMocks(test_tools.BaseMockCreator):

    path: str = "UserMS.controllers.external.logic.user."

    def __init__(self) -> None:
        self.DataLayer: MongoUserDataLayer = ...


mock_manager: test_tools.MockManager[
    Tuple[ExternalLegalLogicMocks, ExternalUserLogicMocks]
] = test_tools.MockManager()

legal_mocks: int = 0
user_mocks: int = 1
