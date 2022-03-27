from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, validator
from ..core.hydantic.fields import ObjectId
from ..core.hydantic.fields import EconomicalCode
from ..core.hydantic.fields import Numeric
from ..core.hydantic.fields import NationalCode
from ..core.hydantic.fields import NationalId
from ..core.hydantic.fields import PhoneNumber
from ..core.hydantic.fields import MobileNumber


class LegalInfo(BaseModel):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    organization_name: str = Field(..., max_length=300)
    economical_code: EconomicalCode = Field(None, max_length=16)
    buyer_id: NationalId = Field(..., max_length=11)
    registration_number: Numeric = Field(..., max_length=10)
    city_name: str = Field(..., max_length=150)
    province_name: str = Field(..., max_length=150)
    phone: PhoneNumber = Field(None, max_length=10)
    submit_date: datetime = Field(default_factory=datetime.utcnow)
    buyerpostalcode: Numeric = Field(None, max_length=10)
    address: str = Field(..., max_length=200)
    is_used: bool = Field(default=False)


class User(BaseModel):

    id: Optional[ObjectId] = Field(None, alias="_id")
    password: str = Field(None, max_length=100, exclude=True)
    first_name: str = Field(None, max_length=70)
    last_name: str = Field(None, max_length=100)
    buyer_id: NationalId = Field(None, max_length=11)
    is_foreign_national: bool = Field(default=False)
    foreign_national_image: str = Field(None, max_length=200)
    mobile_number: MobileNumber = Field(max_length=10)
    economical_code: EconomicalCode = Field(None, max_length=16)
    email: EmailStr = Field(None)
    birth_date: str = Field(None, max_length=10)
    job: str = Field(None, max_length=150)
    legal_info: List[LegalInfo]
    is_active: bool = Field(default=True)
    buyerpostalcode: Numeric = Field(None, max_length=10)
    address: str = Field(None, max_length=200)
    is_used: bool = Field(default=False)
    is_superuser: bool = Field(default=False)
    submit_date: datetime = Field(default_factory=datetime.utcnow, exclude=True)
