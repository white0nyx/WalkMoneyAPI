from src.common.repository import SQLAlchemyRepository
from src.currency.models import Currency


class CurrencyRepository(SQLAlchemyRepository):
    model: type[Currency] = Currency
