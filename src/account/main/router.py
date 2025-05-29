


import logging
from typing import List, Annotated

from fastapi import APIRouter, HTTPException, Depends

from src.account.main.schemas import CreateAccountSchema, GetAccountSchema, ResponseGetAccountsSchema, GetSelectedAccountSchema, UpdateAccountSchema
from src.account.main.service import AccountService
from src.auth import jwt_auth
from src.account.main.dependencies import account_service
from src.user.models import User

router = APIRouter(
    prefix="/account_api",
    tags=["account_api"],
    responses={404: {"description": "Not found"}},
)

@router.post("", response_model=GetAccountSchema)
async def create_account(
        account_data: CreateAccountSchema,
        service: Annotated[AccountService, Depends(account_service)],
        user: Annotated[User, Depends(jwt_auth.get_current_user)]
):
    try:
        account = await service.create_account(account_data, user)
        return account
    except HTTPException:
        raise
    except Exception as e:
        logging.exception(f"Error creating account. Error: {e}")
        raise HTTPException(status_code=400, detail="Error creating account")


@router.get("", response_model=ResponseGetAccountsSchema)
async def get_accounts(
        service: Annotated[AccountService, Depends(account_service)],
        user: Annotated[User, Depends(jwt_auth.get_current_user)],
):
    try:
        accounts = await service.get_accounts(user)
        return accounts
    except HTTPException:
        raise
    except Exception as e:
        logging.exception(f"Error getting accounts. Error: {e}")
        raise HTTPException(status_code=400, detail="Error getting accounts")


@router.get("/{account_id}", response_model=GetSelectedAccountSchema)
async def get_account(
        account_id: int,
        service: Annotated[AccountService, Depends(account_service)],
        user: Annotated[User, Depends(jwt_auth.get_current_user)],
):
    try:
        account = await service.get_account(account_id, user)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        return account
    except HTTPException:
        raise
    except Exception as e:
        logging.exception(f"Error getting account with id {account_id}. Error: {e}")
        raise HTTPException(status_code=400, detail="Error getting account")


@router.patch("/{account_id}", response_model=GetSelectedAccountSchema)
async def update_account(
        account_id: int,
        account_data: UpdateAccountSchema,
        service: Annotated[AccountService, Depends(account_service)],
        user: Annotated[User, Depends(jwt_auth.get_current_user)],
):
    try:
        account = await service.update_account(account_id, account_data, user)
        return account
    except HTTPException:
        raise
    except Exception as e:
        logging.exception(f"Error updating account with id {account_id}. Error: {e}")
        raise HTTPException(status_code=400, detail="Error updating account")


@router.delete("/{account_id}")
async def delete_account(
        account_id: int,
        service: Annotated[AccountService, Depends(account_service)],
        user: Annotated[User, Depends(jwt_auth.get_current_user)],
):
    try:
        await service.delete_account(account_id, user)
        return {"message": "Account deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logging.exception(f"Error deleting account with id {account_id}. Error: {e}")
        raise HTTPException(status_code=400, detail="Error deleting account")