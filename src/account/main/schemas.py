from src.common.schemas import BaseSchema


class CreateAccountSchema(BaseSchema):
    name: str
    balance: float = 0
    type_id: int
    currency_id: int
    icon_url: str | None = None
