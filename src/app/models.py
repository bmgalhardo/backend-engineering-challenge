import datetime

from pydantic import BaseModel, field_validator


class TranslationDelivered(BaseModel):
    timestamp: datetime.datetime
    duration: int


class AggregatedOutput(BaseModel):
    date: datetime.datetime
    average_delivery_time: float

    @field_validator('average_delivery_time')
    def result_check(cls, v):
        return round(v, 1)
