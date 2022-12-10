import tushare as ts
import time
from pandas import DataFrame

TOKEN = "563ff3abd2b93e7d8b065e22439c5d3a3164f28c0855a097e65841cb"

ts.set_token(TOKEN)

def live_data(symbol: str, depth=1) -> DataFrame:
    """实时行情数据

    Args:
        symbol (str): 股票代码
        depth (int, optional): 挡位, 默认为1挡，最多支持5挡数据.

    Returns:
        DataFrame: Pandas Dataframe
    """
    raw = ts.get_realtime_quotes(symbol)
    
    # 根据Depth提供 1~5 挡买卖量价
    depth_list = []
    for i in range(1, depth+1):
        bid = 'b'
        ask = 'a'
        depth_list.append(bid+str(i)+'_p')
        depth_list.append(bid+str(i)+'_v')
        depth_list.append(ask+str(i)+'_p')
        depth_list.append(ask+str(i)+'_v')
    
    base_data = ['code', 'time', 'price', 'high', 'low', 'bid', 'ask', 'volume']

    return raw[base_data + depth_list]

def historical_data(symbol: str, limit=0) -> DataFrame:
    """历史日频数据 - 此数据已是以日期为时间序列index的格式

    Args:
        symbol (str): _description_
        limit (int, optional): 结果上限，若为空或0则为无限

    Returns:
        DataFrame: Pandas Dataframe
    """
    data = ts.get_hist_data(symbol, ktype="D")
    
    data = data[['open', 'high', 'close', 'low', 'volume', 'ma5', 'ma10', 'ma20', 'v_ma5', 'v_ma10','v_ma20']]
    
    if limit == 0:
        return data
    else:
        return data.head(limit)
    
def historical_tick(symbol: str, date: str, limit=0) -> DataFrame:
    """历史（单日）逐笔成交数据

    Args:
        symbol (str): 股票代码
        date (str): 起始日期，如 2022-12-01
        limit (int, optional): Defaults to 0.

    Returns:
        DataFrame: Pandas DataFrame
    """
    data = ts.get_tick_data(symbol, date=date)
    
    if data == None:
        return "权限错误，Tick数据需要付费Tushare Pro接口\n"
    else:
        if limit == 0:
            return data
        else:
            return data.head(limit)

def historical_k_data(symbol: str, start_date: str) -> DataFrame:
    """旧版 Tushare 数据接口，可支持至多20年数据 

    Args:
        symbol (str): 股票代码
        start_date (str): 起始日期，如 2022-12-01

    Returns:
        DataFrame: Pandas DataFrame
    """
    data = ts.get_k_data(symbol, start=start_date)
    return data

# 演示代码
# data = live_data("600519", 5)
# print(data.to_string(index = False))