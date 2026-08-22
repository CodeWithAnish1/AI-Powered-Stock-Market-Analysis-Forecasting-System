import plotly.graph_objects as go
import pandas_ta as pta
import datetime
from dateutil.relativedelta import relativedelta
 
 
def plotly_table(dataframe): 
    headerColor = 'grey' 
    rowEvenColor = '#f8fafd' 
    rowOddColor = '#e1efff' 
 
    fig = go.Figure(data=[go.Table( 
        header=dict( 
            values=["", ""], 
            line_color='#0078ff', 
            fill_color='#0078ff', 
            align='center', 
            font=dict(color='white', size=15), 
            height=35, 
        ), 
        cells=dict( 
            values=[["<b>" + str(i) + "</b>" for i in dataframe.index]] + [dataframe[i].tolist() for i in dataframe.columns], 
            fill_color=[[rowOddColor, rowEvenColor]], 
            align='left', 
            line_color=['white'], 
            font=dict(color=['black'], size=15) 
        ) 
    )]) 
 
    fig.update_layout( 
        height=220, 
        margin=dict(l=0, r=0, t=0, b=0) 
    ) 

    return fig

def plotly_table1(dataframe): 
    headerColor = 'grey' 
    rowEvenColor = '#f8fafd' 
    rowOddColor = '#e1efff' 
 
    fig1 = go.Figure(data=[go.Table( 
        header=dict( 
            values=["", ""], 
            line_color='#0078ff', 
            fill_color='#0078ff', 
            align='center', 
            font=dict(color='white', size=15), 
            height=35, 
        ), 
        cells=dict( 
            values=[["<b>" + str(i) + "</b>" for i in dataframe.index]] + [dataframe[i].tolist() for i in dataframe.columns], 
            fill_color=[[rowOddColor, rowEvenColor]], 
            align='left', 
            line_color=['white'], 
            font=dict(color=['black'], size=15) 
        ) 
    )]) 
 
    fig1.update_layout( 
        height=400, 
        margin=dict(l=0, r=0, t=0, b=0) 
    ) 
 
    return fig1



def filter_data(dataframe, num_period):
    if num_period == '1mo':
        date = dataframe.index[-1] + relativedelta(months=-1)                      #  take the last/ latest date -> do the month-=1

    elif num_period == '5d':
        date = dataframe.index[-1] + relativedelta(days=-5)

    elif num_period == '6mo':
        date = dataframe.index[-1] + relativedelta(months=-6)

    elif num_period == '1y':
        date = dataframe.index[-1] + relativedelta(years=-1)

    elif num_period == '5y':
        date = dataframe.index[-1] + relativedelta(years=-5)

    elif num_period == 'ytd':
        date =  datetime.datetime(dataframe.index[-1].year, 1, 1).strftime('%Y-%m-%d')   #  datetime.datetime(2026, 1, 1) = 1 jan 2026
        #strftime('%Y-%m-%d') = 2026-01-01 (made)  
        # ytd= This year full data
    else:
        date = dataframe.index[0]                                                   # oldest or first available data

    return dataframe.reset_index()[dataframe.reset_index()['Date'] > date]          # Changing the index -> Date and find the actual date whichi is interval of this period








def close_chart(dataframe, num_period=False):                                    # if num_period not available then also okh.
    if num_period:
        dataframe = filter_data(dataframe, num_period)                            # if num_period is there then collect the data

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'],            # Take the stock's Open price and draw it as a line against the Date
                             mode='lines',
                             name='Open', line=dict(width=2, color='#5ab7ff')))

    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'],           # Scatter plot but not every time it scatterd may be line
                             mode='lines',
                             name='Close', line=dict(width=2, color='black')))

    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'],
                             mode='lines', name='High',
                             line=dict(width=2, color='#0078ff')))

    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'],
                             mode='lines', name='Low',
                             line=dict(width=2, color='red')))

    fig.update_xaxes(rangeslider_visible=True)     #  Range slider

    fig.update_layout(height=500, margin=dict(l=0, r=20, t=20, b=0),
                      plot_bgcolor='white', paper_bgcolor='#efefff',
                      legend=dict(         #type of legend -> show open high written in a fig
                          yanchor="top",
                          xanchor="right"
                      ))

    return fig

