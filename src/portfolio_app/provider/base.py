from abc import ABCMeta, abstractmethod
from datetime import date
from typing import Tuple


class LastPriceProviderClient(metaclass=ABCMeta):
    """
    Data provider to get the last price of a security.
    """

    @abstractmethod
    def last_price(self, symbol: str) -> Tuple[date, float]:
        raise NotImplementedError()
