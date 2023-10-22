import streamlit as st
from datasource.base import DataSource
from datasource.factory import data_source_factory, data_source_options, data_source_display_name

from portfolio.portfolio import Portfolio, PortfolioType


def setup_portfolio(portfolio_type: PortfolioType, source:str, input_file) -> Portfolio:
    ds: DataSource = data_source_factory(source, input_file)
    if ds.validate():
        portfolio: Portfolio = ds.get_portfolio()
        portfolio.set_portfolio_type(portfolio_type)
        return portfolio

def render_sidebar():
    with st.sidebar:
        st.session_state['openai_api_key'] = st.text_input("OpenAI API Key")

def render_data(portfolio: Portfolio):
    st.write(portfolio.df())

def render_page():
    st.title("Portfolio Optimization")

    portfolio_type = st.selectbox("Select your portfolio type", PortfolioType._member_names_)
    source = st.selectbox("Select your portfolio source", data_source_options(), format_func=data_source_display_name)
    uploaded_file = st.file_uploader("Upload your portfolio", type="csv")

    if uploaded_file is not None:
        portfolio: Portfolio = setup_portfolio(portfolio_type, source, uploaded_file)
        with st.spinner('File received. Looking up security data...'):
            render_data(portfolio)


if __name__ == "__main__":
    render_sidebar()
    render_page()
