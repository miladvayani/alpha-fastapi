from typing import Dict, Optional
from pydantic.main import ModelMetaclass
from pydantic import BaseModel
from pydantic.fields import ModelField


class AllOptionalMeta(ModelMetaclass):
    def __new__(self, name, bases, namespaces, **kwargs):
        annotations: Dict[str, ModelField] = namespaces.get("__annotations__", {})
        for base in bases:
            annotations.update(base.__annotations__)
        for field in annotations:
            if not field.startswith("__"):
                annotations[field] = Optional[annotations[field]]
        namespaces["__annotations__"] = annotations
        return super().__new__(self, name, bases, namespaces, **kwargs)


def create_unset_optional_model(t_model: BaseModel, data: dict) -> dict:
    """Set metaclass to pydantic models for ignore required fields

    Args:
        t_model (BaseModel): entity model
        data (dict): data for add to model

    Returns:
        dict: model data that sent as data (from model)
    """

    class AllOptional(t_model, metaclass=AllOptionalMeta):
        pass

    model: BaseModel = AllOptional(**data)
    return model.dict(exclude_unset=True)
