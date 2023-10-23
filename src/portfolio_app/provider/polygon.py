from datetime import date
from typing import Tuple
import requests
from portfolio_app.provider.base import LastPriceProviderClient


class PolygonClient(LastPriceProviderClient):
    API_ROOT = "https://api.polygon.io/v2"

    def __init__(self, polygon_api_key=None) -> None:
        self.polygon_api_key = polygon_api_key

    def _as_of_date(unix_ts_ms: int) -> date:
        return date.fromtimestamp(unix_ts_ms / 1000)

    def last_price(self, symbol: str) -> Tuple[date, float]:
        """
        https://polygon.io/docs/stocks/get_v2_aggs_ticker__stocksticker__prev
        """
        res = requests.get(
            f"{self.API_ROOT}/aggs/ticker/{symbol}/prev?adjusted=true&apiKey={self.polygon_api_key}"
        ).json()
        if res["status"] != "OK":
            raise Exception(f"Failed to get last price for {symbol}")
        return self._as_of_date(res["results"][0]["t"]), res["results"][0]["c"]
