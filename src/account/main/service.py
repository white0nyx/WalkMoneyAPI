from src.account.main.exceptions import AccountNotFoundException, AccountPermissionDeniedException
from src.account.main.models import Account
from src.account.main.repository import AccountRepository
from src.account.main.schemas import CreateAccountSchema, UpdateAccountSchema
from src.user.models import User


class AccountService:

    def __init__(self, account_repository: AccountRepository):
        self.account_repository = account_repository

    async def create_account(self, account_data: CreateAccountSchema, user: User) -> Account:
        account_data = account_data.model_dump()
        account_data["user_id"] = user.id
        account = await self.account_repository.add_one(account_data)
        return account

    async def get_accounts(self, user: User):
        accounts = await self.account_repository.find_all_by_user_id(user.id)
        return {"accounts": accounts}

    async def get_account(self, account_id: int, user: User) -> Account | None:
        account = await self.account_repository.find_one(account_id)
        if not account:
            raise AccountNotFoundException
        if account.user_id != user.id:
            raise AccountPermissionDeniedException
        return account

    async def update_account(self, account_id: int, account_data: UpdateAccountSchema, user: User) -> Account:
        account = await self.account_repository.find_one(account_id)
        if not account:
            raise AccountNotFoundException
        if account.user_id != user.id:
            raise AccountPermissionDeniedException
        updated_data = account_data.model_dump(exclude_unset=True)
        account = await self.account_repository.update_one(account.id, updated_data)
        return account

    async def delete_account(self, account_id: int, user: User) -> None:
        account = await self.account_repository.find_one(account_id)
        if not account:
            raise AccountNotFoundException
        if account.user_id != user.id:
            raise AccountPermissionDeniedException
        await self.account_repository.delete_one(account.id)
