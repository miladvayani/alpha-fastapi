from typing import Optional
from fastapi import HTTPException
import requests
from pydantic import BaseModel, Field, validator
from UserMS import Application as root
from UserMS.core.hydantic.fields import ObjectId
from UserMS.core.hydantic.fields import EconomicalCode
from UserMS.core.hydantic.fields import StrField
from UserMS.core.hydantic.fields import PostalCode
from UserMS.core.hydantic.fields import PhoneField
from UserMS.core.hydantic.fields import NationalId
from UserMS.core.hydantic.validators import async_validate
from UserMS.core.i18n import _


class AddLegalIncomeModel(BaseModel):
    organization_name: StrField(max_length=300)
    economical_code: EconomicalCode
    buyer_id: NationalId
    registration_number: StrField(alphabetic=False, max_length=10)
    city_name: StrField(
        numeric=False,
        max_length=150,
    )
    province_name: StrField(numeric=False, max_length=150)
    phone: PhoneField = None
    buyerpostalcode: PostalCode = None
    address: StrField(max_length=200)

    @validator("province_name")
    def check_province_city(cls, v, values, **kwargs):
        validate_province_city(province=v, city=values["city_name"])
        return v


class UpdateLegalIncomeModel(BaseModel):
    id: ObjectId = Field(None, alias="_id")
    organization_name: StrField(max_length=300) = None
    economical_code: EconomicalCode = None
    buyer_id: NationalId = None
    registration_number: StrField(alphabetic=False, max_length=10) = None
    city_name: StrField(numeric=False, max_length=150) = None
    province_name: StrField(numeric=False, max_length=150) = None
    phone: PhoneField = None
    buyerpostalcode: PostalCode = None
    address: StrField(max_length=200)

    @validator("province_name")
    def check_province_city(cls, v: str, values: dict):
        if v and values.get("city_name"):
            validate_province_city(province=v, city=values["city_name"])
        return v


def validate_province_city(province: str, city: str) -> None:
    if not city and not province:
        return True
    url = root.config["CONSTANTS_MS_URL"] + "validate_location/" + province + "/" + city
    resp = requests.get(url)
    if resp.status_code != 200:
        HTTPException(
            400,
            detail={
                "city_name": _("Invalid city"),
                "province_name": _("Invalid province"),
            },
        )
