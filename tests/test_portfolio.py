import pytest
from portfolio_app.portfolio.models import (
    EconomicStatusAllocation,
    FundAssetAllocation,
    GrowthValueAllocation,
    MarketCapAllocation,
    RegionAllocation,
    SectorAllocation,
    SecurityAllocation,
    SecurityInfo,
    USInternationalAllocation,
)
from portfolio_app.portfolio.portfolio import (
    Portfolio,
    PortfolioType,
    SecurityHolding,
    SecurityType,
)


class TestPortfolio:
    @pytest.fixture
    def portfolio(self):
        portfolio = Portfolio(
            account_name="TEST ACCOUNT",
            portfolio_source="TEST",
            portfolio_type=PortfolioType.ROTH_IRA,
        )
        portfolio.set_cash(999.99)

        spy = SecurityHolding.build(
            symbol="SPY",
            name="SPDR S&P 500 ETF",
            security_type=SecurityType.ETF,
            quantity=10,
            last_price=100,
            avg_price_paid=50,
        )
        spy_allocation = SecurityAllocation(
            symbol="SPY",
            security_info=SecurityInfo(
                symbol="SPY",
                security_name="SPDR S&P 500 ETF",
                security_type=SecurityType.ETF,
                homepage_url="https://www.ssga.com/us/en/individual/etfs/funds/spdr-sp-500-etf-trust-spy",
                expense_ratio=0.09,
            ),
            fund_asset_allocation=FundAssetAllocation(
                stocks=100,
            ),
            market_cap_allocation=MarketCapAllocation(
                large_cap=100,
                mid_cap=0,
                small_cap=0,
            ),
            us_international_allocation=USInternationalAllocation(
                us=100,
            ),
            region_allocation=RegionAllocation(
                north_america=100,
            ),
            growth_value_allocation=GrowthValueAllocation(
                growth=60,
                value=40,
            ),
            economic_status_allocation=EconomicStatusAllocation(
                developed=100,
            ),
            sector_allocation=SectorAllocation(
                information_technology=20,
                health_care=20,
                financials=20,
                consumer_discretionary=20,
                energy=10,
                communication_services=10,
            ),
        )
        portfolio.add_security(spy)
        portfolio.add_security_allocation_data(spy_allocation)
        vti = SecurityHolding.build(
            symbol="VTI",
            name="Vanguard Total Stock Market ETF",
            security_type=SecurityType.ETF,
            quantity=8,
            last_price=200,
            avg_price_paid=180,
        )
        vti_allocation = SecurityAllocation(
            symbol="VTI",
            security_info=SecurityInfo(
                symbol="VTI",
                security_name="Vanguard Total Stock Market ETF",
                security_type=SecurityType.ETF,
                homepage_url="https://investor.vanguard.com/etf/profile/VTI",
                expense_ratio=0.03,
            ),
            fund_asset_allocation=FundAssetAllocation(
                stocks=100,
            ),
            market_cap_allocation=MarketCapAllocation(
                large_cap=60,
                mid_cap=30,
                small_cap=10,
            ),
            us_international_allocation=USInternationalAllocation(
                us=100,
            ),
            region_allocation=RegionAllocation(
                north_america=100,
            ),
            growth_value_allocation=GrowthValueAllocation(
                growth=50,
                value=50,
            ),
            economic_status_allocation=EconomicStatusAllocation(
                developed=100,
            ),
            sector_allocation=SectorAllocation(
                information_technology=20,
                health_care=20,
                financials=20,
                consumer_discretionary=20,
                communication_services=20,
            ),
        )
        portfolio.add_security(vti)
        portfolio.add_security_allocation_data(vti_allocation)
        vwo = SecurityHolding.build(
            symbol="VWO",
            name="Vanguard FTSE Emerging Markets ETF",
            security_type=SecurityType.ETF,
            quantity=5,
            last_price=50,
            avg_price_paid=40,
        )
        vwo_allocation = SecurityAllocation(
            symbol="VWO",
            security_info=SecurityInfo(
                symbol="VWO",
                security_name="Vanguard FTSE Emerging Markets ETF",
                security_type=SecurityType.ETF,
                homepage_url="https://investor.vanguard.com/etf/profile/VWO",
                expense_ratio=0.1,
            ),
            fund_asset_allocation=FundAssetAllocation(
                stocks=100,
            ),
            market_cap_allocation=MarketCapAllocation(
                large_cap=60,
                mid_cap=30,
                small_cap=10,
            ),
            us_international_allocation=USInternationalAllocation(
                international=100,
            ),
            region_allocation=RegionAllocation(
                north_america=0,
                emea=20,
                latam=20,
                apac=60,
            ),
            growth_value_allocation=GrowthValueAllocation(
                growth=50,
                value=50,
            ),
            economic_status_allocation=EconomicStatusAllocation(
                emerging=100,
            ),
            sector_allocation=SectorAllocation(
                information_technology=20,
                health_care=20,
                financials=20,
                consumer_discretionary=20,
                communication_services=20,
            ),
        )
        portfolio.add_security(vwo)
        portfolio.add_security_allocation_data(vwo_allocation)
        arkk = SecurityHolding.build(
            symbol="ARKK",
            name="ARK Innovation ETF",
            security_type=SecurityType.ETF,
            quantity=3,
            last_price=300,
            avg_price_paid=10,
        )
        arkk_allocation = SecurityAllocation(
            symbol="ARKK",
            security_info=SecurityInfo(
                symbol="ARKK",
                security_name="ARK Innovation ETF",
                security_type=SecurityType.ETF,
                homepage_url="https://ark-funds.com/arkk",
                expense_ratio=0.75,
            ),
            fund_asset_allocation=FundAssetAllocation(stocks=95, cash=5),
            market_cap_allocation=MarketCapAllocation(
                large_cap=80,
                mid_cap=20,
                small_cap=0,
            ),
            us_international_allocation=USInternationalAllocation(
                us=100,
            ),
            region_allocation=RegionAllocation(
                north_america=100,
            ),
            growth_value_allocation=GrowthValueAllocation(
                growth=100,
                value=0,
            ),
            economic_status_allocation=EconomicStatusAllocation(
                developed=100,
            ),
            sector_allocation=SectorAllocation(
                information_technology=90,
                health_care=10,
            ),
        )
        portfolio.add_security(arkk)
        portfolio.add_security_allocation_data(arkk_allocation)
        portfolio._data_complete = True
        return portfolio

    def test_portfolio_empty(self):
        subject = Portfolio(
            portfolio_source="TEST", portfolio_type=PortfolioType.ROTH_IRA
        )
        assert subject.holdings == {}

    def test_portfolio_df_keys(self, portfolio):
        df = portfolio.df()
        assert all(
            key in df.keys()
            for key in [
                "symbol",
                "name",
                "quantity",
                "last_price",
                "avg_price_paid",
                "total_value",
                "total_return",
            ]
        )
        assert df.columns.size == 7
        assert df.index.size == 4

    def test_portfolio_df_allocation_keys(self, portfolio):
        df = portfolio.allocation_df()
        for key in [
            "symbol",
            "security_name",
            "security_type",
            "homepage_url",
            "expense_ratio",
            "asset_type_stocks_pct",
            "asset_type_bonds_pct",
            "asset_type_cash_pct",
            "mc_large_cap_pct",
            "mc_mid_cap_pct",
            "mc_small_cap_pct",
            "intl_us_pct",
            "intl_international_pct",
            "region_north_america_pct",
            "region_emea_pct",
            "region_latam_pct",
            "region_apac_pct",
            "region_global__pct",
            "strategy_growth_pct",
            "strategy_value_pct",
            "econ_developed_pct",
            "econ_emerging_pct",
            "econ_frontier_pct",
            "sector_information_technology_pct",
            "sector_health_care_pct",
            "sector_financials_pct",
            "sector_consumer_discretionary_pct",
            "sector_energy_pct",
            "sector_communication_services_pct",
            "sector_consumer_staples_pct",
            "sector_industrials_pct",
            "sector_materials_pct",
            "sector_real_estate_pct",
            "sector_utilities_pct",
        ]:
            assert key in df.keys()
        assert df.columns.size == 35
        assert df.index.size == 4

    def test_portfolio_df_total_expense_ratio(self, portfolio):
        assert portfolio.get_total_expense_ratio() == 0.1764

    def test_portfolio_total_value(self, portfolio):
        assert portfolio.total_value() == 4749.99

    def test_portfolio_total_return(self, portfolio):
        assert portfolio.total_return() == 1580


class TestSecurity:
    def test_security(self):
        subject = SecurityHolding.build(
            symbol="AAPL",
            name="Apple",
            security_type=SecurityType.STOCK,
            quantity=10,
            last_price=100,
            avg_price_paid=50,
        )
        assert subject.symbol == "AAPL"
        assert subject.name == "Apple"
        assert subject.quantity == 10
        assert subject.last_price == 100
        assert subject.avg_price_paid == 50
        assert subject.total_value == 1000
        assert subject.total_return() == 500
        assert subject.to_dict() == {
            "symbol": "AAPL",
            "name": "Apple",
            "quantity": 10,
            "last_price": 100,
            "avg_price_paid": 50,
            "total_value": 1000,
            "total_return": 500,
        }
