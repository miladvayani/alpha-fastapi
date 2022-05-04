"""
For use cache first should create redis_connnection and redis from redis manager.
Then for every function that need cache should decorate function with
cache_manager.cache_function(expire_time:int,key_bilder:function)
key_bulder should return string that will be used as key for cache.
example:
    from core.redis_manager import Redis
    from core.cache_manager import CacheManager
    redis=Redis(address='redis://127.0.0.1:6379',password='',index=1,ttl=3600)
    # create redis conection
    await redis.get_connection()

    @cache_manager.cache_function(expire_time=3600,key_builder=key_bulider)

Key bulder example

from typing import Callable

from starlette.requests import Request


def key_builder(func: Callable, *args, **kwargs) -> str:
    '''Build a key for caching.

    Args:
        func (Callable): The function to be cached.

    Returns:
        str: The key for caching.
    '''
    key = func.__name__
    key_request:Request=list(filter(lambda request:isinstance(request[1],Request),kwargs.items()))[0][1]
    name=key_request.headers['name']
    
    return key+"_"+name

"""

from .cache import CacheManager