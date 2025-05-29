from src.account_type.repository import AccountTypeRepository
from src.account_type.service import AccountTypeService


def account_type_service() -> AccountTypeService:
    return AccountTypeService(AccountTypeRepository())
