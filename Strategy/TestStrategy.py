import pandas as pd

from Strategy import BaseStrategy
import statsmodels.api as sm
class EsStg(BaseStrategy.BaseStrategy):
    def __init__(self,name='EsStg'):
        self.name=name

    def on_init(self,period:int,safe_factor=0.2,risk_factor=70):
        self.period=period#忘记是什么了，间隔？
        self.safe_factor=safe_factor#风控因子,当最大回撤到多少时不再交易此股票，0~0.3
        self.risk_factor=risk_factor#风险偏好，0~100

    def on_caculate(self,context):
        res={}
        vix_sum=0
        for code in context.code_list:
            try:#预防停牌
                daysdata=context.get_daysdata(code)
            except:
                context.daysdata[code]=pd.DataFrame()
                continue# res[code] = {'high': 1000000, 'low': 0, 'vix': 100}
            #预测波动率
            VIX=daysdata.high.subtract(daysdata.low).div(daysdata.close)
            Vix_train=VIX.tolist()
            Vix_train.reverse()
            Vix_model=sm.tsa.ExponentialSmoothing(Vix_train,seasonal_periods=4, trend='add', seasonal='add').fit()
            vix=Vix_model.forecast(1)
            vix_sum+=vix
            #预测最高价
            high_train=daysdata['high'].tolist()
            high_train.reverse()
            high_model=sm.tsa.ExponentialSmoothing(high_train,seasonal_periods=4, trend='add', seasonal='add').fit()
            high=high_model.forecast(1)
            #预测最低价
            low_train=daysdata['low'].tolist()
            low_train.reverse()
            low_model=sm.tsa.ExponentialSmoothing(low_train,seasonal_periods=4, trend='add', seasonal='add').fit()
            low=low_model.forecast(1)
            close_=daysdata.iloc[0]['close']
            #不超过最高最低涨跌幅
            high=min(high,close_*1.1)
            low=max(low,close_*0.9)
            res[code]={'high':high,'low':low,'vix':vix}
        vixmean=vix_sum/len(context.code_list)#平均波动率
        return res,vixmean

    def on_bar(self,context):
        #先根据ES预测下一日的max、min，在最高价最低价相差risk_factor%的位置买卖即可。
        pre,vixmean=self.on_caculate(context)
        positions=context.positions
        balance=context.balance#当日交易额不超过现有*0.3
        avail=balance['avail']*0.3
        Tsignal=[]
        for key,value in pre.items():
            try:
                avg=positions[key]['avg']
                pnl_ratio=positions[key]['p/l_ratio']
                volume_s=positions[key]['volume']
            except:
                avg=(pre[key]['high']+pre[key]['low'])/2
                pnl_ratio=0
                volume_s=0
            high=pre[key]['high']
            low=pre[key]['low']
            vix=pre[key]['vix']
        #生成交易信号[symbol,vol,side,o_type,price,o_effect]
            s_price=int((high-vix*(100-self.risk_factor)/100*avg/2)*100)/100
            b_price=int((low+vix*(100-self.risk_factor)/100*avg/2)*100)/100
            volume_b=int(avail/len(pre)*vix/vixmean/100/b_price)*100
            if pnl_ratio<-1*self.safe_factor and volume_s==0 and avg>0:
                context.code_list.remove(key)
                continue
            if volume_s!=0 and avg<s_price-context.trading_fee_ratio*volume_s*s_price/100:
                Tsignal.append([key,volume_s,2,1,s_price,2])#平仓
            if volume_b!=0 and b_price<s_price-context.trading_fee_ratio*volume_b*b_price/100:
                Tsignal.append([key,volume_b,1,1,b_price,1])
        return Tsignal

    def on_tick(self,context,newTick):
        pass

