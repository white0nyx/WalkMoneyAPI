import logging
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends

from src.account_type.dependencies import account_type_service
from src.account_type.service import AccountTypeService

router = APIRouter(
    prefix="/account_type_api",
    tags=["account_type_api"],
    responses={404: {"description": "Not found"}},
)

@router.get("")
async def get_account_types(
        service: Annotated[AccountTypeService, Depends(account_type_service)],
):
    try:
        account_types = await service.account_type_repository.find_all()
        return account_types
    except HTTPException:
        raise
    except Exception as e:
        logging.exception(f"Error getting account types. Error: {e}")
        raise HTTPException(status_code=400, detail="Error getting account types")

