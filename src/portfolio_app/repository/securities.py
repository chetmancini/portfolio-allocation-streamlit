from typing import Iterable

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
