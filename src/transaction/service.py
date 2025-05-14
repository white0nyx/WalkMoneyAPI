from src.transaction.repository import TransactionRepository
from src.transaction.models import Transaction
from src.user.models import User
from fastapi import HTTPException
from datetime import datetime
from typing import List

class TransactionNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Transaction not found.")

class AccessForbiddenError(HTTPException):
    def __init__(self):
        super().__init__(status_code=403, detail="Access to this transaction is forbidden.")

class TransactionService:

    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository

    async def create_transaction(self, data: dict, user: User) -> Transaction:
        # Допустим, у нас есть проверка доступа для создания транзакции
        if not self.has_access(user):
            raise AccessForbiddenError()
        return await self.transaction_repository.add_one(data)

    async def get_transaction(self, transaction_id: int, user: User) -> Transaction:
        transaction = await self.transaction_repository.find_one(transaction_id)
        if not transaction:
            raise TransactionNotFoundError()
        if not self.has_access(user):
            raise AccessForbiddenError()
        return transaction

    async def get_all_transactions(self, user: User) -> List[Transaction]:
        if not self.has_access(user):
            raise AccessForbiddenError()
        return await self.transaction_repository.find_all()

    async def update_transaction(self, transaction_id: int, data: dict, user: User) -> Transaction:
        transaction = await self.transaction_repository.find_one(transaction_id)
        if not transaction:
            raise TransactionNotFoundError()
        if not self.has_access(user):
            raise AccessForbiddenError()
        return await self.transaction_repository.update_one(transaction_id, data)

    async def delete_transaction(self, transaction_id: int, user: User) -> None:
        transaction = await self.transaction_repository.find_one(transaction_id)
        if not transaction:
            raise TransactionNotFoundError()
        if not self.has_access(user):
            raise AccessForbiddenError()
        await self.transaction_repository.delete_one(transaction_id)

    async def find_transactions_by_account(self, account_id: int, user: User) -> List[Transaction]:
        if not self.has_access(user):
            raise AccessForbiddenError()
        return await self.transaction_repository.find_by_account_id(account_id)

    async def find_transactions_by_date_range(self, start_date: datetime, end_date: datetime, user: User) -> List[Transaction]:
        if not self.has_access(user):
            raise AccessForbiddenError()
        return await self.transaction_repository.find_by_date_range(start_date, end_date)

    def has_access(self, user: User) -> bool:
        # Логика проверки доступа, например, проверка роли
        return user.role.name == "admin"
