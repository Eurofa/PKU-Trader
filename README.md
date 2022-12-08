# PKU Trader
---
## 组员

|姓名|负责部分|
|--|--|
|Kevin Miao|行情模块，交易模块|
|陈子豪|回测模块，交易模块|

---
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

---
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
    10：b1_v，买一 volume
    11：b1_p，买一 price 
    12：b2_v，买二 volume
    13：b2_p，买二 price
    14：b3_v，买三 volume
    15：b3_p，买三 price
    16：b4_v，买四 volume
    17：b4_p，买四 price
    18：b5_v，买五 volume
    19：b5_p，买五 price
    20：a1_v，卖一 volume
    21：a1_p，卖一 price
    22：a2v，卖2v 
    23：a2p，卖2p
    24：a3v，卖3v 
    25：a3p，卖3p 
    26：a4v，卖4v 
    27：a4p，卖4p 
    28：a5v，卖5v 
    29：a5p，卖5p 
    30：date，日期； 
    31：time，时间；
    32：code，股票代码

---
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
---
## Context模块
（周五写）
---
## Strategy模块

---
## Dtengine模块

---
## DtAnalysis模块
