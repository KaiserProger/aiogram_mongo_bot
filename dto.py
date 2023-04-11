from pydantic import BaseModel, Field

from datetime import datetime
from enum import Enum


class GroupType(Enum):
    DAY = "day"
    MONTH = "month"
    HOUR = "hour"


class AggregationInputDto(BaseModel):
    dt_from: datetime
    dt_to: datetime = Field(alias="dt_upto")
    group_type: GroupType


class AggregationOutputDto(BaseModel):
    dataset: list[int]
    labels: list[datetime]


class DatetimeAggregationBuilder:
    def __init__(self) -> None:
        self.base = self.year

    @property
    def year(self):
        return {"year": {"$year": "$dt"}}

    def with_month(self):
        self.base["month"] = {"$month": "$dt"}
        return self

    def with_day(self):
        self.base["day"] = {"$dayOfMonth": "$dt"}
        return self

    def with_hour(self):
        self.base["hour"] = {"$hour": "$dt"}
        return self

    def build(self):
        return self.base
