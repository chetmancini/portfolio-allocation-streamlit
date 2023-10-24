from enum import Enum
from typing import List, Tuple
from pydantic import BaseModel, ConfigDict, Field


class SecurityType(str, Enum):
    STOCK = "Stock"
    OPTION = "Option"
    BOND = "Bond"
    ETF = "ETF"
    REIT = "REIT"
    MUTUAL_FUND = "Mutual Fund"
    OTHER = "Other"


class BaseAllocationModel(BaseModel):
    """Base allocation model."""

    @classmethod
    def prefix(cls):
        return ""

    def to_dict(self):
        return {f"{self.prefix()}_{f}_pct": getattr(self, f) for f in self.model_fields}

    @classmethod
    def keys_labels(cls) -> Tuple[List[str], List[str]]:
        return (
            [f"{cls.prefix()}_{f}_pct" for f in cls.model_fields],
            [f.title for f in cls.model_fields.values()],
        )


class USInternationalAllocation(BaseAllocationModel):
    """US and international allocation in percentages."""

    us: int = Field(title="US", default=0, strict=False)
    international: int = Field(title="International", default=0, strict=False)

    @classmethod
    def prefix(cls):
        return "intl"


class RegionAllocation(BaseAllocationModel):
    """Region allocation in percentages."""

    north_america: int = Field(title="North America", default=0, strict=False)
    emea: int = Field(title="Europe, Middle East, Africa", default=0, strict=False)
    latam: int = Field(title="Latin America", default=0, strict=False)
    apac: int = Field(title="Asia/Pacific", default=0, strict=False)
    global_: int = Field(title="Global", alias="global_", default=100, strict=False)

    @classmethod
    def prefix(cls):
        return "region"


class FundAssetAllocation(BaseAllocationModel):
    """Fund asset allocation in percentages."""

    stocks: int = Field(title="Stocks", default=0, strict=False)
    bonds: int = Field(title="Bonds", default=0, strict=False)
    real_estate: int = Field(title="Real Estate", default=0, strict=False)
    cash: int = Field(title="Cash", default=0, strict=False)

    @classmethod
    def prefix(cls):
        return "asset_type"


class MarketCapAllocation(BaseAllocationModel):
    """Market cap allocation in percentages."""

    large_cap: int = Field(title="Large Cap", strict=False)
    mid_cap: int = Field(title="Mid Cap", strict=False)
    small_cap: int = Field(title="Small Cap", strict=False)

    @classmethod
    def prefix(cls):
        return "marketcap"


class GrowthValueAllocation(BaseAllocationModel):
    """Growth value allocation in percentages."""

    growth: int = Field(title="Growth", default=0, strict=False)
    value: int = Field(title="Value", default=0, strict=False)

    @classmethod
    def prefix(cls):
        return "strategy"


class EconomicStatusAllocation(BaseAllocationModel):
    """Economic status allocation in percentages."""

    developed: int = Field(title="Developed Markets", default=0, strict=False)
    emerging: int = Field(title="Emerging Markets", default=0, strict=False)
    frontier: int = Field(title="Frontier Markets", default=0, strict=False)

    @classmethod
    def prefix(cls):
        return "econ_status"


class SectorAllocation(BaseAllocationModel):
    """Sector allocation in percentages."""

    information_technology: int = Field(
        title="Information Technology", default=0, strict=False
    )
    health_care: int = Field(title="Health Care", default=0, strict=False)
    financials: int = Field(title="Financials", default=0, strict=False)
    consumer_discretionary: int = Field(
        title="Consumer Discretionary", default=0, strict=False
    )
    communication_services: int = Field(
        title="Communication Services", default=0, strict=False
    )
    industrials: int = Field(title="Industrials", default=0, strict=False)
    consumer_staples: int = Field(title="Consumer Staples", default=0, strict=False)
    energy: int = Field(title="Energy", default=0, strict=False)
    utilities: int = Field(title="Utilities", default=0, strict=False)
    real_estate: int = Field(title="Real Estate", default=0, strict=False)
    materials: int = Field(title="Materials", default=0, strict=False)

    @classmethod
    def prefix(cls):
        return "sector"


class SecurityInfo(BaseModel):
    """Security information."""

    model_config = ConfigDict(use_enum_values=True)

    symbol: str = Field(
        title="Symbol",
        description="Ticker symbol",
        strict=True,
    )
    security_name: str = Field(
        title="Security Name",
        description="Security name",
        strict=True,
    )
    security_type: SecurityType = Field(
        title="Security Type",
        description="Security type",
        default="",
    )
    homepage_url: str = Field(
        title="Homepage URL",
        description="Homepage URL",
        default="",
        strict=False,
    )
    expense_ratio: float = Field(
        title="Expense Ratio",
        description="Expense ratio",
        default=0.0,
        strict=False,
    )

    def to_dict(self):
        return {
            "symbol": self.symbol,
            "security_name": self.security_name,
            "security_type": self.security_type,
            "homepage_url": self.homepage_url,
            "expense_ratio": self.expense_ratio,
        }


class SecurityAllocation(BaseModel):
    """Security allocation in percentages."""

    symbol: str = Field(
        title="Symbol",
        description="Ticker symbol",
        strict=True,
    )
    security_info: SecurityInfo
    fund_asset_allocation: FundAssetAllocation
    market_cap_allocation: MarketCapAllocation
    us_international_allocation: USInternationalAllocation
    region_allocation: RegionAllocation
    growth_value_allocation: GrowthValueAllocation
    economic_status_allocation: EconomicStatusAllocation
    sector_allocation: SectorAllocation

    def to_dict(self):
        ret = {
            "symbol": self.symbol,
        }
        ret.update(self.security_info.to_dict())
        ret.update(self.fund_asset_allocation.to_dict())
        ret.update(self.market_cap_allocation.to_dict())
        ret.update(self.us_international_allocation.to_dict())
        ret.update(self.region_allocation.to_dict())
        ret.update(self.growth_value_allocation.to_dict())
        ret.update(self.economic_status_allocation.to_dict())
        ret.update(self.sector_allocation.to_dict())
        return ret
