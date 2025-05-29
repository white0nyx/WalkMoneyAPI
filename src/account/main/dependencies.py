from src.account.main.repository import AccountRepository
from src.account.main.service import AccountService


def account_service() -> AccountService:
    return AccountService(AccountRepository())
