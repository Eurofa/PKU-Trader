from gmtrade.api import *
from hangqing.constants import API_TOKEN, breaker
from hangqing.tu_data import *

#交易接口初始化
def trade_init() -> None:
    """初始化交易接口
    """
    #身份验证
    set_token(API_TOKEN)
    
    #链接服务器
    set_endpoint("api.myquant.cn:9000")

    #登录账户
    acc = account(account_id='ef37c766-6bbd-11ed-b621-00163e18a8b3', account_alias='PKU_Trader')

    #登录
    login(acc)

#账户资金查询
def balance() -> dict:
    """返回当前交易账户的账户资金余额

    Returns:
        dict: 返回一个dict, 共包含两项：1. Frozen 冻结金额 以及 2. Avail 可用余额
    """
    cash = get_cash()
    
    #数据整理
    buffer = dict()
    buffer["frozen"] = cash.frozen
    buffer["avail"] = cash.available
    return buffer

#持仓查询
def positions() -> list:
    """返回当前交易账户的全部持仓

    Returns:
        list: 返回一个list, 格式如下：
            'symbol': 'SHSE.600519', 
            'volume': 100, 
            'price': 101.0, 
            'average price': 100, 
            'profit/loss': 100, 
            'p/l_ratio': 0.01
    """
    
    positions = get_positions()
    
    #数据整理
    buffer_list = []
    
    for item in positions:
        buffer = dict()
        buffer["symbol"] = item.symbol
        buffer["volume"] = item.volume
        buffer["price"] = item.price
        buffer["average price"] = item.vwap
        buffer["profit/loss"] = item.fpnl
        
        #Calculate p/l percentage
        buffer["p/l_ratio"] = item.fpnl / (item.volume * item.vwap)
        
        buffer_list.append(buffer)
 
    return buffer_list

#模拟盘下单
def order(symbol, volume, side, order_type, order_price, order_effect) -> list:
    """创建新的订单

    Args:
        symbol (str): 股票代码
        volume (float): 股票数量
        side (int): 1 = 买单， 2 = 麦单
        order_type (int): 1 = 限价委托, 2 = 市价委托, 3 = 止损止盈委托
        order_price (float): 订单价格，默认为0
        order_effect (int): 1 = 开仓, 2 = 平仓

    Returns:
        list: 返回一个包含订单信息的列表, 格式如下：
            symbol: "600519"
            side: 1
            position_effect: 1
            order_type: 2
            status: 1
            price: 1731.0
            order_style: 1
            volume: 1
    """
    
    result = order_volume(symbol=symbol, volume=volume, side=side, order_type=order_type, position_effect=order_effect, price=order_price)
    
    return result

