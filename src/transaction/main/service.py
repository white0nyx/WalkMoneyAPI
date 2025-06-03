from typing import List

from src.account.main.exceptions import AccountNotFoundException, AccountPermissionDeniedException
from src.account.main.repository import AccountRepository
from src.category.main.exceptions import CategoryNotFoundException, CategoryPermissionDeniedException
from src.category.main.repository import CategoryRepository
from src.subcategory.main.exceptions import SubCategoryNotFoundException
from src.transaction.main.models import Transaction
from src.transaction.main.repository import TransactionRepository
from src.transaction.main.schemas import CreateTransactionSchema
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

    async def update_transaction(self, transaction_id: int, data: dict, user: User) -> Transaction:
        transaction = await self.get_transaction(transaction_id, user)
        transaction = await self.transaction_repository.update_one(transaction_id, data.model_dump(exclude_unset=True))
        return transaction

    async def delete_transaction(self, transaction_id: int, user: User) -> None:
        transaction = await self.get_transaction(transaction_id, user)
        await self.transaction_repository.delete_one(transaction_id)
        return {"message": "Transaction deleted successfully"}

