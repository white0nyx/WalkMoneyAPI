import logging
from typing import List, Annotated

from fastapi import APIRouter, HTTPException, Depends

from src.auth import jwt_auth
from src.transaction.main.dependencies import transaction_service
from src.transaction.main.schemas import CreateTransactionSchema, UpdateTransactionSchema, GetTransactionSchema
from src.transaction.main.service import TransactionService
from src.user.models import User

router = APIRouter(
    prefix="/transaction_api",
    tags=["transaction_api"],
    responses={404: {"description": "Not found"}},
)

@router.post("", response_model=GetTransactionSchema)
async def create_transaction(
    transaction_data: CreateTransactionSchema,
    service: Annotated[TransactionService, Depends(transaction_service)],
    user: User = Depends(jwt_auth.get_current_user),
):
    try:
        transaction = await service.create_transaction(transaction_data, user)
        return transaction
    except Exception as e:
        logging.exception(f"Error creating transaction. Error: {e}")
        raise HTTPException(status_code=400, detail="Error creating transaction")


@router.get("/{transaction_id}", response_model=GetTransactionSchema)
async def get_transaction(
    transaction_id: int,
    service: Annotated[TransactionService, Depends(transaction_service)],
    user: User = Depends(jwt_auth.get_current_user),
):
    try:
        transaction = await service.get_transaction(transaction_id, user)
        return transaction
    except HTTPException:
        raise
    except Exception as e:
        logging.exception(f"Error getting transaction. Error: {e}")
        raise HTTPException(status_code=400, detail="Error getting transaction")


@router.get("", response_model=List[GetTransactionSchema])
async def get_all_transactions(
    service: Annotated[TransactionService, Depends(transaction_service)],
    user: User = Depends(jwt_auth.get_current_user),
):
    try:
        transactions = await service.get_all_transactions(user)
        return transactions
    except HTTPException:
        raise
    except Exception as e:
        logging.exception(f"Error getting transactions. Error: {e}")
        raise HTTPException(status_code=400, detail="Error getting transactions")


@router.put("/{transaction_id}", response_model=GetTransactionSchema)
async def update_transaction(
    transaction_id: int,
    transaction_data: UpdateTransactionSchema,
    service: Annotated[TransactionService, Depends(transaction_service)],
    user: User = Depends(jwt_auth.get_current_user),
):
    try:
        transaction = await service.update_transaction(transaction_id, transaction_data.model_dump(), user)
        return transaction
    except HTTPException:
        raise
    except Exception as e:
        logging.exception(f"Error updating transaction. Error: {e}")
        raise HTTPException(status_code=400, detail="Error updating transaction")


@router.delete("/{transaction_id}")
async def delete_transaction(
    transaction_id: int,
    service: Annotated[TransactionService, Depends(transaction_service)],
    user: User = Depends(jwt_auth.get_current_user),
):
    try:
        await service.delete_transaction(transaction_id, user)
        return {"message": "Transaction deleted"}
    except HTTPException:
        raise
    except Exception as e:
        logging.exception(f"Error deleting transaction. Error: {e}")
        raise HTTPException(status_code=400, detail="Error deleting transaction")



