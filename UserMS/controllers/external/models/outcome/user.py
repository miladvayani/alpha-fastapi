from datetime import datetime
from typing import List
from pydantic import BaseModel
from UserMS.core.contrib import fields


class LegalInfoResponse(BaseModel):
    _id: fields.ObjectId = None
    organization_name: str = None
    economical_code: str = None
    buyer_id: str = None
    registration_number: str = None
    city_name: str = None
    province_name: str = None
    phone: str = None
    submit_date: datetime = None
    buyerpostalcode: str = None
    address: str = None
    is_used: bool = None


class UserResponse(BaseModel):
    first_name: str = None
    last_name: str = None
    buyer_id: str = None
    is_foreign_national: bool = None
    foreign_national_image: str = None
    mobile_number: str = None
    economical_code: str = None
    email: str = None
    birth_date: str = None
    job: str = None
    legal_info: List[LegalInfoResponse] = None
    buyerpostalcode: str = None
    address: str = None
    is_used: bool = None
