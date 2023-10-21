import streamlit as st
from datasource.base import DataSource
from datasource.factory import data_source_factory

from portfolio import Portfolio, PortfolioType


def setup_portfolio(portfolio_type: PortfolioType, source:str, input_file) -> Portfolio:
    ds: DataSource = data_source_factory(source, input_file)
    if ds.validate():
        portfolio: Portfolio = ds.get_portfolio()
        portfolio.set_portfolio_type(portfolio_type)
        return portfolio


def render_page():
    st.title("Portfolio Optimization")

    portfolio_type = st.selectbox("Select your portfolio type", PortfolioType._member_names_)
    source = st.selectbox("Select your portfolio source", ["etrade-csv", "other"])
    uploaded_file = st.file_uploader("Upload your portfolio", type="csv")

    if uploaded_file is not None:
        portfolio: Portfolio = setup_portfolio(portfolio_type, source, uploaded_file)
    
        st.write(portfolio.df())

    st.write("This is a streamlit ")


if __name__ == "__main__":
    render_page()
