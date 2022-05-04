import aioredis
from typing import Union, Any
from .base import BaseRedis


class Str(BaseRedis):
    """Redis string class."""
    @classmethod
    async def set(cls,key: Union[str, int], value: Union[str, int], ttl: int=None,connection:aioredis.Redis=None) -> None:
        """Set key to value in Redis database.

        Args:
            key (Union[str, int]): key to set.
            value (Union[str, int]): value to set.
            ttl (int, optional): time to live. Defaults to None.
            connection (aioredis.Redis, optional): Redis Connectio. Defaults to None.
        """
        connection=connection if connection else cls.connection
        ttl=ttl if ttl else cls.ttl
        await connection.set(name=key,value= value,ex= ttl)

    @classmethod
    async def get(cls,key: Union[str, int],connection:aioredis.Redis=None) -> str:
        """Get value from Redis database.
        
        Args:
            key (Union[str, int]): key to get.
            connection (aioredis.Redis, optional): Redis Connectio. Defaults to None.

        Returns:
            str: value from Redis database.

        """
        connection=connection if connection else cls.connection
        return await connection.get(name=key)
        


class Set(BaseRedis):
    """Set Redis class."""
    @classmethod
    async def set(cls,key: Union[str, int], value: set, ttl: int=None,connection:aioredis.Redis=None) -> None:
        """Set value to Redis set.

        Args:
            key (Union[str, int]): key to set.
            value (set): value to set.
            ttl (int, optional): time to live. Defaults to None.
            connection (aioredis.Redis, optional): Redis Connection. Defaults to None.
        """
        connection=connection if connection else cls.connection
        ttl=ttl if ttl else cls.ttl
        await connection.sadd(key,*value)
        if ttl:
            await connection.expire(name=key,time= ttl)

    @classmethod
    async def get(cls,key: Union[str, int],connection:aioredis.Redis=None) -> set:
        """Get value from Redis set.
        
        Args:
            key (Union[str, int]): key to get.
            connection (aioredis.Redis, optional): Redis Connection. Defaults to None.

        Returns:
            set: value from Redis set.
        """
        connection=connection if connection else cls.connection
        return await connection.smembers(name=key)

    @classmethod
    async def sismember(cls,key: Union[str, int], value: Any) -> bool:
        """Check if value is in Redis set.
        
        Args:
            key (Union[str, int]): key to check.
            value (Any): value to check.

        Returns:
            bool: True if value is in Redis set.
        """
        return await cls.connection.sismember(name=key,value=value)
       


class List(BaseRedis):
    """Redis List class."""
    @classmethod
    async def set(cls,key: Union[str, int], value: list, ttl:int=None,connection:aioredis.Redis=None) -> None:
        """Set list to Redis database.

        Args:
            key (Union[str, int]): key to set.
            value (list): value to set.
            ttl (int, optional): time to live. Defaults to None.
            connection (aioredis.Redis, optional): Redis connection. Defaults to None.
        """
        connection=connection if connection else cls.connection
        ttl=ttl if ttl else cls.ttl
        await connection.lpush(key, *value)
        
        if ttl:
            await connection.expire(name=key,time= ttl)
        print(key)
        print(value)

    @classmethod
    async def get(cls,key: Union[str, int],connection:aioredis.Redis=None) -> list:
        """Get list from Redis database.

        Args:
            key (Union[str, int]): key to get.
            connection (aioredis.Redis, optional): Redis connection. Defaults to None.

        Returns:
            list: list from Redis database.
        """
        connection=connection if connection else cls.connection
        return await connection.lrange(name=key,start= 0,end= -1)


class Hash(BaseRedis):
    """For hash data type."""
    @classmethod
    async def set(cls,key: Union[str, int], value: dict, ttl:int=None,connection:aioredis.Redis=None) -> None:
        """save value to Redis hash.

        Args:
            key (Union[str, int]): key in redis hash.
            value (dict): value of key in redis.
            ttl (int): time to live.
            connection (aioredis.Redis, optional): Redis connection. Defaults to None.
        """
        connection=connection if connection else cls.connection
        ttl=ttl if ttl else cls.ttl
        await connection.hmset(name=key, mapping=value)
        if ttl:
            await connection.expire(name=key,time= ttl)

    @classmethod
    async def get(cls,key: Union[str, int],connection:aioredis.Redis=None) -> dict:
        """Get value from Redis hash.

        Args:
            key (Union[str, int]): key in redis hash.
            connection (aioredis.Redis, optional): Redis connection. Defaults to None.

        Returns:
            dict: value of key in redis.
        """
        connection=connection if connection else cls.connection
        return await connection.hgetall(name=key)

    


class Redis(BaseRedis):
    """This class used for manage all redis data types."""
    types = dict(
        string=Str,
        str=Str,
        list=List,
        hash=Hash,
        int=Str,
        tuple=List,
        dict=Hash,
        set=Set,
    )

    async def set(self, key: Union[str, int], value: Any,ttl:int=None) -> None:
        """Set value to Redis database.

        Args:
            key (Union[str,int]):  key to set value to.
            value (Any): value to set.
            ttl (int): expire time in seconds.
        """
        try:
            ttl=ttl if ttl else self.ttl
            await Redis.types[str(type(value).__name__)].set(key=key,value= value,ttl=ttl,connection=Redis.connection)
        except:
            raise Exception("Type not supported")


    async def get(self, key: Union[str, int]) -> Any:
        """Get value from Redis database.

        Args:
            key (Union[str,int]): key to get value from.

        Returns:
            Any: value from Redis database.
        """
        try:
            return await Redis.types[await Redis.connection.type(key)].get(key=key,connection=Redis.connection)
        except:
            return None


    

    
