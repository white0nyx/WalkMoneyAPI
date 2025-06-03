from datetime import datetime
from enum import Enum
from typing import Optional

from src.common.schemas import BaseSchema
from src.transaction.main.models import TransactionType


class GetTransactionParamsSchema(BaseSchema):
    start_period: datetime | None = None
    end_period: datetime | None = None
    type: Optional[TransactionType] = None


class StatisticPeriodEnum(str, Enum):
    day = "day"
    week = "week"
    month = "month"
    year = "year"
    all = "all"

class GetStatisticByCategoriesParams(BaseSchema):
    type: Optional[TransactionType] = None
    period: StatisticPeriodEnum = StatisticPeriodEnum.day

class GetTransactionSchema(BaseSchema):
    id: int
    account_id: int
    category_id: int | None
    subcategory_id: int | None
    amount: float
    transfer_to_account_id: int | None = None
    transaction_type: str
    created_at: datetime
    description: Optional[str] = None

class CreateTransactionSchema(BaseSchema):
    account_id: int
    category_id: int | None = None
    subcategory_id: int | None = None
    transfer_to_account_id: int | None = None
    amount: float = 0
    transaction_type: TransactionType
    created_at: datetime = datetime.now()
    description: str | None


class UpdateTransactionSchema(CreateTransactionSchema):
    pass

