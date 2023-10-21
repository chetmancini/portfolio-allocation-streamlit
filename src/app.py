import streamlit as st

st.title("Portfolio Optimization")


st.file_uploader("Upload your portfolio", type="csv")

st.form_submit_button("Submit")

st.write("This is a streamlit ")

st.sidebar.title("Sidebar")