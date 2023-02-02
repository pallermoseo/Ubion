import numpy as np
import pandas as pd

class Momentum():
    def __init__(self, df, col):
        self.df = df
        self.col = col
    
    def testing(self):
        
        if 'Date' not in self.df.columns: 
            self.df = self.df.reset_index()
            # self.df.reser_index(inplace=True)
        self.df = self.df[~self.df.isin([np.nan, np.inf, -np.inf]).any(1)] # 결측치, 이상치 제거
        self.df = self.df.loc[:, ['Date', self.col]] # self.df[['Date', self.col]]
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        self.df['STD-YM'] = self.df['Date'].dt.strftime('%Y-%m')
        self.df.set_index('Date', inplace=True)

        
        self.df2 = self.df[~(self.df.shift(-1)['STD-YM'] == self.df['STD-YM'])]
        self.df2['BF_1M'] = self.df2.shift(1)[self.col].fillna(0)
        self.df2['BF_12M'] = self.df2.shift(12)[self.col].fillna(0)
       

        self.df['trade'] = ''
        self.df['return'] = 1
        
        for i in self.df2.index:
            signal = ''
            momentum_index = self.df2.loc[i, 'BF_1M'] / self.df2.loc[i,'BF_12M'] - 1
            flag = True if((momentum_index > 0) and (momentum_index != np.inf) and (momentum_index != -np.inf)) else False
            if flag:
                signal ='buy'
            self.df.loc[i, 'trade'] = signal

        rtn = 1.0
        buy = 0
        sell = 0
        
        for i in self.df.index:
            # 구매한 날짜 체크 현재 trade = buy and 전 날 행의 trade =''
            if self.df.loc[i, 'trade'] =='buy' and self.df.shift(1).loc[i,'trade'] == '':
                buy = self.df.loc[i, self.col]
                print('구매일:', i,'구매가격:', buy)
            elif self.df.loc[i,'trade'] == '' and self.df.shift(1).loc[i,'trade'] =='buy':
                sell = self.df.loc[i, self.col]
                rtn = (sell-buy) / buy + 1
                self.df.loc[i, 'return'] = rtn
                print('판매일:', i, '판매가격:', sell, '수익률:', rtn)

            if self.df.loc[i,'trade'] =='':
                buy = 0
                sell = 0

        acc_rtn = 1

        for i in self.df.index:
            rtn = self.df.loc[i, 'return']
            acc_rtn *= rtn
            self.df.loc[i,'acc_rtn'] = acc_rtn

        print('누적 수익률:', acc_rtn)

        return self.df
