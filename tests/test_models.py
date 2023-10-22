from portfolio_app.portfolio.models import (
    EconomicStatusAllocation,
    SectorAllocation,
    GrowthValueAllocation,
    USInternationalAllocation,
    RegionAllocation,
    FundAssetAllocation,
    MarketCapAllocation,
)


def test_economic_status_allocation_keys_labels():
    keys, labels = EconomicStatusAllocation.keys_labels()
    assert keys == ["developed_pct", "emerging_pct", "frontier_pct"]
    assert labels == ["Developed Markets", "Emerging Markets", "Frontier Markets"]


def test_growth_value_allocation_keys_labels():
    keys, labels = GrowthValueAllocation.keys_labels()
    assert keys == ["growth_pct", "value_pct"]
    assert labels == ["Growth", "Value"]


def test_us_international_allocation_keys_labels():
    keys, labels = USInternationalAllocation.keys_labels()
    assert keys == ["us_pct", "international_pct"]
    assert labels == ["US", "International"]


def test_region_allocation_keys_labels():
    keys, labels = RegionAllocation.keys_labels()
    assert keys == [
        "north_america_pct",
        "eama_pct",
        "latam_pct",
        "apac_pct",
        "global__pct",
    ]
    assert labels == [
        "North America",
        "Europe & Middle East",
        "Latin America",
        "Asia/Pacific",
        "Global",
    ]


def test_economic_status_allocation():
    allocation = EconomicStatusAllocation(developed=40, emerging=30, frontier=30)
    assert allocation.to_dict() == {
        "developed_pct": 40,
        "emerging_pct": 30,
        "frontier_pct": 30,
    }


def test_sector_allocation():
    allocation = SectorAllocation(information_technology=50, health_care=50)
    assert allocation.to_dict() == {
        "information_technology_pct": 50,
        "communication_services_pct": 0,
        "consumer_discretionary_pct": 0,
        "consumer_staples_pct": 0,
        "energy_pct": 0,
        "health_care_pct": 50,
        "financials_pct": 0,
        "industrials_pct": 0,
        "materials_pct": 0,
        "real_estate_pct": 0,
        "utilities_pct": 0,
    }


def test_growth_value_allocation():
    allocation = GrowthValueAllocation(growth=60, value=40)
    assert allocation.to_dict() == {"growth_pct": 60, "value_pct": 40}


def test_us_international_allocation():
    allocation = USInternationalAllocation(us=70, international=30)
    assert allocation.to_dict() == {"us_pct": 70, "international_pct": 30}


def test_region_allocation():
    allocation = RegionAllocation(
        north_america=25, eama=25, latam=25, apac=25, global_=0
    )
    assert allocation.to_dict() == {
        "north_america_pct": 25,
        "eama_pct": 25,
        "latam_pct": 25,
        "apac_pct": 25,
        "global__pct": 0,
    }


def test_fund_asset_allocation():
    allocation = FundAssetAllocation(stocks=50, bonds=30, real_estate=20)
    assert allocation.to_dict() == {
        "stocks_pct": 50,
        "bonds_pct": 30,
        "real_estate_pct": 20,
        "cash_pct": 0,
    }


def test_market_cap_allocation():
    allocation = MarketCapAllocation(large_cap=40, mid_cap=30, small_cap=30)
    assert allocation.to_dict() == {
        "large_cap_pct": 40,
        "mid_cap_pct": 30,
        "small_cap_pct": 30,
    }
