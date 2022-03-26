from typing import Callable
from fastapi import Query
from fastapi import Header
from fastapi import Body
from fastapi import Cookie
from fastapi import Path
from .base import JWTManager

locations: dict = {
    "header": Header(...),
    "cookie": Cookie(...),
    "body": Body(...),
    "path": Path(...),
    "query": Query(...),
}


def token_required(manager: JWTManager, location: str = "header") -> Callable:
    """token required decorator or dependency for fastapi

    Args:
        manager (JWTManager): jwt manager instance
        location (str, optional): distenation of lookuping the token from request
        . Defaults to "header".

    Returns:
        Callable: function to decode the income `token`.
    """

    async def wrapper(
        token: str = locations.get(location.lower(), Header(...)),
    ) -> dict:
        return manager.decode(jwt=token)

    return wrapper
