import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


st.set_page_config(layout="wide")
url = "https://docs.google.com/spreadsheets/d/1DqyHkjSP-ykf1FqQp7R2FSbuUIGyIRgpad9J9WDKXck"
st.title("DASHBOARD - PADRONIZAÇÃO AGIR")
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(spreadsheet=url, usecols=list(range(34)))
df = df.drop_duplicates()

# Convert "DATA OC" column to datetime
df["DATA OC"] = pd.to_datetime(df["DATA OC"], format='%d/%m/%Y', errors='coerce')

st.dataframe(df)
