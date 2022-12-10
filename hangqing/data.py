from constants import API_TOKEN, breaker
from datetime import timedelta
from tu_data import *
import pandas as pd
import sqlite3 as sql
import os, time, io, math


# 示例代码
if __name__ == "__main__":
    
    #示例 - 实时数据
    breaker()
    data = live_data("600519", 1)
    print(data.to_string(index = False))
    
    #示例 - 数据分割方法
    breaker()
    print(data[['code', 'price']])
        
    #示例 - 历史数据(至多一年半)
    breaker()
    print(historical_k_data("600519", "2020-1-1"))
    
    #示例 - 历史数据(日线至多一年半，小时数据最多350个历史小时)
    breaker()
    df = historical_data("600519", 0)
    df.index = pd.to_datetime(df.index)
    
    # 数据获取演示 -------------------------------------
    
    #日期切割示例 - 仅过去一年
    # print("\n日期切割")
    # df = df['2021':'2022']
    
    # 若开盘价高于前收盘价 3%
    print("\n条件: 开盘价高于收盘价 3%")
    op3cl = df.loc[(df["open"] - df["close"].shift(-1))/df["close"].shift(-1) > 0.03]
    
    if op3cl.empty:
        print("\n没有匹配的结果\n")
    else:
        print(op3cl)
    
    # 若收盘价高于开盘价
    print("\n条件: 收盘价高于开盘价 5%")
    cl5op = df.loc[(df['close'] - df['open'])/df['open'] > 0.05]
    
    if cl5op.empty:
        print("\n没有匹配的结果\n")
    else:
        print(cl5op)
        
    # 若收盘价低于于开盘价
    print("\n条件: 收盘价低于开盘价 5%")
    cln5op = df.loc[(df['close'] - df['open'])/df['open'] < -0.05]
    
    if cln5op.empty:
        print("\n没有匹配的结果\n")
    else:
        print(cln5op)

    # 简单超买策略回测演示
    print("\n策略: 若收盘价高于开盘价 5% 则融券卖出")
    print("规则: 以收盘价格卖出, 第二个交易日收盘买回\n")
    
    breaker()
    print("简单超买策略回测开始 ($1,000,000, No Leverage, No TP/SL)")
    breaker()
    
    trigger_dates = cl5op.index.tolist()
    pnl_counter = 0
    
    for i in trigger_dates:
        print("Trigger Date: " + str(i.date()), end="")
        print(" --- Executing Date: " + str(i.date()+timedelta(days=1)))

        sell_price = cl5op.loc[i, 'close']
        shift = df['close'].shift(1)
        buy_price = shift.loc[i]
        volume = math.floor(1000000/sell_price)
       
        print("卖出 {}x @ {}, 买入 {}x @ {}".format(volume, sell_price, volume, buy_price))
        
        profit = (sell_price - buy_price)*volume
        pnl_counter += profit
        if profit >= 0:
            print("本次交易收益[${:.2f}]\n".format(profit))
        else:
            print("本次交易损失[${:.2f}]\n".format(profit))

    breaker()
    print("回测结束")
    breaker()
    
    print("总体PNL [${:.2f}]".format(pnl_counter))
    print("收益率 [{:.2f}%]".format(pnl_counter/1000000))
    
    breaker()
    
    # 简单超卖策略回测演示
    print("\n策略: 若收盘价低于开盘价 5% 则买入")
    print("规则: 以收盘价格买入, 第二个交易日收盘卖出\n")
    
    breaker()
    print("简单超卖策略回测开始 ($1,000,000, No Leverage, No TP/SL)")
    breaker()
    
    trigger_dates = cln5op.index.tolist()
    pnl_counter = 0
    
    for i in trigger_dates:
        print("Trigger Date: " + str(i.date()), end="")
        print(" --- Executing Date: " + str(i.date()+timedelta(days=1)))

        buy_price = cln5op.loc[i, 'close']
        shift = df['close'].shift(1)
        sell_price = shift.loc[i]
        volume = math.floor(1000000/buy_price)
       
        print("买入 {}x @ {}, 卖出 {}x @ {}".format(volume, buy_price, volume, sell_price))
        
        profit = (sell_price - buy_price)*volume
        pnl_counter += profit
        if profit >= 0:
            print("本次交易收益[${:.2f}]\n".format(profit))
        else:
            print("本次交易损失[${:.2f}]\n".format(profit))

    breaker()
    print("回测结束")
    breaker()
    
    print("总体PNL [${:.2f}]".format(pnl_counter))
    print("收益率 [{:.2f}%]".format(pnl_counter/1000000))
    
