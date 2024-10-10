import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np


@st.cache_data
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header=0)
    scrapped_df = html[0]
    return scrapped_df


# app title
st.header("""SP500 Stock Price App
***
""")

# data source
st.write("""
**Data source**: [Wikipedia](https://www.wikipedia.org/)
***
""")

# loading data
df = load_data()
sector = df.groupby('GICS Sector')

# sidebar header
st.sidebar.header('User Input Features')

# sidebar sector selection
sector_unique = sorted(df['GICS Sector'].unique())
selected_sector = st.sidebar.multiselect('Sector', sector_unique, sector_unique)

# display selected companies data
df_selected_sector = df[df['GICS Sector'].isin(selected_sector)]

st.header('Companies in selected sector(s)')
st.write('Data dimension: ' + str(df_selected_sector.shape[0]) + ' rows and ' + str(df_selected_sector.shape[1])
         + ' columns')
st.write(df_selected_sector)

# display selected sectors on market
log_ret = pd.DataFrame()
st.header('Sector(s) on stock market (past year)')
for sector in selected_sector:
    symbols = df_selected_sector[df_selected_sector['GICS Sector'] == sector]['Symbol'].tolist()
    data = yf.download(symbols, period='1y')['Close'].fillna(1)
    log_ret[sector] = np.log(data / data.shift(1)).cumsum().mean(axis=1)

st.line_chart(log_ret)
