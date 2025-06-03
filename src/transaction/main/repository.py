from datetime import datetime

from sqlalchemy import select, Select, func
from sqlalchemy.orm import selectinload

from src.account.main.models import Account
from src.category.main.models import Category
from src.common.database import async_session_maker
from src.common.repository import SQLAlchemyRepository
from src.transaction.main.models import Transaction, TransactionType
from src.transaction.main.schemas import GetTransactionParamsSchema, StatisticPeriodEnum


class TransactionRepository(SQLAlchemyRepository):
    model: type[Transaction] = Transaction
    account_model: type[Account] = Account
    category_model: type[Category] = Category



    def _apply_filters(self, stmt: Select, params: GetTransactionParamsSchema):
        if params.start_period:
            stmt = stmt.where(self.model.created_at >= params.start_period)
        if params.end_period:
            stmt = stmt.where(self.model.created_at <= params.end_period)
        return stmt

    async def find_one(self, transaction_id: int):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.id == transaction_id)
            stmt = stmt.options(selectinload(self.model.account))
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

    async def find_all_by_user_id(self, user_id: int, params: GetTransactionParamsSchema):
        async with async_session_maker() as session:

            stmt = select(self.account_model.id).where(self.account_model.user_id == user_id)
            res = await session.execute(stmt)
            accounts_ids = res.scalars().all()
            stmt = self.apply_pagination(stmt, params)
            stmt = select(self.model).where(self.model.account_id.in_(accounts_ids))
            stmt = stmt.order_by(self.model.created_at.desc())
            res = await session.execute(stmt)
            return res.scalars().all()

    async def get_period_category_statistics(
        self,
        user_id: int,
        start_period: datetime | None,
        end_period: datetime | None,
        transaction_type: TransactionType | None,
        period: StatisticPeriodEnum,
    ):
        async with async_session_maker() as session:
            # Получаем id счетов пользователя
            stmt_accounts = select(self.account_model.id).where(self.account_model.user_id == user_id)
            result_accounts = await session.execute(stmt_accounts)
            accounts_ids = result_accounts.scalars().all()
            if not accounts_ids:
                return []

            # Выбираем группировку по месяцу для year и all, иначе по period
            if period in (StatisticPeriodEnum.year, StatisticPeriodEnum.all):
                group_period = func.date_trunc("month", self.model.created_at).label("period")
            else:
                group_period = func.date_trunc("day", self.model.created_at).label("period")

            stmt = (
                select(
                    self.model.category_id,
                    func.sum(self.model.amount).label("total_amount"),
                    Category.name.label("category_name"),
                    group_period,
                )
                .join(Category, Category.id == self.model.category_id)
                .where(self.model.account_id.in_(accounts_ids))
                .group_by(group_period, self.model.category_id, Category.name)
                .order_by(group_period)
            )

            if start_period is not None:
                stmt = stmt.where(self.model.created_at >= start_period)
            if end_period is not None:
                stmt = stmt.where(self.model.created_at <= end_period)
            if transaction_type is not None:
                stmt = stmt.where(self.model.transaction_type == transaction_type)

            result = await session.execute(stmt)
            return result.all()

    async def get_total_category_statistics(
            self,
            user_id: int,
            start_period: datetime | None,
            end_period: datetime | None,
            transaction_type: TransactionType | None,
    ):
        async with async_session_maker() as session:
            stmt_accounts = select(self.account_model.id).where(self.account_model.user_id == user_id)
            result_accounts = await session.execute(stmt_accounts)
            accounts_ids = result_accounts.scalars().all()
            if not accounts_ids:
                return []

            stmt = (
                select(
                    self.model.category_id,
                    func.sum(self.model.amount).label("total_amount"),
                    Category.name.label("category_name")
                )
                .join(Category, Category.id == self.model.category_id)
                .where(self.model.account_id.in_(accounts_ids))
                .group_by(self.model.category_id, Category.name)
                .order_by(self.model.category_id)
            )

            if start_period is not None:
                stmt = stmt.where(self.model.created_at >= start_period)
            if end_period is not None:
                stmt = stmt.where(self.model.created_at <= end_period)
            if transaction_type is not None:
                stmt = stmt.where(self.model.transaction_type == transaction_type)

            result = await session.execute(stmt)
            return result.all()

    async def get_first_transaction_date(self, user_id: int) -> datetime | None:
        async with async_session_maker() as session:
            # Получаем id счетов пользователя
            stmt_accounts = select(self.account_model.id).where(self.account_model.user_id == user_id)
            result_accounts = await session.execute(stmt_accounts)
            accounts_ids = result_accounts.scalars().all()
            if not accounts_ids:
                return None

            stmt_min_date = select(func.min(self.model.created_at)).where(self.model.account_id.in_(accounts_ids))
            result = await session.execute(stmt_min_date)
            min_date = result.scalar_one_or_none()
            return min_date