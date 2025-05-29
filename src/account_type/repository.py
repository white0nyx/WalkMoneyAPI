from src.account_type.models import AccountType
from src.common.repository import SQLAlchemyRepository


class AccountTypeRepository(SQLAlchemyRepository):
    model: type[AccountType] = AccountType
