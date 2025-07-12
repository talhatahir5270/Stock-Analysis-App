import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from datetime import datetime

st.set_page_config(page_title="📈 Stock Analyzer", layout="wide")
st.title("📊 Stock Price Analysis App")

# Sidebar for user inputs
st.sidebar.header("Stock Configuration")

# Input: Stock Symbol
stock = st.sidebar.text_input("Enter Stock Symbol (e.g. AAPL, MSFT, GOOGL)", "AAPL")

# Input: Date Range
start_date = st.sidebar.date_input("Start Date", datetime(2020, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime.today())

# Fetch stock data using yfinance
try:
    df = yf.download(stock, start=start_date, end=end_date)
    if df.empty:
        st.error("No data found. Check the stock symbol.")
        st.stop()
    st.success(f"Showing data for {stock} from {start_date} to {end_date}")
except Exception as e:
    st.error(f"Failed to load data: {e}")
    st.stop()

# Show data
st.subheader(f"Raw Data for {stock}")
st.dataframe(df.tail())

# Plotting
st.subheader("📈 Closing Price Over Time")
st.line_chart(df["Close"])

# Moving Average
st.subheader("📊 Moving Averages")
ma1 = st.sidebar.slider("Short-term MA (days)", 5, 50, 20)
ma2 = st.sidebar.slider("Long-term MA (days)", 10, 200, 50)

df["MA1"] = df["Close"].rolling(ma1).mean()
df["MA2"] = df["Close"].rolling(ma2).mean()

fig, ax = plt.subplots()
df["Close"].plot(ax=ax, label="Close Price", linewidth=1)
df["MA1"].plot(ax=ax, label=f"{ma1}-Day MA", linestyle="--")
df["MA2"].plot(ax=ax, label=f"{ma2}-Day MA", linestyle="--")
ax.set_ylabel("Price ($)")
ax.set_title(f"{stock} Price with Moving Averages")
ax.legend()
st.pyplot(fig)

# Volume Chart
st.subheader("📉 Trading Volume")
st.bar_chart(df["Volume"])

# Correlation Heatmap
st.subheader("🧠 Feature Correlation Heatmap")
fig2, ax2 = plt.subplots()
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", fmt=".2f", ax=ax2)
st.pyplot(fig2)
