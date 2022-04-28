from random import randint
from typing import Union
import decimal
import re
from datetime import datetime
from typing import Any, Dict, Pattern, cast, List, Type, Callable

import bson
import bson.binary
import bson.decimal128
import bson.int64
import bson.regex
from pydantic.fields import ModelField
from pydantic.datetime_parse import parse_datetime
from pydantic.main import BaseModel
from pydantic.validators import (
    bytes_validator,
    decimal_validator,
    int_validator,
    pattern_validator,
)
from pydantic.types import _registered
from .validators import _
from .validators import validate_economical_code
from .validators import validate_mobile_number
from .validators import validate_national_code
from .validators import validate_national_id
from .validators import validate_phone_number
from .base import BaseConstrainedStr, BaseMultiFieldSelector


class ObjectId(bson.ObjectId):
    @classmethod
    def __get_validators__(cls):  # type: ignore
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema: Dict) -> None:
        field_schema.update(
            examples=["5f85f36d6dfecacc68428a46", "ffffffffffffffffffffffff"],
            example="5f85f36d6dfecacc68428a46",
            type="string",
        )

    @classmethod
    def validate(cls, v: Any) -> bson.ObjectId:
        if isinstance(v, (bson.ObjectId, cls)):
            return str(v)
        if isinstance(v, str) and bson.ObjectId.is_valid(v):
            return bson.ObjectId(v)
        raise TypeError(_("invalid ObjectId specified"))


class Int64(bson.int64.Int64):
    @classmethod
    def __get_validators__(cls):  # type: ignore
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema: Dict) -> None:
        field_schema.update(examples=[2147483649], type="number")

    @classmethod
    def validate(cls, v: Any) -> bson.int64.Int64:
        if isinstance(v, bson.int64.Int64):
            return v
        a = int_validator(v)
        return bson.int64.Int64(a)


Long = Int64


class Decimal128(bson.decimal128.Decimal128):
    @classmethod
    def __get_validators__(cls):  # type: ignore
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema: Dict) -> None:
        field_schema.update(examples=[214.7483649], example=214.7483649, type="number")

    @classmethod
    def validate(cls, v: Any) -> bson.decimal128.Decimal128:
        if isinstance(v, bson.decimal128.Decimal128):
            return v
        a = decimal_validator(v)
        return bson.decimal128.Decimal128(a)


class Binary(bson.binary.Binary):
    @classmethod
    def __get_validators__(cls):  # type: ignore
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema: Dict) -> None:
        field_schema.update(type="string", format="binary")

    @classmethod
    def validate(cls, v: Any) -> bson.binary.Binary:
        if isinstance(v, bson.binary.Binary):
            return v
        a = bytes_validator(v)
        return bson.binary.Binary(a)


class Regex(bson.regex.Regex):
    @classmethod
    def __get_validators__(cls):  # type: ignore
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema: Dict) -> None:
        field_schema.update(
            examples=[r"^Foo"], example=r"^Foo", type="string", format="binary"
        )

    @classmethod
    def validate(cls, v: Any) -> bson.regex.Regex:
        if isinstance(v, bson.regex.Regex):
            return v
        a = pattern_validator(v)
        return bson.regex.Regex(a.pattern)


class StrField:
    def __new__(
        cls,
        *,
        empty: bool = True,
        numeric: bool = True,
        alphabetic: bool = True,
        strip_whitespace: bool = True,
        examples: List[str] = [],
        example: str = None,
        to_lower: bool = False,
        strict: bool = True,
        min_length: int = None,
        max_length: int = None,
        curtail_length: int = None,
        validator: Callable = None,
        exclude: bool = False,
        regex: str = None,
    ) -> Type[str]:
        namespace = dict(
            empty=empty,
            numeric=numeric,
            alphabetic=alphabetic,
            strip_whitespace=strip_whitespace,
            to_lower=to_lower,
            strict=strict,
            example=example,
            examples=examples,
            min_length=min_length,
            max_length=max_length,
            curtail_length=curtail_length,
            validator=validator,
            exclude=exclude,
            regex=regex and re.compile(regex),
        )
        return _registered(
            type(
                "ConstrainedStrValue",
                (BaseConstrainedStr,),
                namespace,
            )
        )


class _Pattern:
    @classmethod
    def __get_validators__(cls):  # type: ignore
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> Pattern:
        if isinstance(v, Pattern):
            return v
        elif isinstance(v, bson.regex.Regex):
            return re.compile(v.pattern, flags=v.flags)

        a = pattern_validator(v)
        return a


