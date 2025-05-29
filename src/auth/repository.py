import secrets

from datetime import datetime, UTC
from sqlalchemy import select, update
from sqlalchemy.orm import subqueryload

from src.common.database import async_session_maker
from src.common.repository import SQLAlchemyRepository
from src.user.models import User
from src.role.models import Role


class AuthRepository(SQLAlchemyRepository):
    model: type[User] = User

    async def find_by_email(self, email: str):
        async with async_session_maker() as session:
            stmt = select(self.model).options(subqueryload(self.model.role)).where(self.model.email == email)
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

    async def get_default_role_id(self):
        async with async_session_maker() as session:
            stmt = select(Role.id).where(Role.name == "user")
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

    async def create_password_reset_token(self, email: str):
        async with async_session_maker() as session:
            stmt = (
                update(self.model)
                .where(self.model.email == email)
                .values(reset_password_token=secrets.token_hex(16), reset_password_sent_at=datetime.now(UTC))
                .returning(self.model)
            )
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def set_new_password(self, user_data: dict):
        async with async_session_maker() as session:
            stmt = (
                update(self.model)
                .where(self.model.reset_password_token == user_data["reset_password_token"])
                .values(reset_password_token=None, password=user_data["password"], updated_at=datetime.now(UTC))
                .returning(self.model)
            )
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def record_statistics(self, user_id: int, client_ip: str):
        async with async_session_maker() as session:
            stmt = (
                update(self.model)
                .where(self.model.id == user_id)
                .values(
                    last_sign_in_at=datetime.now(UTC),
                    last_sign_in_ip=client_ip,
                    sign_in_count=self.model.sign_in_count + 1,
                )
                .returning(self.model)
            )
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()
