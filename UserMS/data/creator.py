from typing import Dict, Generic, Union
from typing import TypeVar

from .implements import DataLayerInterface
from .implements import MongoDataLayer

T = TypeVar("T", MongoDataLayer, object)


class DataLayer(Generic[T]):

    __layers: Dict[str, DataLayerInterface] = dict(mongo=MongoDataLayer)

    def __new__(cls, layer: str) -> T:
        _layer = layer.lower()
        if _layer in cls.__layers:
            return cls.__layers[_layer]()
        raise KeyError(f"{layer} has not register in data layers.")
