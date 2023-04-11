from aiogram import Dispatcher
from aiogram.types import Message
from orjson import loads, JSONDecodeError

from db import MongoAdapter
from dto import AggregationInputDto
from exceptions import invalid_json
from services import PaymentAggregationService


async def echo(message: Message):
    await message.reply("Hi!")


async def aggregation_handler(message: Message, db: MongoAdapter):
    objekt = loads(message.text)
    dto = AggregationInputDto(
        dt_from=objekt["dt_from"],
        dt_upto=objekt["dt_upto"],
        group_type=objekt["group_type"]
    )
    collection = db.get_collection("sampleDB", "sample_collection")
    output = await PaymentAggregationService(collection).execute(dto)
    await message.reply(output.json())


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(echo, commands=["start"])
    dp.register_message_handler(aggregation_handler)
    dp.register_errors_handler(invalid_json, exception=JSONDecodeError)
