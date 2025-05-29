import logging
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends

from src.currency.service import CurrencyService
from src.currency.dependecies import currency_service
router = APIRouter(
    prefix="/currency_api",
    tags=["currency_api"],
    responses={404: {"description": "Not found"}},
)

@router.get("")
async def get_currencies(
        service: Annotated[CurrencyService, Depends(currency_service)],
):
    try:
        currencies = await service.currency_repository.find_all()
        return currencies
    except HTTPException:
        raise
    except Exception as e:
        logging.exception(f"Error getting currencies. Error: {e}")
        raise HTTPException(status_code=400, detail="Error getting currencies")

