from constants import API_TOKEN, breaker
from tu_data import *
import os, time


# 测试代码
if __name__ == "__main__":
    
    #行情示例 - 实时数据
    breaker()
    data = live_data("600519")
    print(data[['open', '']])
    
    #行情示例 - 实时数据分类
    breaker()
    print(data.columns.values.tolist())
    
    #行情示例 - 实时数据格式分割方法
    # breaker()
    # print(data[['code', 'price']])
    
    #行情示例 - 历史数据(至多一年半)
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
            
                # 输出格式化
                if begin ==  0:
                    print(trimmed.to_string(index=False))
                    begin = 1
                else:
                    print(trimmed.to_string(index=False, header=False))

                # 不要删除！避免TOKEN被禁用
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            print("正在退出...")
            quit()