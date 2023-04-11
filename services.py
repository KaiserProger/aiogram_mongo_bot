from datetime import datetime, timedelta
from typing import TypedDict

from motor.motor_asyncio import AsyncIOMotorCollection

from dto import AggregationInputDto, AggregationOutputDto, DatetimeAggregationBuilder, GroupType


class AggregationOut(TypedDict):
    _id: None
    dataset: list[int]
    labels: list[datetime]


class PaymentAggregationService:

    def __init__(self, db_collection: AsyncIOMotorCollection) -> None:
        self.mongo = db_collection
        self.group_datetime_formats = {
            GroupType.MONTH: DatetimeAggregationBuilder().with_month(),
            GroupType.DAY: DatetimeAggregationBuilder().with_month().with_day(),
            GroupType.HOUR: DatetimeAggregationBuilder().with_month().with_day().with_hour(),
        }

    async def execute(
        self,
        dto: AggregationInputDto,
    ):
        dto_upper_range = dto.dt_to
        if dto.dt_to.hour == 0:
            dto_upper_range += timedelta(hours=1)
        pipeline = [{
            "$match": {
                "dt": {
                    "$gte": dto.dt_from,
                    "$lte": dto.dt_to,
                },
            },
        }, {
            "$densify": {
                "field": "dt",
                "range": {
                    "step": 1,
                    "unit": "hour",
                    "bounds": [dto.dt_from, dto_upper_range],
                },
            },
        }, {
            "$group": {
                "_id": {
                    "dt": self.group_datetime_formats[dto.group_type].build(),
                },
                "total": {"$sum": "$value"},
            },
        }, {
            "$project": {
                "_id": {
                    "$dateFromParts": {
                        "year": "$_id.dt.year",
                        "month": "$_id.dt.month",
                        "day": {"$ifNull": ["$_id.dt.day", 1]},
                        "hour": {"$ifNull": ["$_id.dt.hour", 0]}
                    }
                },
                "total": 1,
            }
        }, {
            "$sort": {"_id": 1},
        }, {
            "$group": {
                "_id": None,
                "dataset": {
                    "$push": "$total",
                },
                "labels": {
                    "$push": "$_id",
                }
            }
        }]
        _collection: AggregationOut = (await self.mongo.aggregate(pipeline).to_list(None))[0]  # type: ignore
        print(_collection)
        return AggregationOutputDto(
            dataset=_collection["dataset"],
            labels=_collection["labels"]
        )
