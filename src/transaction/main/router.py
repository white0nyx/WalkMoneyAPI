import logging
from typing import List, Annotated

from fastapi import APIRouter, HTTPException, Depends

from src.auth import jwt_auth
from src.transaction.main.dependencies import transaction_service
from src.transaction.main.schemas import CreateTransactionSchema, UpdateTransactionSchema, GetTransactionSchema, GetStatisticByCategoriesParams
from src.transaction.main.service import TransactionService
from src.user.models import User
from src.transaction.main.schemas import GetTransactionParamsSchema

router = APIRouter(
    prefix="/transaction",
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
    params: Annotated[GetTransactionParamsSchema, Depends()],
    service: Annotated[TransactionService, Depends(transaction_service)],
    user: User = Depends(jwt_auth.get_current_user),
):
    try:
        transactions = await service.get_all_transactions(user.id, params)
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
        transaction = await service.update_transaction(transaction_id, transaction_data, user)
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

@router.get("/statistic/by_time")
async def get_subcategory_statistic_by_time(
    params: Annotated[GetStatisticByCategoriesParams, Depends()],
    service: Annotated[TransactionService, Depends(transaction_service)],
    user: Annotated[User, Depends(jwt_auth.get_current_user),],
):
    try:
        statistic = await service.get_time_statistics(params, user.id)
        return statistic
    except HTTPException:
        raise
    except Exception as e:
        logging.exception(f"Error getting subcategory statistic by categories. Error: {e}")
        raise HTTPException(status_code=400, detail="Error getting subcategory statistic by categories")


@router.get("/statistic/by_categories")
async def get_total_category_statistics(
    params: Annotated[GetStatisticByCategoriesParams, Depends()],
    service: Annotated[TransactionService, Depends(transaction_service)],
    user: Annotated[User, Depends(jwt_auth.get_current_user)],
):
    try:
        result = await service.get_category_statistics(params, user.id)
        return result
    except Exception as e:
        logging.exception(f"Error getting total category statistics: {e}")
        raise HTTPException(status_code=400, detail="Error getting total category statistics")



