from abc import ABCMeta, abstractmethod
from datetime import date
from typing import Tuple

from portfolio_app.portfolio.models import SecurityAllocation


class LastPriceProviderClient(metaclass=ABCMeta):
    """
    Data provider to get the last price of a security.
    """

    @abstractmethod
    def last_price(self, symbol: str) -> Tuple[date, float]:
        raise NotImplementedError()


class AllocationDataClient(metaclass=ABCMeta):
    def lookup_allocation(self, symbol: str) -> SecurityAllocation:
        pass

    async def lookup_allocation_async(self, symbol: str) -> SecurityAllocation:
        pass
