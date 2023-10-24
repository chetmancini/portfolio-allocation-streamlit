import os
from typing import Iterable, Tuple
from supabase import create_client, Client
import supabase
from portfolio_app.portfolio.models import SecurityAllocation


class SecurityDataRepository:
    def __init__(self) -> None:
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        self.supabase: Client = create_client(url, key)

    def get_many_securities(
        self, symbols: Iterable[str]
    ) -> Iterable[SecurityAllocation]:
        pass

    def _supabase_contains(self, symbol: str) -> bool:
        """
        Check if Supabase contains the symbol
        """
        data, count = (
            supabase.table("securities").select("symbol, modified_at").execute()
        )
        if data and data[0]["symbol"]:
            return True
        return False

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