class _datetime(datetime):
    @classmethod
    def __get_validators__(cls):  # type: ignore
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> datetime:
        if isinstance(v, datetime):
            d = v
        else:
            d = parse_datetime(v)
        # MongoDB does not store timezone info
        # https://docs.python.org/3/library/datetime.html#determining-if-an-object-is-aware-or-naive
        if d.tzinfo is not None and d.tzinfo.utcoffset(d) is not None:
            raise ValueError(_("datetime objects must be naive (no timezone info)"))
        # Truncate microseconds to milliseconds to comply with Mongo behavior
        microsecs = d.microsecond - d.microsecond % 1000
        return d.replace(microsecond=microsecs)

    @classmethod
    def __modify_schema__(cls, field_schema: Dict) -> None:
        field_schema.update(example=datetime.utcnow().isoformat())


class _decimalDecimal(decimal.Decimal):
    """This specific BSON substitution field helps to handle the support of standard
    python Decimal objects

    https://api.mongodb.com/python/current/faq.html?highlight=decimal#how-can-i-store-decimal-decimal-instances
    """

    @classmethod
    def __get_validators__(cls):  # type: ignore
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> decimal.Decimal:
        if isinstance(v, decimal.Decimal):
            return v
        elif isinstance(v, bson.decimal128.Decimal128):
            return cast(decimal.Decimal, v.to_decimal())

        a = decimal_validator(v)
        return a

    @classmethod
    def __bson__(cls, v: Any) -> bson.decimal128.Decimal128:
        return bson.decimal128.Decimal128(v)


BSON_TYPES_ENCODERS = {
    bson.ObjectId: str,
    bson.decimal128.Decimal128: lambda x: x.to_decimal(),  # Convert to regular decimal
    bson.regex.Regex: lambda x: x.pattern,  # TODO: document no serialization of flags
}


class BaseBSONModel(BaseModel):
    """Equivalent of `pydantic.BaseModel` supporting BSON types encoding.

    If you want to apply other custom JSON encoders, you'll need to use
    [BSON_TYPES_ENCODERS][odmantic.bson.BSON_TYPES_ENCODERS] directly.
    """

    class Config:
        json_encoders = BSON_TYPES_ENCODERS


_BSON_SUBSTITUTED_FIELDS = {
    bson.ObjectId: ObjectId,
    bson.int64.Int64: Int64,
    bson.decimal128.Decimal128: Decimal128,
    bson.binary.Binary: Binary,
    bson.regex.Regex: Regex,
    Pattern: _Pattern,
    decimal.Decimal: _decimalDecimal,
    datetime: _datetime,
}


PostalCode = StrField(
    alphabetic=False,
    min_length=10,
    max_length=10,
    example="1543235643",
)

PhoneField = StrField(
    max_length=10,
    min_length=3,
    examples=["4130293356", "4124432345"],
    example="4124432345",
    alphabetic=False,
    validator=validate_phone_number,
)

MobileField = StrField(
    max_length=10,
    min_length=10,
    examples=["9144154202", "9055153323"],
    example="9144154202",
    alphabetic=False,
    validator=validate_mobile_number,
)

NationalId = StrField(
    max_length=11,
    min_length=11,
    examples=["10220058054", "fffffffffff"],
    example="10220058054",
    validator=validate_national_id,
)

NationalCode = StrField(
    max_length=10,
    min_length=10,
    examples=["1362643254", "ffffffffff"],
    example="1362643254",
    validator=validate_national_code,
)

EconomicalCode = StrField(
    max_length=14,
    min_length=14,
    examples=["411000000000", "4110000000000000"],
    example="411000000000",
    validator=validate_economical_code,
)


class MultiNationlSelector(BaseMultiFieldSelector):
    @classmethod
    def selector(
        cls, fields: List[BaseConstrainedStr]
    ) -> Union[NationalId, NationalCode]:
        examples: List[str] = []
        validators: List[Callable] = []
        for field in fields:
            examples.extend(field.examples)
            validators.append(field.validator)
        return StrField(
            examples=examples,
            example=examples[randint(0, len(examples)) - 1],
            max_length=fields[-1].max_length,
            min_length=fields[0].min_length,
            validator=cls.select_national,
        )

    def select_national(value: str, field: ModelField = None) -> str:
        lv: int = len(value)
        if lv == 10:
            return validate_national_code(value)
        elif lv == 11:
            return validate_national_id(value)


NationlCodeId = MultiNationlSelector(NationalCode, NationalId)


RegistrationNumber = StrField(
    alphabetic=False,
    example="12345",
    examples=["43211", "11111"],
    max_length=5,
    min_length=5,
)
