
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
    # breaker()
    # print(data[['code', 'price']])
    
    #行情示例 - 至多一年半历史数据
    breaker()
    print(historical_data("600519", 10))
    print(historical_data("600519", 10).columns.values.tolist())

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