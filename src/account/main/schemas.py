from src.common.schemas import BaseSchema


class GetAccountSchema(BaseSchema):
    id: int
    user_id: int
    name: str
    balance: float
    type_id: int
    icon_url: str | None


class GetSelectedAccountSchema(BaseSchema):
    id: int
    name: str
    balance: float
    type_id: int
    icon_url: str | None = None
    currency_id: int | None = None
    is_archived: bool = False


class ResponseGetAccountsSchema(BaseSchema):
    accounts: list[GetAccountSchema]


class CreateAccountSchema(BaseSchema):
    name: str
    description: str
    balance: float = 0
    type_id: int
    currency_id: int
    icon_url: str | None = None


class UpdateAccountSchema(BaseSchema):
    name: str | None = None
    description: str | None = None
    balance: float | None = None
    type_id: int | None = None
    icon_url: str | None = None
    is_archived: bool | None = None
