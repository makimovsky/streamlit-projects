import yfinance as yf
import streamlit as st

st.write("""
# Simple stock price app
""")

ticker_smb = 'META'
ticker_data = yf.Ticker(ticker_smb)
ticker_df = ticker_data.history(period='1d', start='2015-01-01', end='2024-01-01')

st.write("""
## Closing Price
""")
st.line_chart(ticker_df['Close'])
st.write("""
## Volume
""")
st.line_chart(ticker_df['Volume'])
