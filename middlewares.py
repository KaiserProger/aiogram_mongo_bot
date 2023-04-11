from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from db import MongoAdapter


class MongoMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, db: MongoAdapter):
        super().__init__()
        self.db = db

    async def pre_process(self, obj, data, *args):
        data["db"] = self.db

    async def post_process(self, obj, data, *args):
        del data["db"]
