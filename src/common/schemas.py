import pytz

from datetime import datetime
from pydantic import BaseModel


def transform_to_moscow_datetime(dt: datetime) -> datetime:
    if dt is None:
        return None
    tz_moscow = pytz.timezone("Europe/Moscow")
    return dt.astimezone(tz=tz_moscow)


def exclude_unset(dictionary: dict) -> dict:
    data_dict = {k: v for k, v in dictionary.items() if v is not None}
    return data_dict


class BaseSchema(BaseModel):
    class Config:
        from_attributes = True
