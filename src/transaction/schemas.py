from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TransactionBaseSchema(BaseModel):
    account_id: int
    category_id: int
    subcategory_id: int
    amount: float
    transaction_type: str
    transaction_date: Optional[datetime] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True

class CreateTransactionSchema(TransactionBaseSchema):
    pass

class UpdateTransactionSchema(TransactionBaseSchema):
    pass

class TransactionSchema(TransactionBaseSchema):
    id: int

    class Config:
        orm_mode = True
