


import logging
from typing import List, Annotated

from fastapi import APIRouter, HTTPException, Depends

from src.account.main.schemas import CreateAccountSchema, GetAccountSchema, ResponseGetAccountsSchema
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