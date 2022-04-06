from typing import List

from . import mock_manager
from . import AsyncMock
from . import async_mark
from . import data_layer_mocks
from . import raises

from UserMS.controllers.external.logic.legal import LegalRepository
from bson import ObjectId
from fastapi import HTTPException


def test_check_user_info_buyer_id_is_None():
    # Setup
    repository = LegalRepository()
    user: dict = dict(buyer_id=None)
    # Action
    with raises(HTTPException) as errors:
        repository.check_user_info(user)
    # Assert
    assert errors.value.status_code == 400
    assert errors.value.detail == "Please complete your personal information first"


def test_check_user_info_buyer_id_is_not_None():
    # Setup
    repository = LegalRepository()
    user: dict = dict(buyer_id="real")
    # Action
    result = repository.check_user_info(user)
    # Assert
    assert result is None


def test_check_legal_duplicate_in_post():
    # Setup
    repository = LegalRepository()
    legals: List[dict] = [dict(buyer_id="1111111111"), dict(buyer_id="2222222222")]
    buyer_id: str = "1111111111"
    # Action
    with raises(HTTPException) as errors:
        repository.check_legal_duplicate_in_post(legals, buyer_id)
    # Assert
    assert errors.value.status_code == 400
    assert errors.value.detail == "Legal info already exists"


@async_mark
async def test_add_legal():
    # Setup
    add_legal_for_user = mock_manager.mocks[
        data_layer_mocks
    ].MongoUserDataLayer.add_legal_for_user = AsyncMock()
    repository = LegalRepository()

    inserted_id = add_legal_for_user.return_value = ObjectId()
    # Action
    result = await repository.add_legal(ObjectId(), legal_data=dict())
    # Assert
    assert result == {"_id": inserted_id}
    assert add_legal_for_user.called


def test_check_legal_duplicate_in_update_legal_info_founded_and_is_used_True():
    # Setup
    buyer_id = "1111111111"
    new_legal_id = ObjectId()
    legals: List[dict] = [dict(_id=new_legal_id, buyer_id=buyer_id, is_used=True)]
    repository = LegalRepository()
    # Action
    with raises(HTTPException) as errors:
        repository.check_legal_duplicate_in_update(
            legals, new_buyer_id=buyer_id, new_legal_id=new_legal_id
        )
    assert errors.value.status_code == 400
    assert errors.value.detail == "Legal info in use"


def test_check_legal_duplicate_in_update_legal_info_founded_and_buyer_id_exists_in_legal_info():
    # Setup
    buyer_id = "1111111111"
    new_legal_id = ObjectId()
    legals: List[dict] = [dict(_id=ObjectId(), buyer_id=buyer_id, is_used=False)]
    repository = LegalRepository()
    # Action
    with raises(HTTPException) as errors:
        repository.check_legal_duplicate_in_update(
            legals, new_buyer_id=buyer_id, new_legal_id=new_legal_id
        )
    # Assert
    assert errors.value.status_code == 400
    assert errors.value.detail == "Legal info already exists"


def test_check_legal_duplicate_in_update_legal_not_found():
    # Setup
    buyer_id = "1111111111"
    new_legal_id = ObjectId()
    legals: List[dict] = [dict(_id=new_legal_id, buyer_id=buyer_id, is_used=False)]
    repository = LegalRepository()
    # Action
    with raises(HTTPException) as errors:
        repository.check_legal_duplicate_in_update(
            legals, new_buyer_id="2222222222", new_legal_id=ObjectId()
        )
    # Assert
    assert errors.value.status_code == 404
    assert errors.value.detail == "Legal info not found"


def test_check_legal_duplicate_in_update_valid_case():
    # Setup
    buyer_id = "1111111111"
    new_legal_id = ObjectId()
    legals: List[dict] = [dict(_id=new_legal_id, buyer_id=buyer_id, is_used=False)]
    repository = LegalRepository()
    # Action
    repository.check_legal_duplicate_in_update(
        legals, new_buyer_id=buyer_id, new_legal_id=new_legal_id
    )


@async_mark
async def test_update_legal():
    # Setup
    update_legal_of_user = mock_manager.mocks[
        data_layer_mocks
    ].MongoUserDataLayer.update_legal_of_user = AsyncMock()
    # Action
    repository = LegalRepository()
    await repository.update_legal(ObjectId(), dict())
    assert update_legal_of_user.called


@async_mark
async def test_delete_legal():
    # Setup
    delete_legal_of_user = mock_manager.mocks[
        data_layer_mocks
    ].MongoUserDataLayer.delete_legal_of_user = AsyncMock()
    # Action
    repository = LegalRepository()
    await repository.delete_legal(ObjectId(), ObjectId())
    assert delete_legal_of_user.called


def test_check_is_used_legal_for_delete_is_used_True():
    # Setup
    new_legal_id = ObjectId()
    legals: List[dict] = [dict(_id=new_legal_id, is_used=True)]
    repository = LegalRepository()
    # Action
    with raises(HTTPException) as errors:
        repository.check_is_used_legal_for_delete(legals, legal_id=new_legal_id)
    assert errors.value.status_code == 400
    assert errors.value.detail == "Legal info in use"


def test_check_is_used_legal_for_delete_is_used_True():
    # Setup
    new_legal_id = ObjectId()
    legals: List[dict] = [dict(_id=ObjectId(), is_used=False)]
    repository = LegalRepository()
    # Action
    with raises(HTTPException) as errors:
        repository.check_is_used_legal_for_delete(legals, legal_id=new_legal_id)
    assert errors.value.status_code == 404
    assert errors.value.detail == "Legal info not found"
