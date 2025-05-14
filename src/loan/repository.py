from sqlalchemy import select

from src.common.database import async_session_maker
from src.loan.models import Loan
from src.common.repository import SQLAlchemyRepository

class LoanRepository(SQLAlchemyRepository):
    model: type[Loan] = Loan

    async def find_by_account_id(self, account_id: int):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.from_account_id == account_id)
            res = await session.execute(stmt)
            return res.scalars().all()

    async def find_active_loans(self):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.loan_status == "active")
            res = await session.execute(stmt)
            return res.scalars().all()
