from datetime import datetime
from typing import Optional

from src.common.schemas import BaseSchema


class GetTransactionSchema(BaseSchema):
    id: int
    account_id: int
    category_id: int
    subcategory_id: int
    amount: float
    transaction_type: str
    transaction_date: Optional[datetime] = None
    description: Optional[str] = None

class CreateTransactionSchema(BaseSchema):
    pass

class UpdateTransactionSchema(BaseSchema):
    pass
