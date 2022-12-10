#策略调用的类，提供数据（行情、仓位、时间）接口、下单接口等
import pandas as pd
import Myquant_API as api
from gmtrade.api import *
from hangqing import tu_data
import os, time

def date_int_trans(datetime):
    if isinstance(datetime,str):
        datetime=int(datetime.replace('-',''))
    else:
        datetime=str.format(f'{int(datetime/10000)}-{int(datetime/100%100)}-{int(datetime%100)}')
    return datetime

class Context:
    def __init__(self,start='2021-04-19',today=time.strftime('%Y-%m-%d'),code_list=[]):
        # api.trade_init()    #初始化接口
        
        self.code_list=code_list    #策略所需的股票代码池
        self.start=start    # 策略开始时间
        self.today=today    # 默认取本地当前时间
        
        self.positions = {}    # 持仓
        self.balance={'frozen':0,'avail':0}    # 余额
        self.pnl=0
        self.daysdata={}    #缓存之前的数据
        self.trading_fee_ratio=0.0005    #交易税
        self.on_init()
        
    def on_init(self):
        for code in self.code_list:
            self.daysdata[code]=pd.DataFrame()
            
    #更新实时账户数据
    def update_data(self):
        self.positions=self.account_positions()
        self.balance=self.account_balance()
        self.pnl=self.account_pnl()

    def change_code_list(self,code,mode=1):
        #1加入code,2移除code
        if mode==1:
            self.code_list.append(code)
        else:
            self.code_list.remove(code)

    #账户仓位
    def account_positions(self):
        return api.positions()
    
    # 账户资金查询
    def account_balance(self):
        return api.balance()
    
    #账户盈亏统计
    def account_pnl(self):
        #算每个仓位的盈亏，初始调用一次，末尾调用一次。
        # positions=self.account_positions()
        positions=self.positions
        pnl=0
        for key,value in positions.items():
            pnl+=value['pnl']
        return pnl
    #获取分钟线数据
    def data_minute(self,code,minutes):
        pass
        # 暂无分钟线历史数据


    #获取、更新日线数据
    def get_daysdata(self,code):
        '''
        :param days:日线天数
        :return:从self.today开始往前到start的日线数据
        '''
        if not self.daysdata[code].empty and code in self.daysdata.keys() and date_int_trans(self.daysdata[code].index[0])>date_int_trans(self.today) \
                and date_int_trans(self.daysdata[code].index[-1])<date_int_trans(self.start):
            m = self.daysdata[code].index.get_loc(self.today)
            try:
                n = self.daysdata[code].index.get_loc(self.start)
            except:
                n = self.daysdata[code].shape[0]
            return self.daysdata[code].iloc[m:n,:]
        today=date_int_trans(self.today)
        flag=1
        try:
            days_data=pd.read_pickle('./datasets/historical_data/'+str(code)+'.pkl')#若无最新数据则更新
            newest_date=date_int_trans(days_data.index[0].replace('-',''))
            if newest_date<today and time.localtime().tm_hour>15 and today<=time.localtime().tm_mday:
                flag=2
            else:
                flag=0
        except:
            pass
        if bool(flag):
            new_data = tu_data.historical_data(str(code))
            if flag==1:
                days_data=new_data
            else:#合并新数据和旧数据
                old_index=days_data.index[0]
                k=new_data.index.get_loc(old_index)
                days_data=pd.concat([new_data.iloc[:k,:],days_data])
            file_name = './datasets/historical_data/'+ str(code) + '.pkl'
            days_data.to_pickle(file_name)
        try:
            m=days_data.index.get_loc(date_int_trans(today))
        except:
            m=1
        try:
            n=days_data.index.get_loc(self.start)
        except:
            n=days_data.shape[0]
        self.daysdata[code]=days_data
        res_data=days_data.iloc[m:n,:]
        return res_data


if __name__=='__main__':
    context=Context()
    # context.today='2022-10-10'
    # df=context.get_daysdata(context.code_list[0])
    # print(df)