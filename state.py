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
import requests


load_dotenv()

# Binance API data
api_key = os.getenv("API_KEY")
secret_key = os.getenv("SECRET_KEY")

client = Client(api_key, secret_key)


def telegram_bot_sendtext(bot_message):
   bot_token = os.getenv("BOT_TOKEN")
   bot_chatID = os.getenv("BOT_CHATID")
   send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
   response = requests.get(send_text)

def getData(symbol, interval, past):
  data = pd.DataFrame(client.get_historical_klines(symbol,interval,past + 'min ago UTC'))
  data = data.iloc[:,:5]
  data.columns = ['Time', 'Open', 'High', 'Low', 'Close']
  data = data.set_index('Time')
  data.index = pd.to_datetime(data.index, unit = 'ms')
  data = data.astype(float)
  return data


#df = getData('ADAEUR', '1m', '50')


def calcRSI (df):
  df['RSI'] = ta.RSI(np.array(df['Close']),timeperiod = 14)
  df['DIFF'] = df['Open'] - df['Close']
  df.dropna(inplace=True)


def strategy(pair,interval,past):
  df = getData(pair,interval,past)
  calcRSI(df)
  diff = df.Close.iloc[-1] - df.Open.iloc[-1]

  rsi = int(df.RSI.iloc[-1])
  if (rsi > 0) and (rsi < 20):
   rsi_state = ("RSI Oversold => %i" % rsi)
  elif (rsi > 20) and (rsi < 40):
    rsi_state = ("RSI Slightly Oversold => %i" % rsi)
  elif (rsi > 40) and (rsi < 60):
    rsi_state = ("RSI Stable => %i" % rsi)
  elif (rsi > 60) and (rsi < 75):
    rsi_state = ("RSI Slightly Overbought => %i" % rsi)
  elif (rsi > 75):
    rsi_state = ("Overbought  => %i" % rsi)

  telegram_bot_sendtext(f'Pair: *'+ pair + '*\n\nOpen Price:' + str(df.Open.iloc[-1])+' €'+ '\nClose Price: ' + str(df.Close.iloc[-1])+ ' €' + '\nDiff Open/Close is %.2f' % diff + ' €' +  '\n' + str(rsi_state))
  #with open(pair + '.csv', 'w', newline='') as file:
    #writer = csv.writer(file, delimiter=';')
    #writer.writerow(["Time","Open Price", "Close Price", "Diff Open/Close", "RSI"])
    #writer.writerow([str(df.Time.iloc[-1]),str(df.Open.iloc[-1]),str(df.Close.iloc[-1]),diff,str(rsi_state)])
    #file.close

strategy('BTCEUR', '1m', '50')
















#timestamp = client._get_earliest_valid_timestamp('ADAEUR', '1d')
#bars = client.get_historical_klines('ADAEUR', '1d', timestamp, limit=1000)

#btc_df = pd.DataFrame(bars, columns= ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume','Number of Trades', 'TB Base Volume', 'TB Quote Volume', 'Ignore'])
#btc_df.set_index('Open Time', inplace=True)
#btc_df.to_csv('ada_bars3.csv')




#ada_price = client.get_ticker(symbol = 'ADAEUR')


#print (ada_price['lastPrice'])
