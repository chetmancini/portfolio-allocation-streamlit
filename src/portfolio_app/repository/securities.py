import os
from typing import Iterable, Optional, Tuple
from supabase import create_client, Client
import supabase
from portfolio_app.portfolio.models import SecurityAllocation
from portfolio_app.provider.base import AllocationDataClient
from portfolio_app.provider.openai import OpenAIClient


class SecurityDataRepository:
    """
    Single data repository for securities and all related market data.
    """

    def __init__(
        self,
        allocation_client: Optional[AllocationDataClient] = None,
        supabase_client: Optional[Client] = None,
    ) -> None:
        if supabase_client:
            self.supabase = supabase_client
        else:
            url: str = os.environ.get("SUPABASE_URL")
            key: str = os.environ.get("SUPABASE_KEY")
            self.supabase: Client = create_client(url, key)
        if allocation_client:
            self.allocation_client = allocation_client
        else:
            self.allocation_client = OpenAIClient()

    def get_many_securities(
        self, symbols: Iterable[str]
    ) -> Iterable[SecurityAllocation]:
        pass

    def _supabase_contains(self, symbol: str) -> bool:
        """
        Check if Supabase contains the symbol
        """
        data, count = (
            supabase.table("securities")
            .select("symbol, modified_at")
            .eq("symbol", symbol)
            .execute()
        )
        if data and data[0]["symbol"]:
            return True
        return False

    def _supabase_get(self, symbol: str) -> Optional[SecurityAllocation]:
        """
        Get a security from Supabase if it exists
        """
        data, count = (
            supabase.table("securities")
            .select("*, security_allocation_info(*), security_fund_info(*)")
            .eq("securities.symbol", symbol)
            .execute()
        )
        print(data)
        return None

    def _supabase_add(self, security_allocation: SecurityAllocation) -> None:
        """
        Add a security to Supabase
        """
        # data, count = supabase.table('securities').insert({"name": "Denmark"}).execute()
        pass

    def get_single_security_by_symbol(self, symbol: str) -> SecurityAllocation:
        data, count = (
            supabase.table("securities").insert({"id": 1, "name": "Denmark"}).execute()
        )
        pass

    def get_last_price_by_symbol(self, symbol: str) -> float:
        pass

    def get_last_prices_by_symbols(
        self, symbols: Iterable[str]
    ) -> Iterable[Tuple[str, float]]:
        pass
