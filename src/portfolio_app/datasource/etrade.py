import csv
from io import StringIO
import pandas as pd
from portfolio_app.portfolio.portfolio import Portfolio, SecurityHolding
from portfolio_app.datasource.base import DataSource


class ETradeCSVDataSource(DataSource):
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.temp_cash = 0.0

    def validate(self) -> bool:
        with StringIO(self.csv_file.getvalue().decode("utf-8")) as sio:
            first_line = sio.readline()
            return first_line.startswith("Account Summary")

    def _handle_cash(self, bad_line: list[str]) -> None:
        if bad_line[0] == "CASH":
            self.temp_cash = float(next(s for s in bad_line[1:] if s))
        return None

    def get_data_df(self):
        return pd.read_csv(
            self.csv_file,
            skiprows=10,
            skipfooter=4,
            engine="python",
            on_bad_lines=self._handle_cash,
        )

    def get_portfolio_name(self):
        with StringIO(self.csv_file.getvalue().decode("utf-8")) as sio:
            reader = csv.reader(sio)
            next(reader)
            next(reader)  # total headers
            total_values = next(reader)
            self.csv_file.seek(0)
            return total_values[0]

    def get_portfolio(self) -> Portfolio:
        portfolio = Portfolio(portfolio_source="E*Trade CSV")
        df = self.get_data_df()
        for index, row in df.iterrows():
            if row["Symbol"] == "CASH":
                continue
            security = SecurityHolding()
            security.symbol = row["Symbol"]
            security.name = None
            security.quantity = float(row["Quantity"])
            security.last_price = float(row["Last Price $"])
            security.avg_price_paid = float(row["Price Paid $"])
            security.total_value = float(row["Value $"])
            portfolio.add_security(security)

        portfolio.set_cash(self.temp_cash)
        portfolio.set_account_name(self.get_portfolio_name())

        return portfolio
