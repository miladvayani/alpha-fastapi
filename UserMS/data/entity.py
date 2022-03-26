from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, validator
from ..core.hydantic.fields import ObjectId
from ..core.hydantic.validators import validate_economical_code
from ..core.hydantic.validators import validate_mobile_number
from ..core.hydantic.validators import validate_national_code
from ..core.hydantic.validators import validate_national_id
from ..core.hydantic.validators import validate_phone_number
from ..core.hydantic.validators import validate_code


class LegalInfo(BaseModel):
    id: Optional[ObjectId] = Field(None, default_factory=ObjectId, alias="_id")
    organization_name: str = Field(..., max_length=300)
    economical_code: str = Field(None, max_length=16)
    buyer_id: str = Field(..., max_length=11)
    registration_number: str = Field(..., max_length=10)
    city_name: str = Field(..., max_length=150)
    province_name: str = Field(..., max_length=150)
    phone: str = Field(None, max_length=10)
    submit_date: datetime = Field(default_factory=datetime.utcnow)
    buyerpostalcode: str = Field(None, max_length=10)
    address: str = Field(..., max_length=200)
    is_used: bool = Field(default=False)

    @validator("economical_code")
    def checK_economical_code(cls, v: str, values: dict, **kwargs: dict) -> str:
        if validate_economical_code(v):
            return v

    @validator("buyer_id")
    def check_buyer_id(cls, v: str, values: dict, **kwargs: dict) -> str:
        validate_national_id(v)
        return v

    @validator("phone")
    def check_phone(cls, v: str, values: dict, **kwargs: dict) -> str:
        validate_phone_number(v)
        return v

    @validator("buyerpostalcode")
    def check_buyerpostalcode(cls, v: str, values: dict, **kwargs: dict) -> str:
        validate_code(v, number_of_digits=10)
        return v


class User(BaseModel):

    id: Optional[ObjectId] = Field(None, alias=True)
    password: str = Field(None, max_length=100, exclude=True)
    first_name: str = Field(None, max_length=70)
    last_name: str = Field(None, max_length=100)
    buyer_id: str = Field(None, max_length=11)
    is_foreign_national: bool = Field(default=False)
    foreign_national_image: str = Field(None, max_length=200)
    mobile_number: str = Field(max_length=10)
    economical_code: str = Field(None, max_length=16)
    email: EmailStr = Field(None)
    birth_date: str = Field(None, max_length=10)
    job: str = Field(None, max_length=150)
    legal_info: List[LegalInfo]
    is_active: bool = Field(default=True)
    buyerpostalcode: str = Field(None, max_length=10)
    address: str = Field(None, max_length=200)
    is_used: bool = Field(default=False)
    is_superuser: bool = Field(default=False)
    submit_date: datetime = Field(default_factory=datetime.utcnow, exclude=True)

    @validator("buyer_id")
    def check_buyer_id(cls, v: str, values: dict, **kwargs: dict) -> str:
        validate_national_code(v)
        return v

    @validator("mobile_number")
    def check_mobile_number(cls, v: str, values: dict, **kwargs: dict) -> str:
        validate_mobile_number(v)
        return v

    @validator("economical_code")
    def checK_economical_code(cls, v: str, values: dict, **kwargs: dict) -> str:
        if validate_economical_code(v):
            return v

    @validator("buyerpostalcode")
    def check_buyerpostalcode(cls, v: str, values: dict, **kwargs: dict) -> str:
        validate_code(v, number_of_digits=10)
        return v
