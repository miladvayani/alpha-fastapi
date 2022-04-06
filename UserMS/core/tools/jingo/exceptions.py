

from .types import Any


class ConfigKeyType(Exception):

    def __init__(self, t: object) -> None:
        super().__init__(f"config key should be instance of str, but this is a {t} object")


class ConfigValueType(Exception):

    __types = [
        'str',
        'int',
        'tuple',
        'dict',
        'list',
        'None',
        'set',
        'float'
    ]

    def __init__(self, t: object) -> None:
        _registered: str = ", ".join(self.__types)
        super().__init__(f"config value should be insatnce of ({_registered}), but this is a {t} object")


class ProviderError(Exception):

    def __init__(self, valid, invalid) -> None:
        super().__init__(f"{invalid!r} does not exist in {valid!r}")