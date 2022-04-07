from typing import List


from . import mock_manager
from . import AsyncMock
from . import Mock
from . import async_mark
from . import data_layer_mocks
from . import raises
from . import patch

from UserMS.controllers.external.logic.user import UserRepository
from UserMS.controllers.internal.logic.user import (
    UserRepository as InternalUserRepository,
)
from UserMS.core.rabbit.exceptions import RabbitException
from bson import ObjectId
from fastapi import HTTPException


@async_mark
async def test_get_user_by_id_user_found():
    # Setup
    user_id: ObjectId = ObjectId()
    user: dict = dict(_id=user_id)
    get_current_user = mock_manager.mocks[
        data_layer_mocks
    ].MongoUserDataLayer.get_current_user = AsyncMock()
    get_current_user.return_value = user
    repository = UserRepository()
    # Action
    found_user = await repository.get_user(user_id)
    # Assert
    assert found_user == user
    assert found_user["_id"] == user["_id"]
    assert get_current_user.called


@async_mark
async def test_get_user_by_id_user_not_found():
    # Setup
    user = None
    get_current_user = mock_manager.mocks[
        data_layer_mocks
    ].MongoUserDataLayer.get_current_user = AsyncMock()
    get_current_user.return_value = user
    repository = UserRepository()
    # Action
    with raises(HTTPException) as errors:
        await repository.get_user(ObjectId())

    assert errors.value.detail == "No Such User Exists"
    assert errors.value.status_code == 404


@patch("UserMS.controllers.external.logic.user.validators.validate_job")
@async_mark
async def test_update_user(validate_job: AsyncMock):
    # Setup
    update_user = mock_manager.mocks[
        data_layer_mocks
    ].MongoUserDataLayer.update_user = AsyncMock()
    repository = UserRepository()
    user: dict = dict(_id=ObjectId(), first_name="Parsa", job="gamer")
    data: dict = dict(first_name="Ali", job="programmer")
    # Action
    await repository.update_user(user, data)
    # Assert
    assert user["first_name"] == "Ali" and user["job"] == "programmer"
    assert update_user.called
    assert validate_job.called


@async_mark
async def test_get_user_by_id_has_found():
    # Setup
    get_current_user = mock_manager.mocks[
        data_layer_mocks
    ].MongoUserDataLayer.get_current_user = AsyncMock()
    user_id = ObjectId()
    get_current_user.return_value = dict(_id=user_id)
    repository = InternalUserRepository()
    # Action
    found_user = await repository.get_user_by_id(user_id=user_id)
    # Assert
    assert found_user["_id"] == user_id
    assert get_current_user.called


@async_mark
async def test_get_user_by_id_not_found():
    # Setup
    get_current_user = mock_manager.mocks[
        data_layer_mocks
    ].MongoUserDataLayer.get_current_user = AsyncMock()
    get_current_user.return_value = None
    repository = InternalUserRepository()
    # Action
    with raises(RabbitException) as errors:
        await repository.get_user_by_id(user_id=ObjectId())
    # Assert
    assert get_current_user.called
    assert errors.value.status == 0


@async_mark
async def test_set_user_by_mobile():
    # Setup 1
    repository = InternalUserRepository()
    get_user_by_mobile = mock_manager.mocks[
        data_layer_mocks
    ].MongoUserDataLayer.get_user_by_mobile = AsyncMock()
    insert_user = mock_manager.mocks[
        data_layer_mocks
    ].MongoUserDataLayer.insert_user = AsyncMock()
    insert_user.return_value = dict(_id=ObjectId())
    # ---1
    get_user_by_mobile.return_value = None
    # Action 1
    result = await repository.set_user_by_mobile("1111111111")

    # Assert 1
    assert insert_user.called
    assert get_user_by_mobile.called
    assert "_id" in result

    # Setup 2
    get_user_by_mobile.reset_mock()
    insert_user.reset_mock()
    insert_user.return_value = None
    get_user_by_mobile.return_value = dict(_id=ObjectId())
    # Action 2
    result = await repository.set_user_by_mobile("1111111111")
    # Assert 2
    assert "_id" in result
    assert not insert_user.called


@async_mark
async def test_update_one_user():
    # Setup 1
    repository = InternalUserRepository()
    update_user = mock_manager.mocks[
        data_layer_mocks
    ].MongoUserDataLayer.update_user = AsyncMock()
    update_user.return_value = (None, 0)
    
    # Action 1

