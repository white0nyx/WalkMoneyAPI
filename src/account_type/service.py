from src.account_type.repository import AccountTypeRepository


class AccountTypeService:

    def __init__(self, account_type_repository: AccountTypeRepository):
        self.account_type_repository = account_type_repository