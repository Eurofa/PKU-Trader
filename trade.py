from gmtrade.api import *

#账户资金查询
def balance():
    cash = get_cash()
    
    #数据整理
    buffer = dict()
    buffer["frozen"] = cash.frozen
    buffer["avail"] = cash.available
    return buffer

#持仓查询
def positions():
    
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

#下单(无内置验证)
def order(symbol, volume, side, order_type, order_price, order_effect):
    # side: buy = 1, sell = 2
    # order_type: 1 = 限价委托, 2 = 市价委托, 3 = 止损止盈委托
    # order_effect: 1 = 开仓, 2 = 平仓 *MORE AVAIL
    
    result = order_volume(symbol=symbol, volume=volume, side=side, order_type=order_type, position_effect=order_effect, price=order_price)
    
    return result
