import uuid
from datetime import datetime, timedelta

import matplotlib
# this line is needed to avoid ModuleNotFoundError: No module named '_tkinter'
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import pandas as pd
from pandas_datareader import data as web

def message_handling(data):
    '''Get a message from the Telegram server and returns a message object with the data that we need'''

    Message = namedtuple('Message', [
        'text', 'first_name',
        'chat_id', 'message_id', 'message_lower_case',
        'message_array', 'update_id' ])
    
    text = data['message']['text']
    first_name = data['message']['chat']['first_name']
    chat_id = data['message']['chat']['id']
    # Message
    message_id = data['message']['message_id']
    message_lower = text.lower()
    message_array = text.split()
    # Update
    update_id = data['update_id']

    message = Message(
        text,
        first_name,
        chat_id,
        message_id,
        message_lower,
        message_array,
        update_id)
    
    return message

def calc_rolling_mean(df, list_of_averages):
    for average in list_of_averages:
        column_name = "SMA_{}".format(average)
        df[column_name] = df['Adj Close'].rolling(window=average).mean()

def get_averages(message):

    try:
        etf = web.DataReader(message.message_array[1], "yahoo")
    except OSError:
        msg = "ETF: {} - Codice errato".format(message.message_array[1])
        return msg, None
    column = ['Adj Close']
    for col in etf.columns.tolist():
        if col not in column:
            etf = etf.drop(col, 1)
    calc_rolling_mean(etf, [30, 100, 300])
    
    last_year = etf.index[-1]
    from_year = str(last_year.year-4)
    etf = etf[from_year:]
    
    # PLOT
    plt.style.use('fivethirtyeight')
    plt.figure(figsize=(20, 10))
    plt.plot(etf.index, etf['SMA_30'], label="SMA 30 days")
    plt.plot(etf.index, etf['SMA_100'], label="SMA 100 days")
    plt.plot(etf.index, etf['SMA_300'], label="SMA 300 days")
    plt.stackplot(etf.index, etf['Adj Close'], labels=["Adjusted closing price"], alpha=0.3, color='#00688B')
    plt.ylim(ymin=etf.describe().loc["min"].min())
    title = "Value VS SMA ({})".format(message.message_array[1].upper())
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.autoscale(tight=True)
    plt.legend(loc=2)
    plt.grid(True)
    
    msg = "COMMAND: {} - ETF: {} - Day: {} - Closed price: {:0.2f} - SMA 30 days: {:0.2f} - SMA 100 days: {:0.2f}	- SMA 300 days {:0.2f}"
    msg = msg.format(message.message_array[0],
                                 message.message_array[1],
                                 etf.index[-1],
                                 etf.iloc[-1]['Adj Close'],
                                 etf.iloc[-1]['SMA_30'],
                                 etf.iloc[-1]['SMA_100'],
                                 etf.iloc[-1]['SMA_300']
                                 )
    return msg, plt
