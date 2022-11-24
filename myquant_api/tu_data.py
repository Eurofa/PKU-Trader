import tushare as ts
import time


TOKEN = "563ff3abd2b93e7d8b065e22439c5d3a3164f28c0855a097e65841cb"

ts.set_token(TOKEN)

def live_data(symbol):
    return ts.get_realtime_quotes(symbol)

def historical_data(symbol, limit=0):
    
    data = ts.get_hist_data(symbol)
    
    if limit == 0:
        return data
    else:
        return data.head(limit)