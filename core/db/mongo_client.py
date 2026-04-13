from motor.motor_asyncio import AsyncIOMotorClient

class MongoClient:
    def __init__(self, uri="mongodb://admin:ptof123@localhost:27017"):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client.ptof_db
        self.iq_collection = self.db.iq_streams

    async def insert_iq(self, data):
        await self.iq_collection.insert_one(data)
