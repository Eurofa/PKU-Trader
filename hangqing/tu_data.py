import tushare as ts
import time


TOKEN = "563ff3abd2b93e7d8b065e22439c5d3a3164f28c0855a097e65841cb"

ts.set_token(TOKEN)

# 实时行情数据
def live_data(symbol):
    return ts.get_realtime_quotes(symbol)

# 历史日频数据
def historical_data(symbol, limit=0):
    
    data = ts.get_hist_data(symbol)
    
    if limit == 0:
        return data
    else:
        return data.head(limit)
    
# 历史（单日）逐笔成交数据
def historical_tick(symbol, date, limit=0):
    data = ts.get_tick_data(symbol)
    
    if limit == 0:
        return data
    else:
        return data.head(limit)