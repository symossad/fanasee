import streamlit as st
import pandas as pd
from utils.value_assignment import assign_values

st.set_page_config(page_title="BLOC Draft Tool", layout="wide")
st.title("🏈 BLOC Fantasy Draft Tool")

uploaded_file = st.file_uploader("Upload Player Stats CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df = assign_values(df)
    
    st.markdown("### Player Values")
    st.dataframe(df.sort_values(by="auto_dollar_value", ascending=False), use_container_width=True)
    
    st.sidebar.markdown("## 💰 Draft Budget")
    total_budget = 320
    st.sidebar.metric(label="Total Draft Budget", value=f"${total_budget}")
else:
    st.info("Upload a CSV to begin.")
