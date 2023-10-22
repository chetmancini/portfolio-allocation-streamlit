
from pydantic import BaseModel, Field


class USInternationalAllocation(BaseModel):
    """US and international allocation in percentages."""
    us: int
    international: int


class RegionAllocation(BaseModel):
    """Region allocation in percentages."""
    north_america: int = Field(default=0, strict=False)
    eama: int = Field(default=0, strict=False)
    latam: int = Field(default=0, strict=False)
    apac: int = Field(default=0, strict=False)
    global_: int = Field(alias="global", default=100, strict=False)


class FundAssetAllocation(BaseModel):
    """Fund asset allocation in percentages."""
    stocks: int
    bonds: int
    real_estate: int
    cash: int


class MarketCapAllocation(BaseModel):
    """Market cap allocation in percentages."""
    large_cap: int = Field(strict=False)
    mid_cap: int = Field(strict=False)
    small_cap: int = Field(strict=False)


class GrowthValueAllocation(BaseModel):
    """Growth value allocation in percentages."""
    growth: int
    value: int


class EconomicStatusAllocation(BaseModel):
    """Economic status allocation in percentages."""
    developed: int
    emerging: int
    frontier: int


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
