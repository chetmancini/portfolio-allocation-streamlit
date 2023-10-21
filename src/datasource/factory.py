from typing import Optional
from datasource.base import DataSource
from datasource.etrade import ETradeCSVDataSource


DATA_SOURCES = {
    "etrade-csv": ETradeCSVDataSource,
}


def data_source_factory(source_type: Optional[str], input_file) -> DataSource:
    if source_type:
        return DATA_SOURCES[source_type](input_file)
