from enum import Enum

from src.common.schemas import BaseSchema

class AccountTypeEnum(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"

class GetCategoryBaseSchema(BaseSchema):
    id: int
    name: str
    icon_url: str | None = None


class CreateCategorySchema(BaseSchema):
    name: str
    icon_url: str | None = None
    type: AccountTypeEnum


class UpdateCategorySchema(CreateCategorySchema):
    pass
