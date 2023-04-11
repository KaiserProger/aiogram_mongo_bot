from motor.motor_asyncio import AsyncIOMotorClient


class MongoAdapter:
    def __init__(self, db_host: str, db_user: str, db_password: str) -> None:
        self.client = AsyncIOMotorClient(f"mongodb://{db_user}:{db_password}@{db_host}", 27017)

    def on_shutdown(self):
        self.client.close()

    def get_collection(self, db_name: str, collection_name: str):
        return self.client.get_database(db_name).get_collection(collection_name)
