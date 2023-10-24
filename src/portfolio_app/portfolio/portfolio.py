from enum import Enum
from typing import Dict, List, Optional
import streamlit as st
import pandas as pd

from portfolio_app.repository.allocation import AllocationLookupService
from portfolio_app.portfolio.models import (
    EconomicStatusAllocation,
    GrowthValueAllocation,
    MarketCapAllocation,
    RegionAllocation,
    SectorAllocation,
    SecurityAllocation,
    SecurityType,
    USInternationalAllocation,
)
from portfolio_app.portfolio.util import float_dollars, float_pct

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
        portfolio_type: PortfolioType = None,
    ):
        self.holdings: Dict[str, Security] = {}
        self.cash: float = 0.0
        self.account_name: str = account_name
        self.portfolio_source: str = portfolio_source
        self.portfolio_type: PortfolioType = portfolio_type
        self.security_allocation_data: Dict[str, SecurityAllocation] = {}
        self._data_complete: bool = False

    def total_value(self) -> float:
        return self.cash + sum(
            (holding.total_value for holding in self.holdings.values())
        )

    def total_return(self) -> float:
        return sum((holding.total_return() for holding in self.holdings.values()))

    def add_security(self, security):
        self.holdings[security.symbol] = security

    def add_security_allocation_data(
        self, security_allocation_data: SecurityAllocation
    ):
        self.security_allocation_data[
            security_allocation_data.symbol
        ] = security_allocation_data

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
            self.security_allocation_data[
                symbol
            ] = allocation_service.get_allocations_by_symbol(symbol)

    def _complete_portfolio_data(self):
        if not self.security_allocation_data or not self._data_complete:
            self._fetch_security_data()
            self._populate_security_names()
            self._data_complete = True

    @st.cache_data()
    def allocation_df(_self) -> pd.DataFrame:
        if not _self._data_complete:
            _self._complete_portfolio_data()
        return pd.DataFrame(
            (
                security_allocation.to_dict()
                for security_allocation in _self.security_allocation_data.values()
            )
        )

    @st.cache_data()
    def df(_self) -> pd.DataFrame:
        if not _self._data_complete:
            _self._complete_portfolio_data()
        return pd.DataFrame((holding.to_dict() for holding in _self.holdings.values()))

    def _merged_df(self) -> pd.DataFrame:
        securities_df = self.df()
        allocation_df = self.allocation_df()
        return pd.merge(securities_df, allocation_df, on="symbol")

    def get_total_expense_ratio(self) -> float:
        df = self._merged_df()
        return (
            df["quantity"] * df["last_price"] * df["expense_ratio"]
        ).sum() / self.total_value()

    def get_bucketed_df(self, keys: List[str], labels: List[str]) -> pd.DataFrame:
        merged_df = self._merged_df()
        totals = [
            (
                merged_df["quantity"] * merged_df["last_price"] * merged_df[key] / 100
            ).sum()
            for key in keys
        ]
        total_value = sum(totals)
        percentages = (float_pct((total / total_value) * 100) for total in totals)
        return pd.DataFrame(
            {
                "Total Value": (float_dollars(total) for total in totals),
                "Percentage": percentages,
            },
            index=labels,
        )

    def get_us_international_df(self) -> pd.DataFrame:
        return self.get_bucketed_df(*USInternationalAllocation.keys_labels())

    def get_growth_value_df(self) -> pd.DataFrame:
        return self.get_bucketed_df(*GrowthValueAllocation.keys_labels())

    def get_market_cap_df(self) -> pd.DataFrame:
        return self.get_bucketed_df(*MarketCapAllocation.keys_labels())

    def get_region_df(self) -> pd.DataFrame:
        return self.get_bucketed_df(*RegionAllocation.keys_labels())

    def get_economic_status_df(self) -> pd.DataFrame:
        return self.get_bucketed_df(*EconomicStatusAllocation.keys_labels())

    def get_sector_df(self) -> pd.DataFrame:
        return self.get_bucketed_df(*SectorAllocation.keys_labels())


class Security:
    def __init__(self):
        self.symbol: str = ""
        self.name: str = ""
        self.security_type: SecurityType = None
        self.quantity: float = 0.0
        self.last_price = None
        self.avg_price_paid = None
        self.total_value = 0.0

    @classmethod
    def build(
        cls,
        symbol: str,
        name: Optional[str],
        security_type: Optional[SecurityType],
        quantity: float,
        last_price,
        avg_price_paid,
        total_value: Optional[float] = None,
    ) -> "Security":
        security = Security()
        security.symbol = symbol
        security.name = name
        security.security_type = security_type
        security.quantity = quantity
        security.last_price = last_price
        security.avg_price_paid = avg_price_paid
        security.total_value = total_value or (quantity * last_price)
        return security

    def total_return(self) -> Optional[float]:
        if self.avg_price_paid and self.quantity:
            return self.total_value - (self.avg_price_paid * self.quantity)
        return None

    def to_dict(self):
        return {
            "symbol": self.symbol,
            "name": self.name,
            "quantity": self.quantity,
            "last_price": self.last_price,
            "avg_price_paid": self.avg_price_paid,
            "total_value": self.total_value,
            "total_return": self.total_return(),
        }
