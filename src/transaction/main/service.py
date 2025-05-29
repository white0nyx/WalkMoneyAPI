from typing import List

from src.transaction.main.models import Transaction
from src.transaction.main.repository import TransactionRepository
from src.user.models import User


class TransactionService:

    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository

    async def create_transaction(self, data: dict, user: User) -> Transaction:
        pass

    async def get_transaction(self, transaction_id: int, user: User) -> Transaction:
        pass

    async def get_all_transactions(self, user: User) -> List[Transaction]:
        pass

    async def update_transaction(self, transaction_id: int, data: dict, user: User) -> Transaction:
        pass

    async def delete_transaction(self, transaction_id: int, user: User) -> None:
        pass
