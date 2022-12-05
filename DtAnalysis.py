import pandas as pd
import numpy as np
import os
import xlsxwriter
#待之后将dtengine中的数据输出、计算拆到此处
class DtAnalysis:
    def __init__(self):
        self.profit_no_risk=1.5#无风险年化利率，暂用银行存款利率

    def caculate(self,Tsignal,Tdata):
        '''
        Tsignal:交易信号，记录买卖、量价、时间
        Tdata:行情数据，记录日线数据。

        Returns:pnl,胜率

        '''
        pass

    def save_file(self,win_ratio,pnl,trade_days,name='default',file_path='./bt_results/'):
        std=max(np.std(pnl),0.0001)
        if os.path.exists(file_path) is not True:
            os.mkdir(file_path[2:-1])
        file_path_xls=file_path+name+'.xlsx'
        #存入最基础的pnl信息并绘图
        df=pd.DataFrame(pnl,index=trade_days)
        df.to_excel(file_path_xls)
        sharp_ratio=(pnl[-1]-pow(self.profit_no_risk,len(pnl)/250))/std
        max_receive=max(1-min(pnl),0)#最大回撤
        Tdays=len(trade_days)#交易天数
        cum_pnl=pnl[-1]#累计收益率
        year_pnl=pnl[-1]/len(trade_days)*250
        #信息整理
        information={}
        information['夏普比率']=sharp_ratio
        information['最大回撤']=max_receive
        information['交易天数']=Tdays
        information['累计收益率']=cum_pnl
        information['年化收益率']=year_pnl
        information['胜率']=win_ratio
        self.write_information(pnl,trade_days,name=name,file_path=file_path,**information)


    def write_information(self,pnl,trade_days,name='default',file_path='./bt_results/',**kwargs):
        workbook = xlsxwriter.Workbook(file_path+name+'.xlsx')
        worksheet = workbook.add_worksheet()
        data = [
            trade_days,
            pnl,
        ]
        worksheet.write_column('A2', data[0])
        worksheet.write_column('B2', data[1])
        chart_col = workbook.add_chart({'type': 'line'})
        chart_col.add_series({
            'name': '策略收益率分析',
            'categories': f'=Sheet1!$A$2:$A${len(data[0])+1}',
            'values': f'=Sheet1!$B$2:$B${len(data[1])+1}',
            'points': [
                {'fill': {'color': '#00CD00'}},
                {'fill': {'color': 'red'}},
                {'fill': {'color': 'yellow'}},
                {'fill': {'color': 'gray'}},
            ],
        })
        chart_col.set_title({'name': '策略收益率分析'})
        chart_col.set_style(10)
        worksheet.insert_chart('D10', chart_col, {'x_offset': 25, 'y_offset': 10})
        # 写入其他信息
        r_start=3
        c_start=6
        for key,value in kwargs.items():
            worksheet.write(r_start,c_start,key)
            worksheet.write(r_start+1,c_start,value)
            c_start+=1
        worksheet.write(0,1,'收益率')
        worksheet.write(0,0,'交易日期')
        workbook.close()

