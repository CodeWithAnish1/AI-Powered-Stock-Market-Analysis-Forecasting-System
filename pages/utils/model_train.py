# 1. get data 
# 2. stationary check -> by ADF test
# 3. smooth the data -> by rolling mean
# 4. get diffencing order -> by checking stationary
# 5. Scaling the data -> by standard scaller -> scaling down the numerical value
# 6. evaluate model -> by RMSE(root mean squared error)
# 7. fit the model and predict the value for one day
# 8. get a forecast dataframe
# 9. Inverse scaling -> convert the data in an actual manner


import yfinance as yf
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import pandas as pd


def get_data(ticker):
    stock_data = yf.download(ticker, start='2025-01-01')    # start download from this date
    close_price = stock_data['Close'].squeeze()
    close_price.name = 'Close'
    return close_price


def stationary_check(close_price):
    adf_test = adfuller(close_price)
    p_value = round(adf_test[1], 3)                          # Adf test gives -> ADF stat   p-value   lags used   observations
    return p_value


def get_rolling_mean(close_price):                                     
    rolling_price = close_price.rolling(window=7).mean().dropna()     # There is NA rolling mean -> drop it
    rolling_price.name = 'Close'
    return rolling_price

def get_differencing_order(close_price):

    p_value=stationary_check(close_price)
    d=0
    while True:
        if p_value > 0.05:
           d+=1
           close_price=close_price.diff().dropna()
           p_value = stationary_check(close_price)
        else:
            break
    return d



def fit_model(data, differencing_order):
    model = ARIMA(data, order=(30, differencing_order, 30))              # p= 30 past values , q= 30 past error terms
    model_fit = model.fit()

    forecast_steps = 30                                                  # predict for 30 days
    forecast = model_fit.get_forecast(steps=forecast_steps)              # forecast.prediction_mean = values

    predictions = forecast.predicted_mean                                # not means mean -> it find only values without name
    return predictions                                                   # it is in the column format but only values


def evaluate_model(original_price, differencing_order):
    train_data, test_data = original_price[:-30], original_price[-30:]   # train data = Take everything except the last 30 values.
    predictions = fit_model(train_data, differencing_order)

    rmse = np.sqrt(mean_squared_error(test_data, predictions))
    return round(rmse, 2)


def scaling(close_price):
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(
        np.array(close_price).reshape(-1, 1)                                      # changes to 1 column
    )
    return scaled_data, scaler

def get_forecast(original_price, differencing_order):                                        # make a forecast dataframe
    predictions = fit_model(original_price, differencing_order)
    start_date = datetime.now().strftime('%Y-%m-%d')                                         # date of now
    end_date = (datetime.now() + timedelta(days=29)).strftime('%Y-%m-%d')                    # date ater 30 days
    forecast_index = pd.date_range(start=start_date, end=end_date, freq='D')                 # it make the index start to end with 1 freq can say D
    forecast_df = pd.DataFrame(predictions, index=forecast_index, columns=['Close'])         # fill Close columns with predictions
    return forecast_df


def inverse_scaling(scaler, scaled_data):                                  
    close_price = scaler.inverse_transform(
        np.array(scaled_data).reshape(-1, 1)
    )
    return close_price