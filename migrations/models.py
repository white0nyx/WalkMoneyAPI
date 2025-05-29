from src.account.models import Account
from src.account_type.models import AccountType
from src.budget.models import Budget
from src.category.main.models import Category
from src.currency.models import Currency
from src.role.models import Role
from src.subcategory.main.models import SubCategory
from src.transaction.main.models import Transaction
from src.transfer.models import Transfer
from src.user.models import User

all_models = [
    Account,
    AccountType,
    Budget,
    Category,
    SubCategory,
    Currency,
    Role,
    User,
    Transaction,
    Transfer,
]