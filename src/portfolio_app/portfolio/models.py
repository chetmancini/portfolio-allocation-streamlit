
from typing import List, Tuple
from pydantic import BaseModel, Field


class USInternationalAllocation(BaseModel):
    """US and international allocation in percentages."""
    us: int
    international: int

    def to_dict(self):
        return {
            "us_pct": self.us,
            "international_pct": self.international,
        }
    
    @classmethod
    def keys_labels(cls) -> Tuple[List[str], List[str]]:
        return cls().to_dict().keys(), ['US', 'International']


class RegionAllocation(BaseModel):
    """Region allocation in percentages."""
    north_america: int = Field(default=0, strict=False)
    eama: int = Field(default=0, strict=False)
    latam: int = Field(default=0, strict=False)
    apac: int = Field(default=0, strict=False)
    global_: int = Field(alias="global", default=100, strict=False)

    def to_dict(self):
        return {
            "region_north_america_pct": self.north_america,
            "region_eama_pct": self.eama,
            "region_latam_pct": self.latam,
            "region_apac_pct": self.apac,
            "region_global_pct": self.global_,
        }

    def keys_labels(cls) -> Tuple[List[str], List[str]]:
        return cls().to_dict().keys(), ['North America', 'EAMA', 'LATAM', 'APAC', 'Global']


class FundAssetAllocation(BaseModel):
    """Fund asset allocation in percentages."""
    stocks: int
    bonds: int
    real_estate: int
    cash: int

    def to_dict(self):
        return {
            "stocks_pct": self.stocks,
            "bonds_pct": self.bonds,
            "real_estate_pct": self.real_estate,
            "cash_pct": self.cash,
        }
    
    @classmethod
    def keys_labels(cls) -> Tuple[List[str], List[str]]:
        return cls().to_dict().keys(), ['Stocks', 'Bonds', 'Real Estate', 'Cash']
        


class MarketCapAllocation(BaseModel):
    """Market cap allocation in percentages."""
    large_cap: int = Field(strict=False)
    mid_cap: int = Field(strict=False)
    small_cap: int = Field(strict=False)

    def to_dict(self):
        return {
            "large_cap_pct": self.large_cap,
            "mid_cap_pct": self.mid_cap,
            "small_cap_pct": self.small_cap,
        }
    
    @classmethod
    def keys_labels(cls) -> Tuple[List[str], List[str]]:
        return cls().to_dict().keys(), ['Large Cap', 'Mid Cap', 'Small Cap']


class GrowthValueAllocation(BaseModel):
    """Growth value allocation in percentages."""
    growth: int
    value: int

    def to_dict(self):
        return {
            "growth_pct": self.growth,
            "value_pct": self.value,
        }
    
    def keys_labels(cls) -> Tuple[List[str], List[str]]:
        return cls().to_dict().keys(), ['Growth', 'Value']


class EconomicStatusAllocation(BaseModel):
    """Economic status allocation in percentages."""
    developed: int
    emerging: int
    frontier: int

    def to_dict(self):
        return {
            "developed_markets_pct": self.developed,
            "emerging_markets_pct": self.emerging,
            "frontier_markets_pct": self.frontier,
        }

    @classmethod 
    def keys_labels(cls) -> Tuple[List[str], List[str]]:
        return cls().to_dict().keys(), ['Developed Markets', 'Emerging Markets', 'Frontier Markets']
    

class SectorAllocation(BaseModel):
    """Sector allocation in percentages."""
    information_technology: int
    health_care: int
    financials: int
    consumer_discretionary: int
    communication_services: int
    industrials: int
    consumer_staples: int
    energy: int
    utilities: int
    real_estate: int
    materials: int

    def to_dict(self):
        return {
            "sector_information_technology_pct": self.information_technology,
            "sector_health_care_pct": self.health_care,
            "sector_financials_pct": self.financials,
            "sector_consumer_discretionary_pct": self.consumer_discretionary,
            "sector_communication_services_pct": self.communication_services,
            "sector_industrials_pct": self.industrials,
            "sector_consumer_staples_pct": self.consumer_staples,
            "sector_energy_pct": self.energy,
            "sector_utilities_pct": self.utilities,
            "sector_real_estate_pct": self.real_estate,
            "sector_materials_pct": self.materials,
        }
    
    @classmethod
    def keys_labels(cls) -> Tuple[List[str], List[str]]:
        return cls().to_dict().keys(), [
            'Information Technology', 
            'Health Care', 
            'Financials', 
            'Consumer Discretionary', 
            'Communication Services',
            'Industrials', 
            'Consumer Staples', 
            'Energy', 'Utilities', 
            'Real Estate', 
            'Materials'
        ]


class SecurityAllocation(BaseModel):
    """Security allocation in percentages."""
    symbol: str
    security_name: str

    fund_asset_allocation: FundAssetAllocation
    market_cap_allocation: MarketCapAllocation
    us_international_allocation: USInternationalAllocation
    region_allocation: RegionAllocation
    growth_value_allocation: GrowthValueAllocation
    economic_status_allocation: EconomicStatusAllocation

    def to_dict(self):
        ret = {
            "symbol": self.symbol,
            "security_name": self.security_name,
        }
        ret.update(self.fund_asset_allocation.to_dict())
        ret.update(self.market_cap_allocation.to_dict())
        ret.update(self.us_international_allocation.to_dict())
        ret.update(self.region_allocation.to_dict())
        ret.update(self.growth_value_allocation.to_dict())
        ret.update(self.economic_status_allocation.to_dict())
        return ret
    