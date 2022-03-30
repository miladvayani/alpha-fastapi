from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from ..core.hydantic.fields import MobileField, ObjectId, PhoneField
from ..core.hydantic.fields import PostalCode
from ..core.hydantic.fields import StrField
from ..core.hydantic.fields import EconomicalCode
from ..core.hydantic.fields import NationalId


class LegalInfo(BaseModel):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    organization_name: StrField(max_length=300)
    economical_code: EconomicalCode
    buyer_id: NationalId
    registration_number: StrField(max_length=10)
    city_name: StrField(max_length=150)
    province_name: StrField(max_length=150)
    phone: PhoneField
    submit_date: datetime = Field(default_factory=datetime.utcnow)
    buyerpostalcode: PostalCode
    address: StrField(max_length=200)
    is_used: bool = Field(default=False)


class User(BaseModel):

    id: Optional[ObjectId] = Field(None, alias="_id")
    password: StrField(max_length=100) = None
    first_name: StrField(max_length=70) = None
    last_name: StrField(max_length=100) = None
    buyer_id: NationalId
    is_foreign_national: bool = Field(default=False)
    foreign_national_image: StrField(max_length=200) = None
    mobile_number: MobileField
    economical_code: EconomicalCode = None
    email: EmailStr = None
    birth_date: StrField(max_length=10) = None
    job: StrField(max_length=150) = None
    legal_info: List[LegalInfo] = []
    is_active: bool = Field(default=True)
    buyerpostalcode: PostalCode = None
    address: StrField(max_length=200) = None
    is_used: bool = Field(default=False)
    is_superuser: bool = Field(default=False)
    submit_date: datetime = Field(default_factory=datetime.utcnow, exclude=True)
