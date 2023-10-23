from portfolio_app.portfolio.models import (
    EconomicStatusAllocation,
    SectorAllocation,
    GrowthValueAllocation,
    USInternationalAllocation,
    RegionAllocation,
    FundAssetAllocation,
)


def test_economic_status_allocation_keys_labels():
    keys, labels = EconomicStatusAllocation.keys_labels()
    assert keys == ["econ_status_developed_pct", "econ_status_emerging_pct", "econ_status_frontier_pct"]
    assert labels == ["Developed Markets", "Emerging Markets", "Frontier Markets"]


def test_growth_value_allocation_keys_labels():
    keys, labels = GrowthValueAllocation.keys_labels()
    assert keys == ["strategy_growth_pct", "strategy_value_pct"]
    assert labels == ["Growth", "Value"]


def test_us_international_allocation_keys_labels():
    keys, labels = USInternationalAllocation.keys_labels()
    assert keys == ["intl_us_pct", "intl_international_pct"]
    assert labels == ["US", "International"]


def test_region_allocation_keys_labels():
    keys, labels = RegionAllocation.keys_labels()
    assert keys == [
        "region_north_america_pct",
        "region_emea_pct",
        "region_latam_pct",
        "region_apac_pct",
        "region_global__pct",
    ]
    assert labels == [
        "North America",
        "Europe, Middle East, Africa",
        "Latin America",
        "Asia/Pacific",
        "Global",
    ]


def test_sector_allocation():
    allocation = SectorAllocation(information_technology=50, health_care=50)
    assert allocation.to_dict() == {
        "sector_information_technology_pct": 50,
        "sector_communication_services_pct": 0,
        "sector_consumer_discretionary_pct": 0,
        "sector_consumer_staples_pct": 0,
        "sector_energy_pct": 0,
        "sector_health_care_pct": 50,
        "sector_financials_pct": 0,
        "sector_industrials_pct": 0,
        "sector_materials_pct": 0,
        "sector_real_estate_pct": 0,
        "sector_utilities_pct": 0,
    }


def test_region_allocation():
    allocation = RegionAllocation(
        north_america=25, emea=25, latam=25, apac=25, global_=0
    )
    assert allocation.to_dict() == {
        "region_north_america_pct": 25,
        "region_emea_pct": 25,
        "region_latam_pct": 25,
        "region_apac_pct": 25,
        "region_global__pct": 0,
    }


def test_fund_asset_allocation():
    allocation = FundAssetAllocation(stocks=50, bonds=30, real_estate=20)
    assert allocation.to_dict() == {
        "asset_type_stocks_pct": 50,
        "asset_type_bonds_pct": 30,
        "asset_type_real_estate_pct": 20,
        "asset_type_cash_pct": 0,
    }
