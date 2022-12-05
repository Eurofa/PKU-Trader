from constants import API_TOKEN, breaker
from tu_data import *
import os, time


# 测试代码
if __name__ == "__main__":
    
    #示例 - 实时数据
    breaker()
    data = live_data("600519", 1)
    print(data.to_string(index = False))
    
    #示例 - 数据分割方法
    # breaker()
    # print(data[['code', 'price']])
    
    #示例 - 历史数据(至多一年半)
    # breaker()
    # print(historical_data("600519", 10))


    breaker()
    mode = 0
    # mode = input("任意字符退出, 1 进入循环拉取模式:\n")
    begin = 0
    
    if mode == "1":
        os.system("cls")
        try:
            while True:
                data = live_data("600519", 1)
            
                # 输出格式化
                if begin ==  0:
                    print(data.to_string(index=False))
                    begin = 1
                else:
                    print(data.to_string(index=False, header=False))

                # 不要删除！避免TOKEN被禁用
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            print("正在退出...")
            quit()