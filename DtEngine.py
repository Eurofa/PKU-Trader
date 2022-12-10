import random
import trade_rule
import Context
import pandas as pd
import numpy as np
import Myquant_API as api
from gmtrade.api import *
from DtAnalysis import DtAnalysis
from Strategy import BaseStrategy, TestStrategy
from hangqing.constants import breaker

# 运行的策略用一个DtEngine统一管理包装,后续计划添加多进程功能


class DtEngine:
    def __init__(self):
        api.trade_init
        # self.stg_context=[[BaseStrategy.BaseStrategy(),Context.Context()]]#Context默认从2021-04-19到今天，无code_list
        self.stg_context = []
        self.__config__ = dict()  # 配置信息，如数据保存位置

    def change_context(self, context, index):
        self.stg_context[index][1] = context

    def set_stg(self, strategy: BaseStrategy, index):
        self.stg_context[index][0] = strategy

    def set_default_positon(self, context, code):
        context.positions.setdefault(
            code, {'volume_today': 0, 'volume': 0, 'pnl': 0, 'price': 0, 'avg': 0, 'p/l_ratio': 0})
        return context

    def run_backtest(self, start, end, init_cur, stg: BaseStrategy):
        # 创建一个新的stg_context并初始化
        context = Context.Context()
        context.balance = {'frozen': 0, 'avail': init_cur}
        context.today = end
        code_list = pd.read_pickle('./datasets/stock/sz504query.pkl').index.tolist()
        context.code_list = code_list[:3]
        trade_days = trade_rule.trade_time.trade_days()
        self.stg_context.append([stg, context])  # 策略传入前应对象化
        for code in context.code_list:
            try:
                context.daysdata[code] = pd.DataFrame()
                context.get_daysdata(code)  # 提前缓存context中的日线数据
            except:
                pass
            
        # 从start至end每日进行一次预测与交易
        start_index = trade_days.index(start)
        end_index = trade_days.index(end)
        
        # 统计
        win_count, pnl_ratio = [
            0]*(start_index-end_index), [-1]*(start_index-end_index)
        trade_count = 0
        Trecord = {}
        breaker()
        print("""| 启动回测 | 
初始资金：              1，000，000.00 CNY
风控因子(最大回撤)：    20.0%
风险偏好：              70/100
              """)
        for i in range(start_index-end_index):
            while len(context.code_list) < 3:
                context.code_list.append(random.choice(code_list))
                context.today = end
                context.get_daysdata(context.code_list[-1])
                
            # 若当日为空
            for code in context.code_list:
                m = 0
                while context.daysdata[code].empty:
                    context.today = trade_days[j-m]
                    context.get_daysdata(code)
                    m += 1
            j = start_index-i
            context.today = trade_days[j]
            
            # 生成交易信号
            Tsignal = stg.on_bar(context)
            
            # 执行回测内交易，通过wtanalysis分析，记录收益pnl、胜率等，更新context的balance、position
            tomorrow = trade_days[j-1]
            tomorrow_trading = {}
            
            for key in list(set(context.daysdata.keys()).intersection(context.code_list)):
                try:
                    tomorrow_trading[key] = context.daysdata[key].loc[tomorrow]
                except:
                    print(f'{key}在{tomorrow}没有数据')
                    
            Trecord.setdefault(tomorrow, [])
            
            for Tsig in Tsignal:
                if Tsig[2]-1.5 > 0:
                    if tomorrow_trading[Tsig[0]]['high'] > Tsig[4]:  # 成交
                        context.positions[Tsig[0]]['volume_today'] = Tsig[1]
                        trade_fee = Tsig[4] * Tsig[1] * context.trading_fee_ratio
                        pnl_this = (Tsig[4]-context.positions[Tsig[0]]['avg']) * Tsig[1]-Tsig[4]*Tsig[1]*context.trading_fee_ratio
                            
                        context.positions[Tsig[0]]['pnl'] = pnl_this
                        context.positions[Tsig[0]]['avg'] = (context.positions[Tsig[0]]['avg']*context.positions[Tsig[0]]['volume']+trade_fee)/context.positions[Tsig[0]]['volume']
                        
                        context.positions[Tsig[0]]['volume'] -= Tsig[1]
                        
                        context.balance['avail'] += Tsig[4]*Tsig[1]-trade_fee
                        
                        if pnl_this > 0:
                            win_count[i] += 1
                        trade_count += 1
                        Trecord[tomorrow].append(Tsig)
                    else:
                        continue
                    
                else:  # 买入
                    if tomorrow_trading[Tsig[0]]['low'] < Tsig[4]:  # 成交
                        last_pnl = 0
                        context = self.set_default_positon(context, Tsig[0])
                        trade_fee = Tsig[4] * Tsig[1] * \
                            context.trading_fee_ratio
                        context.positions[Tsig[0]]['volume_today'] = Tsig[1]
                        if context.positions[Tsig[0]]['volume'] == 0:
                            last_pnl = context.positions[Tsig[0]]['pnl']
                        context.positions[Tsig[0]]['avg'] = (context.positions[Tsig[0]]['volume'] *
                                                             context.positions[Tsig[0]]['avg']+Tsig[1]*Tsig[4] +
                                                             trade_fee-last_pnl)/(Tsig[1]+context.positions[Tsig[0]]['volume'])

                        context.positions[Tsig[0]]['volume'] += Tsig[1]
                        context.balance['avail'] -= Tsig[4]*Tsig[1]+trade_fee
                        Trecord[tomorrow].append(Tsig)
                    else:
                        continue
                    
            for key, value in context.positions.items():
                try:
                    # 这个try可以帮助避开不在code_list但是曾在持仓的code
                    value['price'] = tomorrow_trading[key]['close']
                except:
                    print(f'{key}退出交易，其收益率为{value["p/l_ratio"]}')
                    context.positions.pop(key)
                if value['volume'] > 10:
                    value['pnl'] = (value['price']-value['avg'])*value['volume']
                    value['p/l_ratio'] = value['pnl']/value['avg'] / value['volume']*pow(-1, (value['avg'] < 0))
                    
            context.balance['frozen'] = np.sum([position['price']*position['volume'] for key, position in context.positions.items()])
            pnl_ratio[i] = (context.balance['avail'] + context.balance['frozen'])/init_cur
            
            breaker()
            output_stringbuilder = ""
            output_stringbuilder += 'PNL Ratio:     '
            output_stringbuilder += "{:.2f}%".format((float(pnl_ratio[i]-1))*100)
            output_stringbuilder += "\n"
            output_stringbuilder += 'Win Count:     ' 
            output_stringbuilder += str(win_count[i])
            output_stringbuilder += "\n"
            output_stringbuilder +=  'PNL:          '
            output_stringbuilder += "{:.2f}￥".format(context.account_pnl())
            output_stringbuilder += "\n"

            print(output_stringbuilder)
            
            print("当前持仓: ")
            for item in context.positions.keys():
                print("[SHSE:{}]".format(item))
            print("\n完整持仓信息: ")
            print(context.positions)
            
        win_ratio = np.sum(win_count)/trade_count
        
        # 输出回测结果
        dta = DtAnalysis()
        dta.save_file(win_ratio, pnl_ratio,
                      trade_days[end_index:start_index], name='bt_test', file_path='./Demo/bt_results/')
        return win_ratio, pnl_ratio

    def run_ontime(self):
        pass
        # 由于数据接口限制暂无详细历史日内数据


if __name__ == '__main__':
    dte = DtEngine()
    trade_days = trade_rule.trade_time.trade_days()
    esStg = TestStrategy.EsStg()
    esStg.on_init(1)
    win_raito, pnl_ratio = dte.run_backtest(
        trade_days[-200], trade_days[190], 1000000, esStg)

    breaker()
    print("| 回测完成 | \n结果已输出至 ./Demo/bt_results/bt_test.xlsx, 请使用 Excel 查看\n")
