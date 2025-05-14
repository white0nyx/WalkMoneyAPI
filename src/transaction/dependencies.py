from fastapi import Depends
from src.transaction.repository import TransactionRepository
from src.transaction.service import TransactionService

def get_transaction_repository() -> TransactionRepository:
    return TransactionRepository()

def get_transaction_service(transaction_repository: TransactionRepository = Depends(get_transaction_repository)) -> TransactionService:
    return TransactionService(transaction_repository)
