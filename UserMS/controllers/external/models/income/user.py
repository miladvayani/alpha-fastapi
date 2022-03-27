from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator

from UserMS.core.hydantic.fields import StrField
from UserMS.core.hydantic.fields import NationalCode
from UserMS.core.hydantic.fields import EconomicalCode


class UserUpdateIncomeModel(BaseModel):

    first_name: str = Field(..., max_length=70)
    last_name: str = Field(..., max_length=100)
    buyer_id: NationalCode = Field(..., max_length=11)
    economical_code: Optional[EconomicalCode] = None
    email: EmailStr
    birth_date: str
    job: str
    buyerpostalcode: StrField(numeric=True, alphabetic=False, max_length=10)
    address: str = Field(None, max_length=200)
