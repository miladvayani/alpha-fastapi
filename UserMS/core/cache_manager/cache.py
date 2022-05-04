from functools import wraps
from typing import Callable, Optional
from core.redis_manager.base import BaseRedis


class CacheManager:
    """This Class Used for caching."""
    redis: BaseRedis = None
    key_builder: Callable = None

    def __init__(self, redis: BaseRedis, key_builder: Callable) -> None:
        CacheManager.redis = redis
        CacheManager.key_builder = key_builder

    @classmethod
    def cache(cls, expire: Optional[int] = None):
        """Decorator for caching.

        Args:
            expire (Optional[int], optional): Time to live. Defaults to None.
        """
        def wrapper(func: Callable):
            @wraps(func)
            async def inner(*args, **kwargs):

                key = cls.key_builder(func, *args, **kwargs)

                value = await cls.redis.get(key)

                if not value:
                    value = await func(*args, **kwargs)
                    await cls.redis.set(key, value, expire)

                return value

            return inner

        return wrapper
