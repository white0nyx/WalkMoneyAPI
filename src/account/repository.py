from sqlalchemy import select
from src.common.database import async_session_maker
from src.account.models import Account
from src.common.repository import SQLAlchemyRepository

class AccountRepository(SQLAlchemyRepository):
    model: type[Account] = Account

    async def find_by_user_id(self, user_id: int):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.user_id == user_id)
            res = await session.execute(stmt)
            return res.scalars().all()

    async def find_archived_accounts(self):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.is_archived == True)
            res = await session.execute(stmt)
            return res.scalars().all()
