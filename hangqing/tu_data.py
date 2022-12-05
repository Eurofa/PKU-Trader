import tushare as ts
import time


TOKEN = "563ff3abd2b93e7d8b065e22439c5d3a3164f28c0855a097e65841cb"

ts.set_token(TOKEN)

# 实时行情数据
def live_data(symbol, depth=1):
    raw = ts.get_realtime_quotes(symbol)
    
    # 根据Depth提供 1~5 挡买卖量价
    depth_list = []
    for i in range(1, depth+1):
        bid = 'b'
        ask = 'a'
        depth_list.append(bid+str(depth)+'_p')
        depth_list.append(bid+str(depth)+'_v')
        depth_list.append(ask+str(depth)+'_p')
        depth_list.append(ask+str(depth)+'_v')
    
    base_data = ['code', 'time', 'price', 'high', 'low', 'bid', 'ask', 'volume']

    return raw[base_data + depth_list]

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