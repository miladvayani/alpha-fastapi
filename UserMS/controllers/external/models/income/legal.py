from fastapi import HTTPException
import requests
from pydantic import BaseModel, Field, validator
from UserMS import Application as root
from UserMS.core.hydantic.fields import ObjectId
from UserMS.core.hydantic.fields import EconomicalCode
from UserMS.core.hydantic.fields import Numeric
from UserMS.core.hydantic.fields import PhoneNumber
from UserMS.core.hydantic.fields import NationalId
from UserMS.core.i18n import _


class AddLegalIncomeModel(BaseModel):
    organization_name: str = Field(..., max_length=300)
    economical_code: EconomicalCode = Field(None, max_length=16)
    buyer_id: NationalId = Field(..., max_length=11)
    registration_number: str = Field(..., max_length=10)
    city_name: str = Field(..., max_length=150)
    province_name: str = Field(..., max_length=150)
    phone: PhoneNumber = Field(None, max_length=10)
    buyerpostalcode: Numeric = Field(None, max_length=10)
    address: str = Field(..., max_length=200)

    @validator("province_name")
    def validate(cls, v, values, **kwargs):
        validate_province_city(province=v, city=values["city_name"])
        return v


class UpdateLegalIncomeModel(BaseModel):
    id: ObjectId = Field(None, alias="_id")
    organization_name: str = Field(None, max_length=300)
    economical_code: EconomicalCode = Field(None, max_length=16)
    buyer_id: NationalId = Field(None, max_length=11)
    registration_number: str = Field(None, max_length=10)
    city_name: str = Field(None, max_length=150)
    province_name: str = Field(None, max_length=150)
    phone: PhoneNumber = Field(None, max_length=10)
    buyerpostalcode: Numeric = Field(None, max_length=10)
    address: str = Field(None, max_length=200)

    @validator("province_name")
    def check_province(cls, v: str, values: dict):
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
