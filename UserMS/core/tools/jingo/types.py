from types import LambdaType
from typing import Dict
from typing import Generic
from typing import List
from typing import Any
from typing import Optional
from typing import Sequence
from typing import Type
from typing import TypeVar
from typing import Union
from typing import overload
from typing import Callable
from types import ModuleType 
 
_S = TypeVar("_S")
_T = TypeVar("_T")
_KT = TypeVar("_KT")  # Key type.
_VT = TypeVar("_VT")  # Value type.
_T_co = TypeVar("_T_co", covariant=True)  # Any type covariant containers.
_V_co = TypeVar("_V_co", covariant=True)  # Any type covariant containers.
_KT_co = TypeVar("_KT_co", covariant=True)  # Key type covariant containers.
_VT_co = TypeVar("_VT_co", covariant=True)  # Value type covariant containers.
_T_contra = TypeVar("_T_contra", contravariant=True)  # Ditto contravariant.
_TC = TypeVar("_TC", bound=Type[object])