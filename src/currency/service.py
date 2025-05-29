from src.currency.repository import CurrencyRepository


class CurrencyService:

    def __init__(self, currency_repository: CurrencyRepository):
        self.currency_repository = currency_repository