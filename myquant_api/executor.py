from gmtrade.api import *
from constants import API_TOKEN
from tu_data import *
import os, time

#初始化接口
def init():
    #身份验证
    set_token(API_TOKEN)
    
    #链接服务器
    set_endpoint("api.myquant.cn:9000")

    #登录账户
    acc = account(account_id='ef37c766-6bbd-11ed-b621-00163e18a8b3', account_alias='PKU_Trader')

    #登录
    login(acc)

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

#格式代码
def breaker():
    print("\n" + '-'*25 + "\n")

# 测试代码
if __name__ == "__main__":
    #初始化
    init()
    
    #模拟盘交易服务
        # status = start()
        # if status == 0:
        #     print('连接交易服务成功.................')
        #     pass
        # else:
        #     print('接交易服务失败.................')
        #     stop()

    #行情 & 交易
    
    #行情示例 - 实时数据
    breaker()
    data = live_data("600519")
    print(data)
    
    #行情示例 - 实时数据分类
    breaker()
    print(data.columns.values.tolist())
    
    #行情示例 - 实时数据格式分割方法
    breaker()
    print(data[['code', 'price']])
    
    #行情示例 - 至多一年半历史数据
    # breaker()
    # print(historical_data("600519", 10))

    breaker()
    mode = input("任意字符退出, 1 进入循环拉取模式:\n")
    begin = 0
    if mode == "1":
        os.system("cls")
        try:
            while True:
                data = live_data("600519")
                trimmed = data[['time','code','name','price','volume','bid','ask']]
                if begin ==  0:
                    print(trimmed.to_string(index=False))
                    begin = 1
                else:
                    print(trimmed.to_string(index=False, header=False))

                # 不要删除！避免TOKEN被禁用
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("Quiting...")
            quit()