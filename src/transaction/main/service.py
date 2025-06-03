import calendar
from collections import defaultdict
from datetime import datetime, timezone
from datetime import timedelta
from typing import List

from src.account.main.exceptions import AccountNotFoundException, AccountPermissionDeniedException
from src.account.main.repository import AccountRepository
from src.category.main.exceptions import CategoryNotFoundException, CategoryPermissionDeniedException
from src.category.main.repository import CategoryRepository
from src.subcategory.main.exceptions import SubCategoryNotFoundException
from src.transaction.main.exceptions import TransactionNotFoundException, TransactionPermissionDeniedException
from src.transaction.main.models import Transaction
from src.transaction.main.repository import TransactionRepository
from src.transaction.main.schemas import CreateTransactionSchema, UpdateTransactionSchema, GetStatisticByCategoriesParams, StatisticPeriodEnum
from src.transaction.main.schemas import GetTransactionParamsSchema
from src.user.models import User


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
        now = datetime.now(timezone.utc)
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

    @staticmethod
    def generate_dates_list(start: datetime, end: datetime, period: StatisticPeriodEnum) -> List[str]:
        dates = []
        if period in (StatisticPeriodEnum.year, StatisticPeriodEnum.all):
            # Генерируем по месяцам
            current = datetime(start.year, start.month, 1, tzinfo=start.tzinfo)
            last_month = datetime(end.year, end.month, 1, tzinfo=end.tzinfo)
            while current <= last_month:
                dates.append(current.strftime("%Y-%m"))
                year = current.year + (current.month // 12)
                month = (current.month % 12) + 1
                current = current.replace(year=year, month=month)
        else:
            # Генерируем по дням
            current = start
            while current.date() <= end.date():
                dates.append(current.date().isoformat())
                current += timedelta(days=1)
        return dates

    async def get_time_statistics(self, params: GetStatisticByCategoriesParams, user_id: int) -> dict:
        # Получаем период
        start_period, end_period = self.calculate_period_dates(params.period)
        start_period = await self.transaction_repository.get_first_transaction_date(user_id) if not start_period else start_period
        end_period = datetime.now(timezone.utc) if not end_period else end_period

        # Получаем все категории
        categories = await self.category_repository.find_all_by_user_id_without_pagination(user_id, params.type)

        # Генерируем список ключей по датам или месяцам/неделям
        date_keys = self.generate_dates_list(start_period, end_period, params.period)

        # Получаем из репозитория агрегированную статистику:
        rows = await self.transaction_repository.get_period_category_statistics(
            user_id=user_id,
            start_period=start_period,
            end_period=end_period,
            transaction_type=params.type,
            period=params.period
        )
        # rows: List of tuples (category_id, total_amount, category_name, period_dt)

        # Формируем словарь для быстрого доступа к суммам по (date_key, category_id)
        sums_map = {}
        for category_id, total_amount, category_name, period_dt in rows:
            if period_dt is None:
                period_dt = start_period or datetime.now(timezone.utc)
            if params.period in (StatisticPeriodEnum.year, StatisticPeriodEnum.all):
                key = period_dt.strftime("%Y-%m")
            else:
                key = period_dt.date().isoformat()
            sums_map[(key, category_id)] = float(total_amount)

        # Строим итоговую структуру
        data = {}
        total_amount_sum = 0

        for date_key in date_keys:
            day_list = []
            for category in categories:
                amount = sums_map.get((date_key, category.id), 0.0)
                day_list.append({
                    "category_id": category.id,
                    "category_name": category.name,
                    "amount": amount
                })
                total_amount_sum += amount
            data[date_key] = day_list

        # Считаем дни/недели/месяцы для средних
        days = (end_period - start_period).days + 1 if start_period and end_period else 1
        weeks = days / 7 if days > 7 else 1
        months = (end_period.year - start_period.year) * 12 + (end_period.month - start_period.month) + 1 if start_period and end_period else 1

        average_per_day = total_amount_sum / days if days > 0 else 0
        average_per_week = total_amount_sum / weeks if weeks > 0 else 0
        average_per_month = total_amount_sum / months if months > 0 else 0

        return {
            "data": data,
            "total_amount": total_amount_sum,
            "average_per_day": average_per_day,
            "average_per_week": average_per_week,
            "average_per_month": average_per_month,
            "period": params.period.value,
            "days_in_period": days,
            "weeks_in_period": weeks,
            "months_in_period": months
        }

    async def get_category_statistics(self, params: GetStatisticByCategoriesParams, user_id: int) -> dict:
        start_period, end_period = self.calculate_period_dates(params.period)
        start_period = await self.transaction_repository.get_first_transaction_date(user_id) if not start_period else start_period
        end_period = datetime.now() if not end_period else end_period

        rows = await self.transaction_repository.get_total_category_statistics(
            user_id=user_id,
            start_period=start_period,
            end_period=end_period,
            transaction_type=params.type
        )

        data = [
            {
                "category_id": category_id,
                "category_name": category_name,
                "amount": float(total_amount)
            }
            for category_id, total_amount, category_name in rows
        ]

        return {"data": data}

