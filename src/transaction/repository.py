from datetime import datetime

from sqlalchemy import select
from src.common.database import async_session_maker
from src.transaction.models import Transaction
from src.common.repository import SQLAlchemyRepository

class TransactionRepository(SQLAlchemyRepository):
    model: type[Transaction] = Transaction

    async def find_by_account_id(self, account_id: int):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.account_id == account_id)
            res = await session.execute(stmt)
            return res.scalars().all()

    async def find_by_date_range(self, start_date: datetime, end_date: datetime):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.transaction_date.between(start_date, end_date))
            res = await session.execute(stmt)
            return res.scalars().all()
