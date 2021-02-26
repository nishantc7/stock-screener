from flask import Flask, render_template, request
from patterns import candlestick_patterns
from nsetools import Nse
import csv
import json
from nsepy import get_history
from datetime import date, timedelta
import os
import pandas as pd
import talib

app = Flask(__name__)

stocks = {}
nifty_list = csv.reader(open('ind_nifty100list.csv'))


@app.route('/')
def index():

    pattern = request.args.get('pattern', None)
    for stock in nifty_list:
        symbol = stock[0]
        stocks[symbol] = {'company':stock[1]}
    
    # print(stocks)
    if pattern:
        datafiles = os.listdir('datasets')
        for dataset in datafiles:
            df = pd.read_csv(f'datasets/{dataset}')
            #print(df)
            pattern_function = getattr(talib,pattern)
            symbol = dataset.split(".")[0]
            try:
                result = pattern_function(df['Open'],df['High'],df['Low'],df['Close'])
                #print(result)
                last = result.tail(1).values[0]
                # print(last)
                if last >0 :
                    stocks[symbol][pattern] = 'bullish'
                elif last < 0 :
                    stocks[symbol][pattern] = 'bearish'
                else: 
                    stocks[symbol][pattern] = None

            except:
                pass
            
    return render_template('index.html', patterns=candlestick_patterns , stocks = stocks , current_pattern=pattern)

@app.route('/realtimesnapshot')
def realtimesnapshot():
    nse = Nse()
    nifty_list = csv.reader(open('ind_nifty100list.csv'))
    quotes = {}
    for stock in nifty_list:
        fetched_quote = nse.get_quote(stock[0])
        print("fetching "+ stock[0] )
        quotes[stock[0]] = {
        "open": fetched_quote["open"],
        "close": fetched_quote["lastPrice"],
        "dayLow": fetched_quote["dayLow"],
        "dayHigh": fetched_quote["dayHigh"]
        }
    with open("quotes.json","w") as f:
        json.dump(quotes,f)
    return quotes

@app.route('/snapshot')
def snapshot():
    
    for stock in nifty_list:
        symbol = stock[0]
        days = date.today() - timedelta(5)
        df = get_history(symbol=symbol,start= days,end=date.today())
        df.to_csv(f"datasets/{symbol}.csv")
    return {}
