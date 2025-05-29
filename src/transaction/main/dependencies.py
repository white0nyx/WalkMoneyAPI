from src.account.main.repository import AccountRepository
from src.category.main.repository import CategoryRepository
from src.transaction.main.repository import TransactionRepository
from src.transaction.main.service import TransactionService



def transaction_service() -> TransactionService:
    return TransactionService(TransactionRepository(), CategoryRepository(), AccountRepository())
