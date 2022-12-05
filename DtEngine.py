import random

import pandas as pd
import Context
from Strategy import BaseStrategy,TestStrategy
from gmtrade.api import *
import trade_rule
import numpy as np
from DtAnalysis import DtAnalysis
API_TOKEN = "e2faec93d69c35b1a9d348ca46fcf38726370474"
def account_init():
    # 身份验证
    set_token(API_TOKEN)

    # 链接服务器
    set_endpoint("api.myquant.cn:9000")

    # 登录账户
    acc = account(account_id='ef37c766-6bbd-11ed-b621-00163e18a8b3', account_alias='PKU_Trader')

    # 登录
    login(acc)
#运行的策略用一个DtEngine统一管理包装,后续再写多进程功能
class DtEngine:
    def __init__(self):
        account_init()
        # self.stg_context=[[BaseStrategy.BaseStrategy(),Context.Context()]]#Context默认从2021-04-19到今天，无code_list
        self.stg_context = []
        self.__config__=dict() #配置信息，如数据保存位置

    def change_context(self,context,index):
        self.stg_context[index][1]=context

    def set_stg(self,strategy:BaseStrategy,index):
        self.stg_context[index][0]=strategy

    def set_default_positon(self,context,code):
        context.positions.setdefault(code,{'volume_today':0,'volume':0,'pnl':0,'price':0,'avg':0,'p/l_ratio':0})
        return context
    def run_backtest(self,start,end,init_cur,stg:BaseStrategy):
        #创建一个新的stg_context并初始化
        context=Context.Context()
        context.balance={'frozen':0,'avail':init_cur}
        context.today=end
        code_list=pd.read_pickle('./datasets/stock/sz504query.pkl').index.tolist()#之后替换为全域股票
        context.code_list=code_list[:3]#测试少用几个#TODO:正式时删掉本行
        trade_days=trade_rule.trade_time.trade_days()
        self.stg_context.append([stg,context])#策略传入前应对象化
        for code in context.code_list:
            try:
                context.daysdata[code]=pd.DataFrame()
                context.get_daysdata(code)#提前缓存context中的日线数据
            except:
                pass
        #从start至end每日进行一次预测与交易
        start_index=trade_days.index(start)
        end_index=trade_days.index(end)
        #统计
        win_count, pnl_ratio = [0]*(start_index-end_index), [-1]*(start_index-end_index)
        trade_count=0
        Trecord={}
        for i in range(start_index-end_index):
            while len(context.code_list)<3:
                context.code_list.append(random.choice(code_list))
                context.today=end
                context.get_daysdata(context.code_list[-1])
            #若当日为空
            for code in context.code_list:
                m=0
                while context.daysdata[code].empty:
                    context.today=trade_days[j-m]
                    context.get_daysdata(code)
                    m+=1
            j=start_index-i
            context.today=trade_days[j]
            #生成交易信号
            Tsignal=stg.on_bar(context)#[symbol,vol,side,o_type,price,o_effect]
            #执行回测内交易，通过wtanalysis分析，记录收益pnl、胜率等，更新context的balance、position
            tomorrow=trade_days[j-1]
            tomorrow_trading={}
            for key in list(set(context.daysdata.keys()).intersection(context.code_list)):
                try:
                    tomorrow_trading[key] = context.daysdata[key].loc[tomorrow]
                except:
                    print(f'{key}在{tomorrow}没有数据')
            Trecord.setdefault(tomorrow,[])
            for Tsig in Tsignal:
                # tomorrow_trading[Tsig[0]]=context.daysdata[Tsig[0]].loc[tomorrow]
                # today_trading=context.daysdata[Tsig[0]].loc[context.today]
                if Tsig[2]-1.5>0:#卖出 全卖，还未写部分卖策略
                    if tomorrow_trading[Tsig[0]]['high']>Tsig[4]:#成交
                        context.positions[Tsig[0]]['volume_today']=Tsig[1]
                        trade_fee=Tsig[4] * Tsig[1] * context.trading_fee_ratio
                        pnl_this=(Tsig[4]-context.positions[Tsig[0]]['avg'])*Tsig[1]-Tsig[4]*Tsig[1]*context.trading_fee_ratio
                        context.positions[Tsig[0]]['pnl']=pnl_this
                        context.positions[Tsig[0]]['avg']=(context.positions[Tsig[0]]['avg']*context.positions[Tsig[0]]['volume']+trade_fee)/context.positions[Tsig[0]]['volume']
                        context.positions[Tsig[0]]['volume']-=Tsig[1]
                        context.balance['avail']+=Tsig[4]*Tsig[1]-trade_fee
                        if pnl_this>0:
                            win_count[i]+=1
                        trade_count+=1
                        Trecord[tomorrow].append(Tsig)
                    else:
                        continue
                else:#买入
                    if tomorrow_trading[Tsig[0]]['low']<Tsig[4]:#成交
                        last_pnl=0
                        context=self.set_default_positon(context,Tsig[0])
                        trade_fee=Tsig[4]* Tsig[1] * context.trading_fee_ratio
                        context.positions[Tsig[0]]['volume_today']=Tsig[1]
                        if context.positions[Tsig[0]]['volume']==0:
                            last_pnl=context.positions[Tsig[0]]['pnl']
                        context.positions[Tsig[0]]['avg']=(context.positions[Tsig[0]]['volume']*
                                                           context.positions[Tsig[0]]['avg']+Tsig[1]*Tsig[4]+
                                                           trade_fee-last_pnl)/(Tsig[1]+context.positions[Tsig[0]]['volume'])
                        # context.positions[Tsig[0]]['pnl'] += (Tsig[4] - context.positions[Tsig[0]]['avg']) * context.positions[Tsig[0]]['volume'] - \
                        #                                      context.positions[Tsig[0]]['avg'] * Tsig[
                        #                                          1] * context.trading_fee_ratio
                        context.positions[Tsig[0]]['volume']+=Tsig[1]
                        context.balance['avail']-=Tsig[4]*Tsig[1]+trade_fee
                        Trecord[tomorrow].append(Tsig)
                    else:
                        continue
            for key,value in context.positions.items():
                try:
                    value['price'] = tomorrow_trading[key]['close']#这个try可以帮助避开不在code_list但是曾在持仓的code
                except:
                    print(f'{key}退出交易，其收益率为{value["p/l_ratio"]}')#TODO:是否对每个策略都需要更换code_list？
                    context.positions.pop(key)
                if value['volume']>10:
                    value['pnl']=(value['price']-value['avg'])*value['volume']
                    value['p/l_ratio'] = value['pnl']/value['avg']/value['volume']*pow(-1,(value['avg']<0))
            context.balance['frozen']=np.sum([position['price']*position['volume'] for key,position in context.positions.items()])
            pnl_ratio[i]=(context.balance['avail']+context.balance['frozen'])/init_cur
            print('pnl_ratio:',pnl_ratio[i],'win_count',win_count[i],'pnl',context.account_pnl())
            # print(Trecord[tomorrow])
            print(context.positions)
        win_ratio=np.sum(win_count)/trade_count
        #输出回测结果
        dta=DtAnalysis()
        dta.save_file(win_ratio,pnl_ratio,trade_days[end_index:start_index],name='bt_test',file_path='./Demo/bt_results/')
        return win_ratio,pnl_ratio

    def run_ontime(self):
        pass
        #暂无日内数据

if __name__=='__main__':
    dte=DtEngine()
    trade_days=trade_rule.trade_time.trade_days()
    esStg=TestStrategy.EsStg()
    esStg.on_init(1)
    win_raito,pnl_ratio=dte.run_backtest(trade_days[-200],trade_days[190],1000000,esStg)
    #一个bug，180的时候没有数据？
    print(win_raito)
    print(pnl_ratio)