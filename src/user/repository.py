from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.common.database import async_session_maker
from src.common.repository import SQLAlchemyRepository
from src.user.models import User


class UserRepository(SQLAlchemyRepository):
    model: type[User] = User

    async def find_one(self, user_id: int) -> User | None:
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.id == user_id)
            stmt = stmt.options(selectinload(self.model.role))
            res = await session.execute(stmt)
            return res.scalar_one_or_none()