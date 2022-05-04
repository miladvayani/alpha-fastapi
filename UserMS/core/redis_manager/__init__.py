"""For work with specific Redis data types (str, set, list, hash) should import related class from this module.
else for work with all data types should import Redis class from this module.If work with Redis class just can set,
get and delete and multiple get data from Redis.
create connection to Redis server and  use from methods.
example:
    from core.redis import Str, Set, List, Hash,Redis
    str_redis=Str(address='redis://127.0.0.1:6379',password='',index=1,ttl=3600)
"""
from .redis import Redis,Str,Set,List,Hash
