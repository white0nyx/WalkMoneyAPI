import logging
from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from src.auth import jwt_auth
from src.transaction.dependencies import get_transaction_service
from src.transaction.schemas import TransactionSchema, CreateTransactionSchema, UpdateTransactionSchema
from src.transaction.service import TransactionService, TransactionNotFoundError, AccessForbiddenError
from src.user.models import User

router = APIRouter(
    prefix="/transaction_api",
    tags=["transaction_api"],
    responses={404: {"description": "Not found"}},
)

@router.post("/transactions", response_model=TransactionSchema)
async def create_transaction(
    transaction_data: CreateTransactionSchema,
    transaction_service: TransactionService = Depends(get_transaction_service),
    user: User = Depends(jwt_auth.get_current_user),
):
    try:
        transaction = await transaction_service.create_transaction(transaction_data.model_dump(), user)
        return transaction
    except Exception as e:
        logging.exception(f"Transaction creation error. Data: {transaction_data} Error: {e}")
        raise HTTPException(status_code=400, detail="Transaction creation error")


@router.get("/transactions/{transaction_id}", response_model=TransactionSchema)
async def get_transaction(
    transaction_id: int,
    transaction_service: TransactionService = Depends(get_transaction_service),
    user: User = Depends(jwt_auth.get_current_user),
):
    try:
        transaction = await transaction_service.get_transaction(transaction_id, user)
        return transaction
    except TransactionNotFoundError:
        raise HTTPException(status_code=404, detail="Transaction not found")
    except AccessForbiddenError:
        raise HTTPException(status_code=403, detail="Access to this transaction is forbidden")


@router.get("/transactions", response_model=List[TransactionSchema])
async def get_all_transactions(
    transaction_service: TransactionService = Depends(get_transaction_service),
    user: User = Depends(jwt_auth.get_current_user),
):
    try:
        transactions = await transaction_service.get_all_transactions(user)
        return transactions
    except AccessForbiddenError:
        raise HTTPException(status_code=403, detail="Access to transactions is forbidden")


@router.put("/transactions/{transaction_id}", response_model=TransactionSchema)
async def update_transaction(
    transaction_id: int,
    transaction_data: UpdateTransactionSchema,
    transaction_service: TransactionService = Depends(get_transaction_service),
    user: User = Depends(jwt_auth.get_current_user),
):
    try:
        transaction = await transaction_service.update_transaction(transaction_id, transaction_data.model_dump(), user)
        return transaction
    except TransactionNotFoundError:
        raise HTTPException(status_code=404, detail="Transaction not found")
    except AccessForbiddenError:
        raise HTTPException(status_code=403, detail="Access to this transaction is forbidden")


@router.delete("/transactions/{transaction_id}")
async def delete_transaction(
    transaction_id: int,
    transaction_service: TransactionService = Depends(get_transaction_service),
    user: User = Depends(jwt_auth.get_current_user),
):
    try:
        await transaction_service.delete_transaction(transaction_id, user)
        return {"message": "Transaction deleted"}
    except TransactionNotFoundError:
        raise HTTPException(status_code=404, detail="Transaction not found")
    except AccessForbiddenError:
        raise HTTPException(status_code=403, detail="Access to this transaction is forbidden")


@router.get("/transactions/by_account/{account_id}", response_model=List[TransactionSchema])
async def get_transactions_by_account(
    account_id: int,
    transaction_service: TransactionService = Depends(get_transaction_service),
    user: User = Depends(jwt_auth.get_current_user),
):
    try:
        transactions = await transaction_service.find_transactions_by_account(account_id, user)
        return transactions
    except AccessForbiddenError:
        raise HTTPException(status_code=403, detail="Access to this transaction is forbidden")


@router.get("/transactions/by_date_range", response_model=List[TransactionSchema])
async def get_transactions_by_date_range(
    start_date: datetime,
    end_date: datetime,
    transaction_service: TransactionService = Depends(get_transaction_service),
    user: User = Depends(jwt_auth.get_current_user),
):
    try:
        transactions = await transaction_service.find_transactions_by_date_range(start_date, end_date, user)
        return transactions
    except AccessForbiddenError:
        raise HTTPException(status_code=403, detail="Access to this transaction is forbidden")
