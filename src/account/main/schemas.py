from src.common.schemas import BaseSchema


class GetAccountSchema(BaseSchema):
    id: int
    user_id: int
    name: str
    balance: float
    type_id: int
    icon_url: str | None


class ResponseGetAccountsSchema(BaseSchema):
    accounts: list[GetAccountSchema]


class CreateAccountSchema(BaseSchema):
    name: str
    balance: float = 0
    type_id: int
    currency_id: int
    icon_url: str | None = None
