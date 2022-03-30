from json import JSONEncoder
from typing import Any
from jwt import decode
from jwt import encode
from jwt.exceptions import ExpiredSignatureError
from jwt.exceptions import DecodeError
from fastapi import HTTPException


class JWTManager:
    """
    `JWTManager is the base class of jwt.`
    """

    def __init__(
        self,
        algorithm: str = None,
        options: dict = None,
        verify: bool = None,
        key: str = "",
    ):
        """`JWTManager`

        Args:
            algorithm (str, optional): jwt algorithm. Defaults to None.
            options (dict, optional): jwt various options. Defaults to None.
            verify (bool, optional): flag for specifying to ensuring
            validation of income jwt tokens or not. Defaults to None.
            key (str, optional): secret key of jwt encoder/decoder. Defaults to "".
        """
        self.key: str = key
        self.algorithm: str = algorithm
        self.options: dict = options
        self.verify: bool = verify

    def decode(
        self,
        jwt: str,
        key: str = None,
        verify: bool = None,
        algorithm: str = None,
        options: dict = None,
        **kwargs: dict
    ) -> dict:
        """Decoding the income token.

        Args:
            jwt (str): captured jwt.
            key (str, optional): secret key. Defaults to None.
            verify (bool, optional): flag for specifying to ensuring
            validation of income jwt or not. Defaults to None.
            algorithm (str, optional): jwt algorithn. Defaults to None.
            options (dict, optional): jwt various options. Defaults to None.

        Raises:
            HTTPException: 401, Invalid Token.
            HTTPException: 401, Expired Token.

        Returns:
            dict: decoded token.
        """
        try:
            return decode(
                jwt=jwt,
                key=key if key else self.key,
                verify=verify if verify else self.verify,
                algorithms=algorithm if algorithm else self.algorithm,
                options=options if options else self.options,
                **kwargs
            )

        except DecodeError:
            raise HTTPException(401, "Invalid Token")

        except ExpiredSignatureError:
            raise HTTPException(401, "Expired Token")

    def encode(
        self,
        payload: Any,
        key: str = None,
        algorithm: str = None,
        headers: dict = None,
        json_encoder: JSONEncoder = None,
    ) -> str:
        """Encoding the income payload

        Args:
            payload (Any): jwt payload to get encode.
            key (str, optional): secret key. Defaults to None.
            algorithm (str, optional): jwt algorithm. Defaults to None.
            headers (dict, optional): jwt headers for some special validations. Defaults to None.
            json_encoder (JSONEncoder, optional): json encoder interface. Defaults to None.

        Returns:
            str: encoded token
        """
        return encode(
            payload=payload,
            key=key if key else self.key,
            algorithm=algorithm if algorithm else self.algorithm,
            headers=headers,
            json_encoder=json_encoder,
        )
