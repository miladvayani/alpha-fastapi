from pydantic import BaseModel
from pydantic import EmailStr

from UserMS.core.contrib import fields


class UserUpdateIncomeModel(BaseModel):

    first_name: fields.StrField(max_length=70)
    last_name: fields.StrField(max_length=100)
    buyer_id: fields.NationalCode
    economical_code: fields.EconomicalCode = None
    email: EmailStr
    birth_date: fields.StrField()
    job: fields.StrField() = None
    buyerpostalcode: fields.PostalCode = None
    address: fields.StrField(empty=True, max_length=200) = None
