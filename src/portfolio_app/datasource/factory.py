from enum import Enum
from typing import List, Optional
from portfolio_app.datasource.base import DataSource
from portfolio_app.datasource.etrade import ETradeCSVDataSource


class DataSourceType(Enum):
    ETRADE_CSV = "etrade-csv"

    def display_name(self):
        if self == DataSourceType.ETRADE_CSV:
            return "E*Trade Account: CSV File"


DATA_SOURCES = {
    DataSourceType.ETRADE_CSV: ETradeCSVDataSource,
}


def data_source_options() -> List[str]:
    return [source_type.value for source_type in DataSourceType]


def data_source_display_name(data_source_type: str) -> str:
    return DataSourceType(data_source_type).display_name()


def data_source_factory(source_type_str: Optional[str], input_file) -> DataSource:
    if source_type_str:
        return DATA_SOURCES[DataSourceType(source_type_str)](input_file)
