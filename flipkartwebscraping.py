import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
import datetime

# Title of the web app
st.title('Indian Stock Market Trends Analysis')

# Input for stock ticker symbol
stock_ticker = st.text_input('Enter stock symbol (e.g., TCS.NS):')

if stock_ticker:
    # Fetching historical data using yfinance
    stock_data = yf.download(stock_ticker, start='2010-01-01', end=datetime.date.today())

    if not stock_data.empty:
        # Plotting the closing price
        fig = px.line(stock_data, x=stock_data.index, y='Close', title='Closing Price Trend')
        st.plotly_chart(fig)

        # Displaying the raw data
        show_raw_data = st.checkbox('Show raw data')
        if show_raw_data:
            st.subheader('Raw Data')
            st.write(stock_data)

        # Moving average analysis
        ma_period = st.slider('Moving Average Period', min_value=10, max_value=200, value=50, step=10)
        stock_data['MA'] = stock_data['Close'].rolling(window=ma_period).mean()

        fig_ma = px.line(stock_data, x=stock_data.index, y=['Close', 'MA'], title='Closing Price with Moving Average')
        fig_ma.update_traces(line=dict(width=1.2))
        st.plotly_chart(fig_ma)

        # Daily returns analysis
        stock_data['Returns'] = stock_data['Close'].pct_change() * 100

        fig_returns = px.histogram(stock_data, x='Returns', nbins=50, title='Daily Returns Histogram')
        st.plotly_chart(fig_returns)

        # Volatility analysis
        volatility = stock_data['Returns'].std()
        st.subheader('Volatility')
        st.write('Annualized Volatility:', volatility * (252 ** 0.5))  # Assuming 252 trading days in a year

        # Recent data analysis
        st.subheader('Recent Data')
        recent_data = stock_data.tail(10)
        st.write(recent_data)

        # Closing price statistics
        st.subheader('Closing Price Statistics')
        st.write('Mean:', stock_data['Close'].mean())
        st.write('Standard Deviation:', stock_data['Close'].std())
        st.write('Minimum:', stock_data['Close'].min())
        st.write('Maximum:', stock_data['Close'].max())

        # Volume statistics
        st.subheader('Volume Statistics')
        st.write('Mean Volume:', stock_data['Volume'].mean())
        st.write('Standard Deviation Volume:', stock_data['Volume'].std())
        st.write('Minimum Volume:', stock_data['Volume'].min())
        st.write('Maximum Volume:', stock_data['Volume'].max())
        
        # Add developer information and LinkedIn link to the footer
        st.sidebar.markdown("Developed by [Vikash Goyal](https://www.linkedin.com/in/vikash-goyal-20692924b)")
