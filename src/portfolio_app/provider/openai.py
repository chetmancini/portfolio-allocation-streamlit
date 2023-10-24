import os
from typing import Optional

import openai

from portfolio_app.portfolio.models import (
    EconomicStatusAllocation,
    FundAssetAllocation,
    GrowthValueAllocation,
    MarketCapAllocation,
    RegionAllocation,
    SectorAllocation,
    SecurityAllocation,
    SecurityInfo,
    SecurityType,
    USInternationalAllocation,
)
from portfolio_app.provider.base import AllocationDataClient


class OpenAIClient(AllocationDataClient):
    def __init__(self, api_key: Optional[str] = None):
        self.set_api_key(api_key or os.getenv("OPENAI_API_KEY", None))

    @classmethod
    def set_api_key(cls, api_key: str):
        if api_key and cls.validate_api_key(api_key):
            openai.api_key = api_key

    @classmethod
    def validate_api_key(cls, api_key: str) -> bool:
        return api_key.startswith("sk-")

    def _lookup_allocation_args(self, symbol: str):
        return {
            "model": "gpt-3.5-turbo-0613",
            "messages": [
                {
                    "role": "user",
                    "content": f"Give me an asset allocation breakdown for {symbol}. "
                    f"Give data as an integer percentage for the funds assets (stocks vs bonds). "
                    f"Give the market cap split by small/medium/large."
                    f"Give usa vs international, and for regions split out if possible, default 100 to global if there is insufficient data."
                    f"Finally provide growth vs value. If it's a blend use 50-50 for growth / value.",
                }
            ],
            "functions": [
                {
                    "name": "get_answer_for_user_query",
                    "description": "Get user answer in series of steps. "
                    "First the name, "
                    "then the fund asset allocation percentage of stocks and bonds (if it is a fund), "
                    "then the market cap weighting, "
                    "then percent us and international, the split by economic region (default to global), then if it's growth or value, "
                    "and finally the economic status breakdown of the portfolio's holdings "
                    "(developed, emerging, or frontier)",
                    "parameters": SecurityAllocation.model_json_schema(),
                }
            ],
            "function_call": {"name": "get_answer_for_user_query"},
        }

    def lookup_allocation(self, symbol: str):
        response = openai.ChatCompletion.create(**self._lookup_allocation_args(symbol))
        print(response)
        return SecurityAllocation.model_validate_json(
            response.choices[0]["message"]["function_call"]["arguments"]
        )

    async def lookup_allocation_async(self, symbol: str):
        response = await openai.ChatCompletion.acreate(
            **self._lookup_allocation_args(symbol)
        )
        return SecurityAllocation.model_validate_json(
            response.choices[0]["message"]["function_call"]["arguments"]
        )


class MockOpenAIClient(AllocationDataClient):
    def __init__(self) -> None:
        super().__init__()

    def lookup_allocation(self, symbol: str) -> SecurityAllocation:
        return SecurityAllocation(
            symbol=symbol,
            security_info=SecurityInfo(
                symbol=symbol,
                security_name=f"Mock Security: {symbol}",
                security_type=SecurityType.ETF,
                homepage_url="https://www.mock.com",
                expense_ratio=0.1,
            ),
            fund_asset_allocation=FundAssetAllocation(
                stocks=50,
                bonds=50,
            ),
            market_cap_allocation=MarketCapAllocation(
                small_cap=30,
                mid_cap=30,
                large_cap=40,
            ),
            us_international_allocation=USInternationalAllocation(
                us=50,
                international=50,
            ),
            region_allocation=RegionAllocation(
                north_america=100,
            ),
            growth_value_allocation=GrowthValueAllocation(
                growth=50,
                value=50,
            ),
            economic_status_allocation=EconomicStatusAllocation(
                developed=50,
                emerging=50,
            ),
            sector_allocation=SectorAllocation(
                information_technology=50,
                health_care=50,
            ),
        )
