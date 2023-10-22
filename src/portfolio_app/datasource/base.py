from abc import ABCMeta, abstractmethod
from portfolio_app.portfolio.portfolio import Portfolio


class DataSource(metaclass=ABCMeta):

    @abstractmethod
    def validate(self) -> bool:
        pass

    @abstractmethod
    def get_portfolio(self, *args, **kwargs) -> Portfolio:
        pass
