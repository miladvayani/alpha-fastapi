from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticClient
from motor.core import AgnosticDatabase


class Mongo:
    client: AgnosticClient = None
    db: AgnosticDatabase = None

    def __init__(self, configs: dict) -> None:
        """Mongo driver manager

        Args:
            configs (dict): mongo configs for creating connection and database
            name.
        """
        self.configs: dict = configs

    async def create_connection(self) -> AsyncIOMotorClient:
        if not Mongo.client:
            Mongo.client = AsyncIOMotorClient(self.configs["CONNECTION_STRING"])
            Mongo.db = Mongo.client[self.configs["MONGO_DB"]]
