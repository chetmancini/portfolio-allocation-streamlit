from enum import Enum
from typing import Optional

import pandas as pd

from portfolio_app.portfolio.allocation import AllocationLookupService

allocation_service = AllocationLookupService()

class PortfolioType(Enum):
    TAXABLE = "Taxable"
    TRADITIONAL_IRA = "Traditional IRA"
    ROTH_IRA = "Roth IRA"
    SEP_IRA = "SEP IRA"
    SIMPLE_IRA = "SIMPLE IRA"
    SOLO_401K = "Solo 401k"
    TRADITIONAL_401K = "Traditional 401k"
    ROTH_401K = "Roth 401k"
    ACCT_403B = "403b"
    ACCT_457B = "457b"
    HSA = "HSA"
    ESA = "ESA"
    UGMA = "UGMA"
    UTMA = "UTMA"
    TRUST = "Trust"
    CUSTODIAL = "Custodial"
    JOINT = "Joint"
    OTHER = "Other"


class Portfolio:

    def __init__(
            self,
            account_name: str = None,
            portfolio_source: str = None,
            portfolio_type: PortfolioType = None
    ):
        self.holdings = {}
        self.cash = 0.0
        self.account_name = account_name
        self.portfolio_source = portfolio_source
        self.portfolio_type = portfolio_type
        self.security_allocation_data = {}
        self._data_complete = False

    def total_value(self) -> float:
        return self.cash + sum((holding.total_value for holding in self.holdings.values()))

    def add_security(self, security):
        self.holdings[security.symbol] = security

    def set_cash(self, cash) -> None:
        self.cash = cash

    def set_account_name(self, account_name) -> None:
        self.account_name = account_name

    def set_portfolio_type(self, portfolio_type: PortfolioType) -> None:
        self.portfolio_type = portfolio_type

    def _populate_security_names(self):
        for symbol, security in self.holdings.items():
            if symbol in self.security_allocation_data:
                if not security.name:
                    security.name = self.security_allocation_data[symbol].security_name
    
    def _fetch_security_data(self):
        for symbol in self.holdings.keys():
            self.security_allocation_data[symbol] = allocation_service.get_allocations_by_symbol(symbol)

    def _complete_portfolio_data(self):
        if not self.security_allocation_data or not self._data_complete:
            self._fetch_security_data()
            self._populate_security_names()
            self._data_complete = True

    def df(self):
        if not self._data_complete:
            self._complete_portfolio_data()
        return pd.DataFrame((holding.to_dict() for holding in self.holdings.values()))


class SecurityType(Enum):
    STOCK = 1
    OPTION = 2
    BOND = 3
    ETF = 4
    MUTUAL_FUND = 5
    OTHER = 6


class Security:

    def __init__(self):
        self.symbol = ''
        self.name = ''
        self.quantity = 0.0
        self.last_price = None
        self.avg_price_paid = None
        self.total_value = 0.0

    @classmethod
    def build(cls, symbol, name, quantity, last_price, avg_price_paid, total_value) -> 'Security':
        security = Security()
        security.symbol = symbol
        security.name = name
        security.quantity = quantity
        security.last_price = last_price
        security.avg_price_paid = avg_price_paid
        security.total_value = total_value
        return security

    def total_return(self) -> Optional[float]:
        if self.avg_price_paid and self.quantity:
            return self.total_value - (self.avg_price_paid * self.quantity)
        return None

    def to_dict(self):
        return {
            'symbol': self.symbol,
            'name': self.name,
            'quantity': self.quantity,
            'last_price': self.last_price,
            'avg_price_paid': self.avg_price_paid,
            'total_value': self.total_value,
            'total_return': self.total_return(),
        }
