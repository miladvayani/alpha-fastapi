from pydantic import BaseModel
from pydantic import EmailStr

from UserMS.core.hydantic.fields import NationalCode
from UserMS.core.hydantic.fields import PostalCode
from UserMS.core.hydantic.fields import StrField
from UserMS.core.hydantic.fields import EconomicalCode


class UserUpdateIncomeModel(BaseModel):

    first_name: StrField(max_length=70)
    last_name: StrField(max_length=100)
    buyer_id: NationalCode
    economical_code: EconomicalCode = None
    email: EmailStr
    birth_date: StrField()
    job: StrField() = None
    buyerpostalcode: PostalCode = None
    address: StrField(empty=True, max_length=200) = None
