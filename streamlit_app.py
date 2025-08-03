
import streamlit as st
import pandas as pd
from utils.value_assignment import assign_values

st.set_page_config(page_title="BLOC Draft Tool", layout="wide")

st.title("🏈 BLOC Fantasy Draft Tool")

uploaded_file = st.file_uploader("Upload Player Stats CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df = assign_values(df)
    st.dataframe(df)
    total_budget = 320
    st.sidebar.write(f"💰 Draft Budget: ${total_budget}")
