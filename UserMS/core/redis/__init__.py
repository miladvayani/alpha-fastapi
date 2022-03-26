import aioredis


class Redis:
    connection = None
    pool = None

    def __init__(self, configs: dict) -> None:
        self.configs: dict = configs

    async def get_connection(self):
        if Redis.connection:
            return Redis.connection
        Redis.pool = aioredis.ConnectionPool.from_url(
            url=self.configs["WEB_REDIS_ADDRESS"] + "/" + str(self.configs["DB_INDEX"]),
            decode_responses=True,
        )
        Redis.connection = aioredis.Redis(connection_pool=Redis.pool)
        return Redis.connection

    async def op_on_db(self, op, key, value=None):
        if not Redis.connection:
            await self.get_connection()

        if op == "get":
            value = await Redis.connection.get(key)
            return value
        return value
