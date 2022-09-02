from tkinter import NO
import requests
import pandas as pd
import json
import time

def return_common_stock_tickers(token):
    url = 'https://api.polygon.io/v3/reference/tickers'

    parameters = {
        'apiKey': token, # API key
        'type': 'CS', #query common stocks
        'market': 'stocks',
        'limit': 1000 # extract max data possible
    }

    try:
        tickers_json = requests.get(url, parameters).json()
        tickers_list = tickers_json['results']

        while tickers_json['next_url']:
            tickers_json = requests.get(tickers_json['next_url'], parameters).json()
            tickers_list.extend(tickers_json['results'])
            if 'next_url' not in tickers_json.keys():
                break

            # trigger a wait since free tier is limited to 5 calls/min
            time.sleep(12)

    except:
        return None

    return tickers_list


# write our data to .csv or json file

token = input('API key')
tickers = return_common_stock_tickers(token)

# write out as csv 
df_cs_tickers = pd.DataFrame(tickers)
df_cs_tickers.to_csv('polygon_cs_tickers.csv')

# write out as txt
with open('polygon_cs_tickers.txt', 'w') as outfile:
    json.dump(tickers, outfile, indent=4)