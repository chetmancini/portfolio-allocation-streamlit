import streamlit as st

from src.portfolio import PortfolioType

st.title("Portfolio Optimization")

st.selectbox("Select your portfolio type", PortfolioType._member_names_)
st.selectbox("Select your portfolio source", ["E-Trade", "Other"])
uploaded_file = st.file_uploader("Upload your portfolio", type="csv")
if uploaded_file is not None:
    

st.write("This is a streamlit ")

st.sidebar.title("Sidebar")