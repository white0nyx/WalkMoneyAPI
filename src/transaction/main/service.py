from collections import defaultdict
from datetime import datetime, timedelta
from typing import List
import calendar
from src.account.main.exceptions import AccountNotFoundException, AccountPermissionDeniedException
from src.account.main.repository import AccountRepository
from src.category.main.exceptions import CategoryNotFoundException, CategoryPermissionDeniedException
from src.category.main.repository import CategoryRepository
from src.subcategory.main.exceptions import SubCategoryNotFoundException
from src.transaction.main.models import Transaction
from src.transaction.main.repository import TransactionRepository
from src.transaction.main.schemas import CreateTransactionSchema, UpdateTransactionSchema, GetStatisticByCategoriesParams, StatisticPeriodEnum
from src.user.models import User
from src.transaction.main.exceptions import TransactionNotFoundException, TransactionPermissionDeniedException
from src.transaction.main.schemas import GetTransactionParamsSchema


class TransactionService:

    def __init__(
            self,
            transaction_repository: TransactionRepository,
            category_repository: CategoryRepository,
            account_repository: AccountRepository,
    ):
        self.transaction_repository = transaction_repository
        self.category_repository = category_repository
        self.account_repository = account_repository

    @staticmethod
    def calculate_period_dates(period: StatisticPeriodEnum) -> tuple[datetime | None, datetime | None]:
        now = datetime.now()
        if period == StatisticPeriodEnum.day:
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        elif period == StatisticPeriodEnum.week:
            start = now - timedelta(days=now.weekday())  # понедельник этой недели
            start = start.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=6, hours=23, minutes=59, seconds=59, microseconds=999999)
        elif period == StatisticPeriodEnum.month:
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            last_day = calendar.monthrange(now.year, now.month)[1]
            end = now.replace(day=last_day, hour=23, minute=59, second=59, microsecond=999999)
        elif period == StatisticPeriodEnum.year:
            start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            end = now.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
        elif period == StatisticPeriodEnum.all:
            start = None
            end = None
        else:
            start = None
            end = None
        return start, end

    async def get_period_category_statistics(self, params: GetStatisticByCategoriesParams, user_id: int) -> dict:
        start_period, end_period = self.calculate_period_dates(params.period)

        rows = await self.transaction_repository.get_period_category_statistics(
            user_id=user_id,
            start_period=start_period,
            end_period=end_period,
            transaction_type=params.type,
            period=params.period
        )

        data = defaultdict(list)
        total_amount_sum = 0  # Общая сумма за период

        for category_id, total_amount, category_name, period_dt in rows:
            if params.period in (StatisticPeriodEnum.year, StatisticPeriodEnum.all):
                key = period_dt.strftime("%Y-%m")
            elif params.period == StatisticPeriodEnum.week:
                key = period_dt.strftime("%Y-W%U")
            else:
                key = period_dt.date().isoformat()

            amount_float = float(total_amount)
            data[key].append({
                "category_id": category_id,
                "category_name": category_name,
                "amount": amount_float,
            })
            total_amount_sum += amount_float

        # Вычисляем длительность периода в днях (если даты есть)
        if start_period and end_period:
            days = (end_period - start_period).days + 1
        else:
            days = 1  # если дат нет, считаем 1, чтобы не делить на 0

        weeks = days / 7
        # Приблизительно считаем количество месяцев в периоде
        if start_period and end_period:
            months = (end_period.year - start_period.year) * 12 + (end_period.month - start_period.month) + 1
        else:
            months = 1

        average_per_day = total_amount_sum / days if days > 0 else 0
        average_per_week = total_amount_sum / weeks if weeks > 0 else 0
        average_per_month = total_amount_sum / months if months > 0 else 0

        return {
            "data": dict(data),
            "total_amount": total_amount_sum,
            "average_per_day": average_per_day,
            "average_per_week": average_per_week,
            "average_per_month": average_per_month,
            "period": params.period.value,
        }

    async def create_transaction(self, data: CreateTransactionSchema, user: User) -> Transaction:
        if data.category_id is not None:
            category = await self.category_repository.find_one(data.category_id)
            if not category:
                raise CategoryNotFoundException
            if category.user_id != user.id:
                raise CategoryPermissionDeniedException

            if data.subcategory_id is not None:
                subcategory = await self.category_repository.find_one(data.category_id)
                if not subcategory:
                    raise SubCategoryNotFoundException


        account = await self.account_repository.find_one(data.account_id)
        if not account:
            raise AccountNotFoundException
        if account.user_id != user.id:
            raise AccountPermissionDeniedException

        transaction = await self.transaction_repository.add_one(data.model_dump())
        return transaction

    async def get_transaction(self, transaction_id: int, user: User) -> Transaction:
        transaction = await self.transaction_repository.find_one(transaction_id)
        if not transaction:
            raise TransactionNotFoundException
        if transaction.account.user_id != user.id:
            raise TransactionPermissionDeniedException
        return transaction

    async def get_all_transactions(self, user_id: int, params: GetTransactionParamsSchema) -> List[Transaction]:
        transactions = await self.transaction_repository.find_all_by_user_id(user_id, params)
        return transactions

    async def update_transaction(self, transaction_id: int, data: UpdateTransactionSchema, user: User) -> Transaction:
        await self.get_transaction(transaction_id, user)
        transaction = await self.transaction_repository.update_one(transaction_id, data.model_dump(exclude_unset=True))
        return transaction

    async def delete_transaction(self, transaction_id: int, user: User) -> None:
        await self.get_transaction(transaction_id, user)
        await self.transaction_repository.delete_one(transaction_id)
        return {"message": "Transaction deleted successfully"}

