# PKU Trader 简易量化交易系统

## 组员

|姓名|负责部分|
|--|--|
|Kevin Miao|行情模块，交易模块|
|陈子豪|回测模块，交易模块|

<br>

# 简介

PKU-Trader为自行搭建的量化策略运行平台，目前实装了行情模块、回测模块和交易模块。

<br>

# 试用方法

行情模块试用方式:
```
python ./hangqing/data.py
python ./hangqing/trade.py
```
回测模块试用方式：

```
python ./DtEngine.py
```
回测结果以xlsx的形式输出至./Demo/bt_results文件夹下

<br>

# 模块简介

## Context模块
本模块主要为策略运行环境和数据仓库的对接层，其中封装了与行情模块的接口，以及一些信息格式转换的方法。通过context模块，可以为策略运行创建一个独立实时的数据环境，方便未来的多进程运行设计。其中主要方法包括get_daysdata、account_pnl、account_positions，分别用来获取指定TimeRange内的日线数据，账户的profit&loss、账户仓位等。

## Strategy模块
本模块主要为策略基本类，内有生成交易信号的on_bar方法，主职计算与预测的on_caculate方法，由于之前未获得tick级别数据，故on_tick，select_code模块暂未在测试模型中启用，但基本模块中包含。

## Dtengine模块
本模块主要为量化运行的总数据环境管理，通过Dtengine模块，我们可以将多个策略放在不同的context上组合运行，目前这块主要完成了回测功能，即run_backtest部分。

## DtAnalysis模块
本模块主要为数据分析与格式化输出层，用于在策略运行时输出统计指标和运行相关指标，如在run_backtest中输出Pnl和胜率等相关信息并绘图。

<br>

# 其他信息


## 交易所支持
本项目通过MYQUANT进行模拟交易，支持的交易所包括：

- 上交所，市场代码 SHSE
- 深交所，市场代码 SZSE
- 中金所，市场代码 CFFEX
- 上期所，市场代码 SHFE
- 大商所，市场代码 DCE
- 郑商所，市场代码 CZCE
- 纽约商品交易所， 市场代码 CMX (GLN, SLN)
- 伦敦国际石油交易所， 市场代码 IPE (OIL, GAL)
- 纽约商业交易所， 市场代码 NYM (CON, HON)
- 芝加哥商品期货交易所，市场代码 CBT (SOC, SBC, SMC, CRC)
- 纽约期货交易所，市场代码 NYB (SGN)

注：由于MYQUANT不提供行情API，行情另外从Tushare拉取（免费版有限制）

<br>

## 实时行情数据格式
    0：name 股票名称
    1：open，今日开盘价 
    2：pre_close，昨日收盘价 
    3：price，当前价格
    4：high，今日最高价 
    5：low，今日最低价 
    6：bid，竞买价，即“买一”报价 
    7：ask，竞卖价，即“卖一”报价 
    8：volumn，成交量
    9：amount，成交金额 
    10：b1_v，买1 volume
    11：b1_p，买1 price 
    12：b2_v，买2 volume
    13：b2_p，买2 price
    14：b3_v，买3 volume
    15：b3_p，买3 price
    16：b4_v，买4 volume
    17：b4_p，买4 price
    18：b5_v，买5 volume
    19：b5_p，买5 price
    20：a1_v，卖1 volume
    21：a1_p，卖1 price
    22：a2_v，卖2 volume 
    23：a2_p，卖2 price
    24：a3_v，卖3 volume 
    25：a3_p，卖3 price 
    26：a4_v，卖4 volume 
    27：a4_p，卖4 price 
    28：a5_v，卖5 volume 
    29：a5_p，卖5 price 
    30：date，日期； 
    31：time，时间；
    32：code，股票代码

<br>

## 历史行情数据格式
    1. open
    2. high
    3. close
    4. low
    5. volume
    6. 价格变动（单位）
    7. 价格变动（百分比）
    8. MA5
    9. MA10
    10. MA20
    11. VMA5
    12. VMA10
    13. VMA20
    14. Turnover

