#!/usr/bin/python

from binance.client import Client
import csv
import pandas as pd

api_key = os.getenv("API_KEY")
secret_key = os.getenv("SECRET_KEY")



client = Client(api_key, secret_key)

try:
  sell = client.create_order(symbol='BNBUSDT', side='SELL', type='MARKET', quantity=0.1)

except BinanceAPIException as e:
  # error handling goes here
  print(e)
except BinanceOrderException as e:
  # error handling goes here
  print(e)




#timestamp = client._get_earliest_valid_timestamp('ADAUSDT', '1d')

#bars = client.get_historical_klines('ADAUSDT', '1d', timestamp, limit=1000)

#btc_df = pd.DataFrame(bars, columns= ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume','Number of Trades', 'TB Base Volume', 'TB Quote Volume', 'Ignore'])
#btc_df.set_index('Open Time', inplace=True)
#print(btc_df.head())


#btc_df.to_csv('ada_bars3.csv')
