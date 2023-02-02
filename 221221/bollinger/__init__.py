import numpy as np

class Bollinger():
    def __init__(self, df, col, start):
        self.df = df
        self.col = col
        self.start = start
    
    def testing(self):
        self.df = self.df[~self.df.isin([np.nan, np.inf, -np.inf]).any(1)]
        # 해당 컬럼만 남기고 나머지 컬럼은 삭제
        self.df = self.df.loc[:, [self.col]]
        # 이동 평균선, 상단 밴드, 하단 밴드 생성
        self.df['center'] = self.df[self.col].rolling(20).mean()
        self.df['ub'] = self.df['center'] + (2 * self.df[self.col].rolling(20).std())
        self.df['lb'] = self.df['center'] - (2 * self.df[self.col].rolling(20).std())

        self.df = self.df.loc[self.start :]

        self.df['trade'] = ''
        
        # trade 에 거래 내역 추가
        for i in self.df.index:
            if self.df.loc[i, self.col] > self.df.loc[i, 'ub']:
                if self.df.shift(1).loc[i, 'trade'] == 'buy':
                    self.df.loc[i, 'trade'] = ''
                else:
                    self.df.loc[i, 'trade'] = ''
            elif self.df.loc[i, self.col] < self.df.loc[i, 'lb']:
                if self.df.shift(1).loc[i, 'trade'] == 'buy':
                    self.df.loc[i, 'trade'] = 'buy'
                else:
                    self.df.loc[i, 'trade'] = 'buy'
            elif self.df.loc[i, self.col] >= self.df.loc[i, 'lb'] and self.df.loc[i, self.col] <= self.df.loc[i, 'ub']:
                if self.df.shift(1).loc[i, 'trade'] == 'buy':
                    self.df.loc[i, 'trade'] = 'buy'
                else:
                    self.df.loc[i, 'trade'] = ''

        self.df['return'] = 1
        self.rtn = 1.0
        self.buy = 0.0
        self.sell = 0.0

        for i in self.df.index:
        
            if self.df.shift(1).loc[i, 'trade'] == '' and self.df.loc[i,'trade'] == 'buy':
            
                self.buy = self.df.loc[i,self.col]
                
            elif self.df.shift(1).loc[i, 'trade'] == 'buy' and self.df.loc[i,'trade'] == '':
            
                self.sell = self.df.loc[i,self.col]
                self.rtn = (self.sell - self.buy) / self.buy + 1
                self.df.loc[i, 'return'] = self.rtn
                
        self.acc_rtn = 1.0

        for i in self.df.index:
            self.rtn = self.df.loc[i,'return']
            self.acc_rtn *= self.rtn
            self.df.loc[i, 'acc_rtn'] = self.acc_rtn
        
        print('누적수익률:', round(self.acc_rtn, 4))

        return self.df
