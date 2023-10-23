import os
import sys
from pandas import DataFrame
import streamlit as st
from portfolio_app.charts import ChartManager

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)
from portfolio_app.datasource.base import DataSource  # noqa: E402
from portfolio_app.datasource.factory import (  # noqa: E402
    data_source_factory,
    data_source_options,
    data_source_display_name,
)  # noqa: E402
from portfolio_app.portfolio.portfolio import Portfolio, PortfolioType  # noqa: E402


def setup_portfolio(
    portfolio_type: PortfolioType, source: str, input_file
) -> Portfolio:
    ds: DataSource = data_source_factory(source, input_file)
    if ds.validate():
        portfolio: Portfolio = ds.get_portfolio()
        portfolio.set_portfolio_type(portfolio_type)
        return portfolio


def render_sidebar():
    with st.sidebar:
        st.session_state["openai_api_key"] = st.text_input("OpenAI API Key")


def render_data(portfolio: Portfolio):
    st.write(portfolio.df())
    st.write(portfolio.allocation_df())

    st.write("Region Allocation")
    us_intl_allocation: DataFrame = portfolio.get_us_international_df()
    st.bar_chart(us_intl_allocation, y="Total Value")
    st.altair_chart(
        ChartManager.get_pie_chart(us_intl_allocation), use_container_width=True
    )
    st.write(us_intl_allocation)

    # region_allocation: DataFrame = portfolio.get_region_df()
    # st.bar_chart(region_allocation, y="Total Value")
    # st.write(region_allocation)

    economic_allocation: DataFrame = portfolio.get_economic_status_df()
    st.bar_chart(economic_allocation, y="Total Value")
    st.altair_chart(
        ChartManager.get_pie_chart(economic_allocation), use_container_width=True
    )
    st.write(economic_allocation)

    growth_value_df: DataFrame = portfolio.get_growth_value_df()
    st.bar_chart(us_intl_allocation, y="Total Value")
    st.altair_chart(
        ChartManager.get_pie_chart(growth_value_df), use_container_width=True
    )
    st.write(growth_value_df)

    market_cap_df: DataFrame = portfolio.get_market_cap_df()
    st.bar_chart(market_cap_df, y="Total Value")
    st.altair_chart(
        ChartManager.get_pie_chart(market_cap_df), use_container_width=True
    )
    st.write(market_cap_df)

    sector_df: DataFrame = portfolio.get_sector_df()
    st.bar_chart(sector_df, y="Total Value")
    st.altair_chart(
        ChartManager.get_pie_chart(sector_df), use_container_width=True
    )
    st.write(sector_df)

    st.write(f"Total Expense Ratio: {portfolio.get_total_expense_ratio()}")
    st.write(f"Total Portfolio Value: {portfolio.total_value()}")


def render_page():
    st.title("Portfolio Optimization")

    portfolio_type = st.selectbox(
        "Select your portfolio type", PortfolioType._member_names_
    )
    source = st.selectbox(
        "Select your portfolio source",
        data_source_options(),
        format_func=data_source_display_name,
    )
    uploaded_file = st.file_uploader("Upload your portfolio", type="csv")

    if uploaded_file is not None:
        portfolio: Portfolio = setup_portfolio(portfolio_type, source, uploaded_file)
        with st.spinner("File received. Looking up security data..."):
            render_data(portfolio)


if __name__ == "__main__":
    render_sidebar()
    render_page()
