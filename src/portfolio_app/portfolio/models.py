from typing import List, Tuple
from pydantic import BaseModel, Field

class BaseAllocationModel(BaseModel):
    """Base allocation model."""

    def to_dict(self):
        return {f"{f}_pct": getattr(self, f) for f in self.__fields__}

    @classmethod
    def keys_labels(cls) -> Tuple[List[str], List[str]]:
        return [f"{f}_pct" for f in cls.__fields__], [f.title for f in cls.__fields__.values()]


class USInternationalAllocation(BaseAllocationModel):
    """US and international allocation in percentages."""

    us: int = Field(title="US", default=0, strict=False)
    international: int = Field(title="International", default=0, strict=False)


class RegionAllocation(BaseAllocationModel):
    """Region allocation in percentages."""

    north_america: int = Field(title="North America", default=0, strict=False)
    eama: int = Field(title="Europe & Middle East",default=0, strict=False)
    latam: int = Field(title="Latin America", default=0, strict=False)
    apac: int = Field(title="Asia/Pacific", default=0, strict=False)
    global_: int = Field(title="Global", alias="global", default=100, strict=False)


class FundAssetAllocation(BaseAllocationModel):
    """Fund asset allocation in percentages."""

    stocks: int = Field(title="Stocks", default=0, strict=False)
    bonds: int = Field(title="Bonds", default=0, strict=False)
    real_estate: int = Field(title="Real Estate", default=0, strict=False)
    cash: int = Field(title="Cash", default=0, strict=False)


class MarketCapAllocation(BaseAllocationModel):
    """Market cap allocation in percentages."""

    large_cap: int = Field(title="Large Cap", strict=False)
    mid_cap: int = Field(title="Mid Cap", strict=False)
    small_cap: int = Field(title="Small Cap", strict=False)


class GrowthValueAllocation(BaseAllocationModel):
    """Growth value allocation in percentages."""

    growth: int = Field(title="Growth", default=0, strict=False)
    value: int = Field(title="Value", default=0, strict=False)



class EconomicStatusAllocation(BaseAllocationModel):
    """Economic status allocation in percentages."""

    developed: int = Field(title="Developed Markets", default=0, strict=False)
    emerging: int = Field(title="Emerging Markets", default=0, strict=False)
    frontier: int = Field(title="Frontier Markets", default=0, strict=False)


class SectorAllocation(BaseAllocationModel):
    """Sector allocation in percentages."""

    information_technology: int = Field(title="Information Technology")
    health_care: int = Field(title="Health Care")
    financials: int = Field(title="Financials")
    consumer_discretionary: int = Field(title="Consumer Discretionary")
    communication_services: int = Field(title="Communication Services")
    industrials: int = Field(title="Industrials")
    consumer_staples: int = Field(title="Consumer Staples")
    energy: int = Field(title="Energy")
    utilities: int = Field(title="Utilities")
    real_estate: int = Field(title="Real Estate")
    materials: int = Field(title="Materials")


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
