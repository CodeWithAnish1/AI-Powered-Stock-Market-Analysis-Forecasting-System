import streamlit as st
import pandas as pd
import yfinance as yf 
import plotly.graph_objects as go 
import datetime
import ta
from pages.utils.plotly_fig import plotly_table
from pages.utils.plotly_fig import plotly_table1
from pages.utils.plotly_fig import close_chart
from pages.utils.plotly_fig import candlestick
from pages.utils.plotly_fig import RSI
from pages.utils.plotly_fig import Moving_average
from pages.utils.plotly_fig import MACD



# setting page config
st.set_page_config(
    page_title="Stock Analysis",
    page_icon="page_with_curl",
    layout="wide",
)

# Stock analysis from 1 year back to now.
st.title("Stock Analysis")

col1, col2, col3 = st.columns(3)

today = datetime.date.today()

with col1:
    ticker = st.text_input("Stock Ticker", "TSLA")

with col2:
    start_date = st.date_input("Choose Start Date",datetime.date(today.year - 1, today.month, today.day))

with col3:
    end_date = st.date_input("Choose End Date",datetime.date(today.year, today.month, today.day))


# Display ticker as a subheading (Means whatever the ticker is shows as a subheading)
st.subheader(ticker)  

stock = yf.Ticker(ticker)

# Display company information

st.write("**Long Business Summary:**", stock.info["longBusinessSummary"])
st.write("**Sector:**", stock.info["sector"])
st.write("**Website:**", stock.info["website"])
st.write("**Full Time Employees:**", stock.info["fullTimeEmployees"])


col1, col2 = st.columns(2)

with col1:  
    df = pd.DataFrame(index=['Market Cap', 'Beta', 'EPS', 'PE Ratio'])   #Col name is index
    df[''] = [stock.info["marketCap"], stock.info["beta"], stock.info["trailingEps"], stock.info["trailingPE"]]   # Column name is empty string
    fig_df = plotly_table(df)
    st.plotly_chart(fig_df, use_container_width=True)

with col2:
    df = pd.DataFrame(index=['Quick Ratio', 'Revenue per share', 'Profit Margins','Return on Equity'])
    df[''] = [stock.info["quickRatio"], stock.info["revenuePerShare"],stock.info["profitMargins"],stock.info["returnOnEquity"]]
    fig_df = plotly_table(df)
    st.plotly_chart(fig_df, use_container_width=True)



data = yf.download(ticker,start=start_date,end=end_date)
col1, col2, col3 = st.columns(3)    # it gives one row with 3 equal width column

# Daily change 
daily_change = data['Close'].iloc[-1].item() - data['Close'].iloc[-2].item()
with col1:
    col1.metric("**Daily Change**", str(round(data['Close'].iloc[-1].item(), 2)), str(round(daily_change, 2)))
with col2:
    st.metric("High", round(data['High'].iloc[-1], 2))
with col3:
    st.metric("Low", round(data['Low'].iloc[-1], 2))

# Last 10 days table data
last_10_df = data.tail(10).sort_index(ascending=False).round(3)
fig_df = plotly_table1(last_10_df)
st.write('##### Historical Data (Last 10 days)')
st.plotly_chart(fig_df, use_container_width=True)


# Period buttons:-
col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12 = st.columns([1,1,1,1,1,1,1,1,1,1,1,1])

num_period = ''

with col1:
    if st.button('5D'):
        num_period = '5d'

with col2:
    if st.button('1M'):
        num_period = '1mo'

with col3:
    if st.button('6M'):
        num_period = '6mo'

with col4:
    if st.button('YTD'):
        num_period = 'ytd'

with col5:
    if st.button('1Y'):
        num_period = '1y'

with col6:
    if st.button('5Y'):
        num_period = '5y'

with col7:
    if st.button('MAX'):
        num_period = 'max'



# Chart type 
col1, col2, col3 = st.columns([1,1,4])

with col1:
    chart_type = st.selectbox('', ('Candle', 'Line'))

with col2:
    if chart_type == 'Candle':
        indicators = st.selectbox('', ('RSI', 'MACD'))    # label and option #    #label="" -> it can any value to show
    else:
        indicators = st.selectbox('', ('RSI', 'Moving Average', 'MACD'))




# Chart return :-

ticker_ = yf.Ticker(ticker)
new_df1 = ticker_.history(period='max')    #Maxm amount of historical data available.
data1 = ticker_.history(period='max')

if num_period == '':

    if chart_type == 'Candle' and indicators == 'RSI':
        st.plotly_chart(candlestick(data1, '1y'), use_container_width=True)
        st.plotly_chart(RSI(data1, '1y'), use_container_width=True)

    if chart_type == 'Candle' and indicators == 'MACD':
        st.plotly_chart(candlestick(data1, '1y'), use_container_width=True)
        st.plotly_chart(MACD(data1, '1y'), use_container_width=True)

    if chart_type == 'Line' and indicators == 'RSI':
        st.plotly_chart(close_chart(data1, '1y'), use_container_width=True)
        st.plotly_chart(RSI(data1, '1y'), use_container_width=True)

    if chart_type == 'Line' and indicators == 'Moving Average':
        st.plotly_chart(Moving_average(data1, '1y'), use_container_width=True)

    if chart_type == 'Line' and indicators == 'MACD':
        st.plotly_chart(close_chart(data1, '1y'), use_container_width=True)   # close chart is a line chart
        st.plotly_chart(MACD(data1, '1y'), use_container_width=True)

else:

    if chart_type == 'Candle' and indicators == 'RSI':
        st.plotly_chart(candlestick(new_df1, num_period), use_container_width=True)
        st.plotly_chart(RSI(new_df1, num_period), use_container_width=True)

    if chart_type == 'Candle' and indicators == 'MACD':
        st.plotly_chart(candlestick(new_df1, num_period), use_container_width=True)
        st.plotly_chart(MACD(new_df1, num_period), use_container_width=True)

    if chart_type == 'Line' and indicators == 'RSI':
        st.plotly_chart(close_chart(new_df1, num_period), use_container_width=True)
        st.plotly_chart(RSI(new_df1, num_period), use_container_width=True)

    if chart_type == 'Line' and indicators == 'Moving Average':
        st.plotly_chart(Moving_average(new_df1, num_period), use_container_width=True)

    if chart_type == 'Line' and indicators == 'MACD':
        st.plotly_chart(close_chart(new_df1, num_period), use_container_width=True)
        st.plotly_chart(MACD(new_df1, num_period), use_container_width=True)