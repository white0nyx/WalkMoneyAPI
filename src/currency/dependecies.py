from src.currency.repository import CurrencyRepository
from src.currency.service import CurrencyService


def currency_service() -> CurrencyService:
    return CurrencyService(CurrencyRepository())
