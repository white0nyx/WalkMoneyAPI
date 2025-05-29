from src.account.main.models import Account
from src.account.main.repository import AccountRepository
from src.account.main.schemas import CreateAccountSchema
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
