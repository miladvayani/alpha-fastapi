from pydantic import BaseModel
from pydantic import EmailStr

from UserMS.core.contrib import fields


class UserUpdateIncomeModel(BaseModel):

    first_name: fields.StrField(max_length=70)
    last_name: fields.StrField(max_length=100)
    buyer_id: fields.NationalCode
    economical_code: fields.EconomicalCode = None
    email: EmailStr = None
    birth_date: fields.StrField()
    job: fields.StrField()
    buyerpostalcode: fields.PostalCode = None
    city_name: fields.StrField(
        numeric=False,
        max_length=150,
    )
    province_name: fields.StrField(numeric=False, max_length=150)
    address: fields.StrField(max_length=200)
