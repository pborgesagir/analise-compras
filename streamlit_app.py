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

# Convert "DATA OC" column to date
df["DATA OC"] = pd.to_datetime(df["DATA OC"].astype(str), format='%d/%m/%Y às %H:%M', errors='coerce').dt.date

# Filter out rows where the date could not be parsed (NaT)
df = df.dropna(subset=["DATA OC"])

# Extract year, month, and quarter
df["Year"] = df["DATA OC"].dt.year
df["Month"] = df["DATA OC"].dt.month
df["Quarter"] = df["DATA OC"].dt.quarter
df["Semester"] = np.where(df["DATA OC"].dt.month.isin([1, 2, 3, 4, 5, 6]), 1, 2)

# Create a "Year-Quarter" column
df["Year-Quarter"] = df["Year"].astype(str) + "-T" + df["Quarter"].astype(str)

# If you want to create a "Year-Month" column, you can use the following line
df["Year-Month"] = df["DATA OC"].dt.strftime("%Y-%m")

# Create a "Year-Semester" column
df["Year-Semester"] = df["Year"].astype(str) + "-S" + df["Semester"].astype(str)

# Sort the unique values in ascending order
unique_year_month = sorted(df["Year-Month"].unique())
unique_year_quarter = sorted(df["Year-Quarter"].unique())
unique_year_semester = sorted(df["Year-Semester"].unique())
unique_year = sorted(df["Year"].unique())

# Add "All" as an option for both filters
unique_year_month.insert(0, "Todos")
unique_year_quarter.insert(0, "Todos")
unique_year_semester.insert(0, "Todos")
unique_year.insert(0, "Todos")

# Create a sidebar for selecting filters
month = st.sidebar.selectbox("Mês", unique_year_month)
quarter = st.sidebar.selectbox("Trimestre", unique_year_quarter)
semester = st.sidebar.selectbox("Semestre", unique_year_semester)
year = st.sidebar.selectbox("Ano", unique_year)

# Check if "All" is selected for the "Year-Month" filter
if month == "Todos":
    month_filtered = df
else:
    month_filtered = df[df["Year-Month"] == month]

# Check if "All" is selected for the "Year-Quarter" filter
if quarter == "Todos":
    filtered_df = month_filtered
else:
    filtered_df = month_filtered[month_filtered["Year-Quarter"] == quarter]

# Check if "All" is selected for the "Year-Semester" filter
if semester == "Todos":
    filtered_df = filtered_df
else:
    filtered_df = filtered_df[filtered_df["Year-Semester"] == semester]

# Check if "All" is selected for the "Year" filter
if year == "Todos":
    filtered_df = filtered_df
else:
    filtered_df = filtered_df[filtered_df["Year"] == year]

# Display the filtered DataFrame
st.write("Dados Selecionados:")
st.dataframe(filtered_df)
