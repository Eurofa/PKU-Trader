import pandas as pd


def trade_days():
    return pd.read_pickle('datasets/historical_data/600519.pkl').index.tolist()
class trade_time:
    def __init__(self):
        self.trade_days=pd.read_pickle('datasets/historical_data/600519.pkl').index.tolist()

    @classmethod
    def trade_days(cls):
        return pd.read_pickle('datasets/historical_data/600519.pkl').index.tolist()

if __name__=='__main__':
    pass