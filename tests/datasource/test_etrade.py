import pytest
from src.datasource.etrade import ETradeCSVDataSource
from portfolio.portfolio import Portfolio

@pytest.fixture
def etrade():
    return ETradeCSVDataSource('resources/portfolio-etrade-sample.csv')

def test_get_portfolio_name(etrade):
    assert etrade.get_portfolio_name() == 'E*Trade CSV'

def test_get_portfolio(etrade):
    portfolio = etrade.get_portfolio()
    assert isinstance(portfolio, Portfolio)
    assert portfolio.get_account_name() == 'E*Trade CSV'
    assert portfolio.get_cash() == 0.0
    assert len(portfolio.get_securities()) == 10