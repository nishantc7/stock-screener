from pprint import pprint
import json
import csv
from nsepy import get_history
from datetime import date
f = open("stock.json")
data = json.load(f)

quotes = {}
i = 0

nifty_list = csv.reader(open('ind_nifty100list.csv'))
for stock in nifty_list:
    symbol = stock[0]
    df = get_history(symbol=symbol,start=date(2020,2,11),end=date(2020,2,22))
    df.to_csv(f"datasets/{symbol}.csv")

    

