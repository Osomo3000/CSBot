#!/usr/bin/python

from binance.client import Client
import csv
import pandas as pd
import btalib
import mplfinance as mpf
import talib as ta
import numpy as np
from dotenv import load_dotenv
import os


load_dotenv()


# Binance API data
api_key = os.getenv("API_KEY")
secret_key = os.getenv("SECRET_KEY")

client = Client(api_key, secret_key)

def getData(symbol, interval, past):
  data = pd.DataFrame(client.get_historical_klines(symbol,interval,past + 'min ago UTC'))
  data = data.iloc[:,:5]
  data.columns = ['Time', 'Open', 'High', 'Low', 'Close']
  data = data.set_index('Time')
  data.index = pd.to_datetime(data.index, unit = 'ms')
  data = data.astype(float)
  return data


df = getData('ADAEUR', '1m', '50')


def calcRSI (df):
  df['RSI'] = ta.RSI(np.array(df['Close']),timeperiod = 14)
  df['DIFF'] = df['Open'] - df['Close']
  df.dropna(inplace=True)


def strategy(pair,interval,past):
  df = getData(pair,interval,past)
  calcRSI(df)
  print (f'Current Close Price is ' + str(df.Close.iloc[-1]))
  print (f'Current RSI Value is ' + str(df.RSI.iloc[-1]))


calcRSI(df)

print(df)
















#timestamp = client._get_earliest_valid_timestamp('ADAEUR', '1d')
#bars = client.get_historical_klines('ADAEUR', '1d', timestamp, limit=1000)

#btc_df = pd.DataFrame(bars, columns= ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume','Number of Trades', 'TB Base Volume', 'TB Quote Volume', 'Ignore'])
#btc_df.set_index('Open Time', inplace=True)
#btc_df.to_csv('ada_bars3.csv')




#ada_price = client.get_ticker(symbol = 'ADAEUR')


#print (ada_price['lastPrice'])
