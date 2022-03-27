from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator

from UserMS.core.hydantic.fields import NationalId, PostalCode
from UserMS.core.hydantic.fields import EconomicalCode


class UserUpdateIncomeModel(BaseModel):

    first_name: str = Field(..., max_length=70)
    last_name: str = Field(..., max_length=100)
    buyer_id: NationalId
    economical_code: EconomicalCode = None
    email: EmailStr
    birth_date: str
    job: str
    buyerpostalcode: PostalCode = None
    address: str = Field(None, max_length=200)
