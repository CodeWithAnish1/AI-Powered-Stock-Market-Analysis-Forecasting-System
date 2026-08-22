# 📈 Stock Trading & Prediction App

A Streamlit-based stock analysis and prediction application that provides **historical stock data, technical indicators, and 30-day stock price forecasting**.

The application uses **Yahoo Finance** for stock market data and **ARIMA** for time-series forecasting.

---

## 🚀 Features

### 📊 Stock Analysis

- Search stocks using their ticker symbol
- View historical stock prices
- Interactive candlestick chart
- Line chart for Open, Close, High, and Low prices
- View daily price changes
- View High and Low prices
- Interactive date range slider

### 📈 Technical Indicators

The application provides the following technical indicators:

- **RSI (Relative Strength Index)**
- **MACD (Moving Average Convergence Divergence)**
- **50-Day Simple Moving Average (SMA)**

### 🔮 Stock Prediction

- Downloads historical stock data
- Calculates 7-day rolling mean
- Performs Augmented Dickey-Fuller (ADF) stationarity testing
- Determines the differencing order
- Scales the data using StandardScaler
- Trains an ARIMA model
- Evaluates the model using RMSE
- Predicts the next **30 days**
- Performs inverse scaling to convert predictions back to the original price scale
- Displays forecasted prices in a table
- Displays historical and predicted prices on an interactive chart

---

## 🛠️ Technologies Used

### Programming Language

- Python

### Libraries

- Streamlit
- Pandas
- NumPy
- yfinance
- Plotly
- pandas-ta
- Statsmodels
- Scikit-learn
- Python-dateutil

### Machine Learning / Time Series

- ARIMA
- ADF Test
- StandardScaler
- RMSE

---

## 📂 Project Structure

```text
Forecasting/
│
├── pages/
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── model_train.py
│   │   └── plotly_fig.py
│   │
│   ├── Stock_Analysis.py
│   └── Stock_Prediction.py
│
├── Trading_App.py
├── Trading image.png
├── Sources.txt
├── README.md
├── requirements.txt
└── .gitignore