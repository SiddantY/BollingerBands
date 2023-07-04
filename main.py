import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
#from yahoofinancials import YahooFinancials

def get_ticker_df():
    stock_ticker = input("Enter a stock ticker: ")
    df = yf.download(stock_ticker, start='2021-01-01', end='2023-06-30', progress=False)
    return df

def graph_data(df):
    period = 20

    df['SMA'] = df['Close'].rolling(window=period).mean()
    df['STD'] = df['Close'].rolling(window=period).std()
    df['Upper'] = df['SMA'] + (df['STD'] * 2)
    df['Lower'] = df['SMA'] - (df['STD'] * 2)

    columns = ['Close', 'SMA', 'Upper', 'Lower']
    df[columns].plot(figsize=(12.5, 6.5))
    plt.title('Bollinger Bands')
    plt.ylabel('Price USD ($)')
    #plt.show()

    gra = plt.figure(figsize=(12.5, 6.5))
    ax = gra.add_subplot(1,1,1)
    x_axis = df.index

    ax.fill_between(x_axis, df['Upper'], df['Lower'], color='grey')
    ax.plot(x_axis, df['Close'], color='gold', lw=2, label = 'Close')
    ax.plot(x_axis, df['SMA'], color='blue', lw=2, label = 'Simple Moving Average')

    ax.set_title('Bollinger Band')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price USD($)')

    plt.xticks(rotation=45)
    ax.legend()
    plt.show()

def generate_buy_and_sell_signals(df):
    buy_signal = []
    sell_signal = []

    for i in range(len(df['Close'])):
        if df['Close'][i] > df['Upper'][i]:
            buy_signal.append(np.nan)
            sell_signal.append(df['Close'][i])
        elif df['Close'][i] < df['Lower'][i]:
            buy_signal.append(df['Close'][i])
            sell_signal.append(np.nan)
        else:
            buy_signal.append(np.nan)
            sell_signal.append(np.nan)
    
    return buy_signal, sell_signal

def final_graph(df):
    gra = plt.figure(figsize=(12.5, 6.5))
    
    ax = gra.add_subplot(1,1,1)
    x_axis = df.index

    ax.fill_between(x_axis, df['Upper'], df['Lower'], color='grey')
    ax.plot(x_axis, df['Close'], color='gold', lw=2, label = 'Close')
    ax.plot(x_axis, df['SMA'], color='blue', lw=2, label = 'Simple Moving Average')

    ax.scatter(x_axis, df['Buy'], color='green', lw=2, label = 'Buy', marker = '^', alpha = 1)
    ax.scatter(x_axis, df['Sell'], color='red', lw=2, label = 'Sell', marker = 'v', alpha = 1)

    ax.set_title('Bollinger Band')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price USD($)')

    plt.xticks(rotation=45)
    ax.legend()
    plt.show()



if __name__ == "__main__":
    period = 20
    plt.style.use('fivethirtyeight')
    df = get_ticker_df()

    new_df = df[20-1:]

    new_df['SMA'] = new_df['Close'].rolling(window=period).mean()
    new_df['STD'] = new_df['Close'].rolling(window=period).std()
    new_df['Upper'] = new_df['SMA'] + (new_df['STD'] * 2)
    new_df['Lower'] = new_df['SMA'] - (new_df['STD'] * 2)
    
    new_df['Buy'], new_df['Sell'] = generate_buy_and_sell_signals(new_df)
    final_graph(new_df)
    #graph_data(df, buysignal, sellsignal)

    print(1)