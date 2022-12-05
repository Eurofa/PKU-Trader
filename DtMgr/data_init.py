import requests
from urllib.request import quote, unquote
import re
import time
import pandas as pd

def get_headers(str_):
    return {str1.split(":")[0].strip(): str1.split(":", 1)[-1].strip() for str1 in str_.split("\n")}


if __name__=='__main__':
    try:
        sz50_code_name=pd.read_pickle('../datasets/stock/sz504query.pkl')
    except:
    #上证50代码更新,从百度股市通提取
        request_headers='''accept: application/vnd.finance-web.v1+json
    accept-encoding: gzip, deflate, br
    accept-language: zh-CN,zh;q=0.9
    cookie: BIDUPSID=D0F2AD3B7DC8AB2B126DE01960E3C42B; PSTM=1620975614; __yjs_duid=1_240b563cbf9240b6a34a0ed702f4b58a1620995199041; BDUSS=lFVUGdNczR4RlVzcEJwc0poekhNM1BTNnVZU2lsflN5bjd0dU91TVk3akpxZlJoRVFBQUFBJCQAAAAAAAAAAAEAAABT7IQbuqPModauyfEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMkczWHJHM1he; BDUSS_BFESS=lFVUGdNczR4RlVzcEJwc0poekhNM1BTNnVZU2lsflN5bjd0dU91TVk3akpxZlJoRVFBQUFBJCQAAAAAAAAAAAEAAABT7IQbuqPModauyfEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMkczWHJHM1he; BAIDUID=94C38F98A8D24FB520AB5FC8D7B09536:SL=0:NR=10:FG=1; MCITY=-131%3A; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; ab_sr=1.0.1_NjZmZDU5ZmZhYTFhM2I1Yzg4ODcwZDc5OTBlMGI1ODYxYTg1MzFlNTYzZDJjN2JjNmZiMjhjNjRmYzllYmM0M2U5NDY5YmE5ZDI1NTMzNWViZGJlYjI5ZTI1M2ViMmRjNjdhNWU5NTk4MjkzNjYyYTZkNTFjZGM2ZjgzMTM5OTZjZTAzM2FiZjA0Y2ZhZGFiMTU0NTg2YjZhOTE1MTdmNA==; H_PS_PSSID=37855_36561_37517_37835_37841_37872_37766_37796_36803_37761_26350_37786_37881; BA_HECTOR=25848505202k8g8l8k04a0db1hopikr1g; delPer=0; ZFY=mfSy3Ht:Aw6cSZayqvNyMwNVORbQpCUgYbI5zPzGE7CU:C; BAIDUID_BFESS=94C38F98A8D24FB520AB5FC8D7B09536:SL=0:NR=10:FG=1; RT="sl=1&ss=lb9kjwyy&tt=7h&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&z=1&dm=baidu.com&si=vjaq9mcc83n&ul=ig9n&ld=igl5&hd=igqm"; PSINO=7
    origin: https://gushitong.baidu.com
    referer: https://gushitong.baidu.com/
    sec-ch-ua: "Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"
    sec-ch-ua-mobile: ?0
    sec-ch-ua-platform: "Windows"
    sec-fetch-dest: empty
    sec-fetch-mode: cors
    sec-fetch-site: same-site
    user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'''
        request_headers=get_headers(request_headers)
        sz50_name_url = 'https://gushitong.baidu.com/opendata?resource_id=5352&query=000016&code=000016&name=%E4%B8%8A%E8%AF%8150&market=ab&group=asyn_ranking&pn=0&rn=50&pc_web=1&finClientType=pc'
        res = requests.get(sz50_name_url, headers=request_headers)
        sz50_code=re.findall('"code":"(\d+)","name":".*?","market":"ab"',res.text)
        sz50_name=re.findall('"code":"\d+","name":"(.*?)","market":"ab"',res.text)
        sz50_name=[x.encode().decode('unicode_escape') for x in sz50_name]
        sz50_code_name=pd.DataFrame(sz50_name,index=sz50_code)
        sz50_code_name.to_pickle('../datasets/stock/sz504query.pkl')
    print(sz50_code_name)

    #