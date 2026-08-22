import streamlit as st
from pages.utils.model_train import get_data, get_rolling_mean, get_differencing_order, scaling, evaluate_model,get_forecast,inverse_scaling
import pandas as pd
from pages.utils.plotly_fig import plotly_table1, Moving_average_forecast

# set page config
st.set_page_config(
    page_title="Stock Prediction",
    page_icon=":chart_with_downwards_trend:",
    layout="wide",
)

# page
st.title("Stock Prediction")

col1, col2, col3 = st.columns(3)                                    # why making col2 and col3 -> to organize on the side not use of this 

with col1:
    ticker = st.text_input('Stock Ticker', 'AAPL')

rmse = 0

st.subheader('Predicting Next 30 days Close Price for:- ' + ticker)



# checking rmse value 
close_price = get_data(ticker)
rolling_price = get_rolling_mean(close_price)

differencing_order = get_differencing_order(rolling_price)
scaled_data, scaler = scaling(rolling_price)
rmse = evaluate_model(scaled_data, differencing_order)

st.write("**Model RMSE Score:**", rmse)


# forecasting
forecast = get_forecast(scaled_data, differencing_order)

forecast['Close'] = inverse_scaling(scaler, forecast['Close'])
st.write('#### Forecast Data (Next 30 days)')



# table of this forecast
fig_tail = plotly_table1(forecast.sort_index(ascending=True).round(3))
fig_tail.update_layout(height=220)
st.plotly_chart(fig_tail, use_container_width=True)

# plot the forecasting 
forecast = pd.concat([rolling_price, forecast])               
#rolling_price = actual historical data # forecast= 30 predicted values

st.plotly_chart(
    Moving_average_forecast(forecast),
    # go to this function->we are calling this so except last 30 days take for actual bcz it actual + predicted 
    use_container_width=True
)