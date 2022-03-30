from pydantic import BaseModel, Field, validator
from UserMS import Application as root
from UserMS.core.contrib import fields
from UserMS.core.hydantic.validators import async_validate
from UserMS.core.i18n import _


class AddLegalIncomeModel(BaseModel):
    organization_name: fields.StrField(max_length=300)
    economical_code: fields.EconomicalCode
    buyer_id: fields.NationalId
    registration_number: fields.StrField(alphabetic=False, max_length=10)
    city_name: fields.StrField(
        numeric=False,
        max_length=150,
    )
    province_name: fields.StrField(numeric=False, max_length=150)
    phone: fields.PhoneField = None
    buyerpostalcode: fields.PostalCode = None
    address: fields.StrField(max_length=200)

    @validator("province_name")
    def check_province_city(cls, v, values, **kwargs):
        async_validate(v, validate_province_city, city_name=values["city_name"])
        return v


class UpdateLegalIncomeModel(BaseModel):
    id: fields.ObjectId = Field(None, alias="_id")
    organization_name: fields.StrField(max_length=300) = None
    economical_code: fields.EconomicalCode = None
    buyer_id: fields.NationalId = None
    registration_number: fields.StrField(alphabetic=False, max_length=10) = None
    city_name: fields.StrField(numeric=False, max_length=150) = None
    province_name: fields.StrField(numeric=False, max_length=150) = None
    phone: fields.PhoneField = None
    buyerpostalcode: fields.PostalCode = None
    address: fields.StrField(max_length=200)

    @validator("province_name")
    def check_province_city(cls, v: str, values: dict):
        if v and values.get("city_name"):
            async_validate(v, validate_province_city, values["city_name"])
            # validate_province_city(province=v, city=values["city_name"])
        return v


async def validate_province_city(province_name, city_name):
    result = list()
    pipeline = [
        {"$match": {"name": province_name}},
        {
            "$lookup": {
                "from": "city",
                "localField": "code",
                "foreignField": "province_code",
                "as": "city",
            }
        },
        {"$match": {"city": {"$elemMatch": {"name": city_name}}}},
    ]
    documents = root.client["SystemTablesDB"]["province"].aggregate(pipeline)
    async for doc in documents:
        result.append(doc)
    if not result:
        raise ValueError(
            {
                "city_name": _("Invalid city"),
                "province_name": _("Invalid province"),
            }
        )
