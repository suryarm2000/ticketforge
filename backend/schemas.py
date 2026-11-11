import datetime

from pydantic import BaseModel, Field

class EventCreate(BaseModel):
    title: str = Field(min_length=1)
    venue: str = Field(min_length=1)
    date: datetime.date
    price: float = Field(gt=0)