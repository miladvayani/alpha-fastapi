from pydantic import BaseModel, Field
from UserMS.core.contrib import fields
from UserMS.core.i18n import _


class AddLegalIncomeModel(BaseModel):
    organization_name: fields.StrField(max_length=300)
    economical_code: fields.EconomicalCode
    buyer_id: fields.NationalId
    registration_number: fields.RegistrationNumber
    city_name: fields.StrField(
        numeric=False,
        max_length=150,
    )
    province_name: fields.StrField(numeric=False, max_length=150)
    phone: fields.PhoneField = None
    buyerpostalcode: fields.PostalCode = None
    address: fields.StrField(max_length=200)


class UpdateLegalIncomeModel(BaseModel):
    id: fields.ObjectId = Field(None, alias="_id")
    organization_name: fields.StrField(max_length=300) = None
    economical_code: fields.EconomicalCode = None
    buyer_id: fields.NationalId = None
    registration_number: fields.RegistrationNumber = None
    city_name: fields.StrField(numeric=False, max_length=150) = None
    province_name: fields.StrField(numeric=False, max_length=150) = None
    phone: fields.PhoneField = None
    buyerpostalcode: fields.PostalCode = None
    address: fields.StrField(max_length=200)
