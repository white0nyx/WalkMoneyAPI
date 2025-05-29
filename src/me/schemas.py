from datetime import datetime
from typing import Any

from src.common.schemas import BaseSchema
from src.user.models import User


class GetMeSchema(BaseSchema):
    id: int
    email: str
    name: str | None
    created_at: datetime
    updated_at: datetime
    role: str

    @classmethod
    def model_validate(cls, obj: User, **kwargs) -> Any:
        obj_dict = obj.__dict__.copy()
        obj_dict["role"] = obj.role.name
        return super().model_validate(obj_dict)