def candlestick(dataframe, num_period):
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()    # make a empty chart

    # add_trace means adds something to the chart 
    fig.add_trace(go.Candlestick(x=dataframe['Date'],open=dataframe['Open'],high=dataframe['High'],
                                 low=dataframe['Low'],close=dataframe['Close']))

    fig.update_layout(showlegend=False, height=500, margin=dict(l=0, r=20, t=20, b=0), plot_bgcolor='white', paper_bgcolor='#efefff')

    return fig


def RSI(dataframe, num_period):                                       # RSI , Overbrought, Oversold 

    dataframe['RSI'] = pta.rsi(dataframe['Close'])                    # Calculate the RSI using the stock's Close prices and store the result in a new column called RSI.
    dataframe = filter_data(dataframe, num_period) 

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe.RSI, name='RSI', marker_color='orange',
        line=dict(width=2, color='orange'),
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=[70] * len(dataframe), name='Overbought', marker_color='red',     # reference/boundary line at RSI =70  # len(dataframe)=5  (------) 
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=[30] * len(dataframe), fill='tonexty',
        name='Oversold', marker_color='#79da84',
        line=dict(width=2, color='#79da84', dash='dash'),
    ))

    fig.update_layout(
        yaxis_range=[0, 100],
        height=200, plot_bgcolor='white', paper_bgcolor='#efefff',
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict( 
            orientation='h',     # show the legend items horizontly instead of vertically
            yanchor='top',
            y=1.02,
            xanchor='right',
            x=1
        )
    )

    return fig


def Moving_average(dataframe,num_period):                                    #open close high low SMA_50 all show by lines

    dataframe['SMA_50'] = pta.sma(dataframe['Close'],50)                     #50-day Simple Moving Average (SMA) using the Close price and store it in a new column called SMA_50.
    dataframe = filter_data(dataframe,num_period)
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'],
                             mode='lines',
                             name='Open', line = dict(width=2,color = '#5ab7ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'],
                             mode='lines',
                             name='Close', line = dict(width=2,color = 'black')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'],
                             mode='lines', name='High',
                             line = dict(width=2,color = '#0078ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'],
                             mode='lines', name='Low',
                             line = dict(width=2,color = 'red')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['SMA_50'],
                             mode='lines', name='SMA 50',
                             line = dict(width=2,color = 'purple')))

    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(height = 500,margin=dict(l=0, r=20, t=20, b=0), plot_bgcolor = 'white',paper_bgcolor = '#efefff',legend=dict(
    yanchor="top",
    xanchor="right"
    ))

    return fig


def MACD(dataframe, num_period):

    macd = pta.macd(dataframe['Close']).iloc[:,0]                             # macd line, macd signal, macd historam -> 3 things in macd indicator 
    macd_signal = pta.macd(dataframe['Close']).iloc[:,1]
    macd_hist = pta.macd(dataframe['Close']).iloc[:,2]
    dataframe['MACD'] = macd
    dataframe['MACD Signal'] = macd_signal
    dataframe['MACD Hist'] = macd_hist
    dataframe = filter_data(dataframe,num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['MACD'], name='MACD', marker_color='orange', line=dict(width=2,color='orange'),
    ))
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe['MACD Signal'], name='MACD Signal', marker_color='red', line=dict(width=2,color='red',dash='dash'),
    ))
    c = ['red' if cl < 0 else 'green' for cl in macd_hist]

    fig.add_trace(go.Bar(
        x=dataframe['Date'],
        y=dataframe['MACD Hist'],
        marker_color=c,
        name='MACD Hist'
    ))

    fig.update_layout(
        height=200,plot_bgcolor='white', paper_bgcolor='#efefff',margin=dict(l=0, r=0, t=0, b=0),legend=dict(orientation="h",
        yanchor="top",
        y=1.02,
        xanchor="right",
        x=1
        )
    )
    return fig



def Moving_average_forecast(forecast):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=forecast.index[:-30], y=forecast['Close'].iloc[:-30],           # All previous up to 30 days back
                             mode='lines', name='Close Price',
                             line=dict(width=2, color='black')))                               # actual price

    fig.add_trace(go.Scatter(x=forecast.index[-31:], y=forecast['Close'].iloc[-31:],           # 31 se all
                             mode='lines', name='Future Close Price',
                             line=dict(width=2, color='red')))                                 # forecasted price 

    fig.update_xaxes(rangeslider_visible=True)

    fig.update_layout(height=500, margin=dict(l=0, r=20, t=20, b=0),
                      plot_bgcolor='white', paper_bgcolor='#efefff',
                      legend=dict(
                          yanchor="top",
                          xanchor="right"
                      ))

    return fig