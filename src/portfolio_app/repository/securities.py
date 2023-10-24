from typing import Iterable, Tuple

from portfolio_app.portfolio.models import SecurityAllocation


class SecurityDataRepository:
    def __init__(self) -> None:
        pass

    def get_many_securities(
        self, symbols: Iterable[str]
    ) -> Iterable[SecurityAllocation]:
        pass

    def get_single_security_by_symbol(self, symbol: str) -> SecurityAllocation:
        pass

    def get_last_price_by_symbol(self, symbol: str) -> float:
        pass

    def get_last_prices_by_symbols(
        self, symbols: Iterable[str]
    ) -> Iterable[Tuple[str, float]]:
        pass
