from enum import Enum

from pydantic import Field

from src.common.schemas import BaseSchema


class AccountTypeEnum(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"

class GetCategoryParamsSchema(BaseSchema):
    page: int | None = Field(default=1, ge=1)
    page_size: int | None = Field(default=10, ge=1)
    type: AccountTypeEnum

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
