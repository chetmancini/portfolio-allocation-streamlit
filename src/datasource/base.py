from abc import ABCMeta, abstractmethod

from portfolio import Portfolio


class DataSource(metaclass=ABCMeta):

    @abstractmethod
    def get_portfolio(self, *args, **kwargs) -> Portfolio:
        pass
