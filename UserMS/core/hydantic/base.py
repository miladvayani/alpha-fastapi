from email.generator import Generator
from pydantic import BaseConfig, MissingError
from pydantic.types import _registered
from pydantic.types import ConstrainedStr
from pydantic.fields import ModelField
from pydantic.types import update_not_none
from .validators import (
    str_validator,
    constr_length_validator,
    constr_strip_whitespace,
    constr_lower,
    strict_str_validator,
)
from typing import Any, Callable, Dict, List
from .validators import async_validate


class BaseConstrainedStr(ConstrainedStr):

    empty: bool = False
    examples: List[str] = []
    example: str = None
    numeric: bool = True
    alphabetic: bool = False
    validator: Callable = None
    exclude: bool = False

    @classmethod
    def __get_validators__(cls) -> Generator:
        yield strict_str_validator if cls.strict else str_validator
        yield constr_strip_whitespace
        yield constr_lower
        yield cls.validate
        if not cls.empty:
            yield constr_length_validator

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        if cls.numeric and not cls.alphabetic:
            update_not_none(
                field_schema,
                maximum=cls.max_length,
                minimum=cls.min_length,
                pattern=cls.regex and cls.regex.pattern,
            )
        else:
            update_not_none(
                field_schema,
                minLength=cls.min_length,
                maxLength=cls.max_length,
                pattern=cls.regex and cls.regex.pattern,
            )
        if cls.examples:
            field_schema.update(examples=cls.examples)
        if cls.example:
            field_schema.update(example=cls.example)

    @classmethod
    def validate(cls, value: str, field: ModelField, config: BaseConfig) -> str:
        field.field_info.exclude = cls.exclude
        if cls.empty:
            if not value:
                if field.required:
                    raise MissingError
                return None
            else:
                constr_length_validator(value, field=field, config=config)
        result: str = super().validate(value)
        result = result.strip().replace("ي", "ی").replace("ك", "ک")
        if cls.numeric and not cls.alphabetic:
            if not result.isnumeric():
                raise ValueError("is not numeric")
        elif cls.alphabetic and not cls.numeric:
            if result.isspace() and not result.isalpha():
                raise ValueError("is not alphabetic")
        else:
            pass
        if cls.validator:
            return async_validate(result, cls.validator)
        return result
