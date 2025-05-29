from collections.abc import Sequence

from sqlalchemy import select
from src.common.database import async_session_maker
from src.account.main.models import Account
from src.common.repository import SQLAlchemyRepository

class AccountRepository(SQLAlchemyRepository):
    model: type[Account] = Account

    async def find_all_by_user_id(self, user_id: int) -> Sequence[Account]:
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.user_id == user_id, self.model.is_archived == False)
            res = await session.execute(stmt)
            return res.scalars().all()

    async def find_one(self, account_id: int) -> Account | None:
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.id == account_id)
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

