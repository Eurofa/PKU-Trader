from EmQuantAPI import *

def init():
    
    # 使用前必须先打开 EMQuant > LoginActivator.exe
    
    #Type = c.EmQuantData
    loginresult = c.start( )
    
    return loginresult

print(init())