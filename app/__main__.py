import asyncio
import logging

from aiogram import Bot, Dispatcher
from app.config import Config

from app.db import MongoAdapter
from app.handlers import register_handlers
from app.middlewares import MongoMiddleware


logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(level=logging.INFO)
    config = Config(_env_file=".env", _env_file_encoding="utf-8")  # type: ignore
    bot = Bot(token=config.token)
    dp = Dispatcher(bot)
    db = MongoAdapter(db_host=config.mongo_host, db_user=config.mongo_user, db_password=config.mongo_password)
    dp.middleware.setup(MongoMiddleware(db))
    register_handlers(dp)
    session = await bot.get_session()
    try:
        await dp.start_polling()
    finally:
        await session.close()   # type: ignore


def cli():
    """Wrapper for command line"""
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")


if __name__ == '__main__':
    cli()
