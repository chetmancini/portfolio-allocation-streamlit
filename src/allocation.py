from pydantic import BaseModel
from typing import Dict

from src.openai import OpenAIClient


class USInternationalAllocation(BaseModel):
    us: int
    international: int


class RegionAllocation(BaseModel):
    north_america: int
    eama: int
    latam: int
    apac: int
    global_: int


class FundAssetAllocation(BaseModel):
    stocks: int
    bonds: int
    real_estate: int
    cash: int


class MarketCapAllocation(BaseModel):
    large_cap: int
    mid_cap: int
    small_cap: int


class GrowthValueAllocation(BaseModel):
    growth: int
    value: int


class EconomicStatusAllocation(BaseModel):
    developed: int
    emerging: int
    frontier: int


class SecurityAllocation(BaseModel):
    symbol: str
    security_name: str

    fund_asset_allocation: FundAssetAllocation
    market_cap_allocation: MarketCapAllocation
    us_international_allocation: USInternationalAllocation
    region_allocation: RegionAllocation
    growth_value_allocation: GrowthValueAllocation
    economic_status_allocation: EconomicStatusAllocation



class AllocationLookupService:

    def __init__(self):
        self.cache: Dict[str, SecurityAllocation] = {}
        self.openai_client = OpenAIClient()

    def get_allocations_by_symbol(self, symbol: str) -> SecurityAllocation:
        if symbol in self.cache:
            return self.cache[symbol]

        response = self.openai_client.lookup_allocation(symbol=symbol)
        self.cache[symbol] = response
        return response
