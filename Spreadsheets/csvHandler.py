import pandas as pd
import numpy as np

class csvHandler:

    path = r"C:\Users\janva\Documents\Github\FXS-V1\TickerData\\"

    def read_tickers(self, t):
        return pd.read_csv(self.path+t+'.csv', index_col='date')

    def appendTickerData(self, t, df):
        df.to_csv(self.path+t+'.csv', mode='a', header=False, index=False)

    def initalHistoricData(self, t, dataframe):
        dataframe.to_csv(self.path+t+'.csv')
