from io import BytesIO
import pytest

from portfolio_app.datasource.etrade import ETradeCSVDataSource
from portfolio_app.portfolio.portfolio import Portfolio


@pytest.fixture
def etrade():
    with open('resources/portfolio-etrade-sample.csv', "rb") as fh:
        buf = BytesIO(fh.read())
    return ETradeCSVDataSource(buf)

def test_get_portfolio_name(etrade):
    assert etrade.get_portfolio_name() == 'Roth IRA -XXXX'

def test_get_portfolio(etrade):
    portfolio = etrade.get_portfolio()
    assert isinstance(portfolio, Portfolio)
    assert portfolio.account_name == 'Roth IRA -XXXX'
    assert portfolio.cash == 781.05
    assert len(portfolio.holdings) == 12