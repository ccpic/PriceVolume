# -*- coding: UTF-8 -*-
import pandas as pd

class tsMatrix(pd.DataFrame):

    def __init__(self, *args, **kw):
        super(tsMatrix, self).__init__(*args, **kw)
        if self.columns[0][:5] == 'Value':
            self.unit = '销售额'
        elif self.columns[0][:6] == 'Volume':
            self.unit = '销售量'
        else:
            self.unit = ''


    def toGR(self, periods=4):
        df = self.astype('float')
        df.columns = df.columns.str[-4:]
        df_gr = df.pct_change(axis=1, periods=periods)
        df_gr.dropna(how='all', axis=1, inplace=True)
        return df_gr


    def toDiff(self, periods=4):
        df = self.astype('float')
        df.columns = df.columns.str[-4:]
        df.fillna(0, inplace=True)
        df_diff = df.diff(axis=1, periods=periods)
        df_diff.dropna(how='all', axis=1, inplace=True)
        return  df_diff


    def toTotalGR(self, periods=4):
        df = self.astype('float')
        df.columns = df.columns.str[-4:]
        df_total = df.sum().to_frame().T
        df_total_gr = df_total.pct_change(axis=1, periods=periods)
        df_total_gr.dropna(how='all', axis=1, inplace=True)
        return df_total_gr.T


    def toBaseGR(self, base='17Q1', sort=True, sort_ascending=False, head=0):
        df = self.astype('float')
        df.columns = df.columns.str[-4:]
        for i in range(0, len(df.index)):
            df.iloc[i] = df.iloc[i].div(df.ix[i, base]).subtract(1)
        df = df.iloc[:, -7:]
        df.dropna(how='all', axis=0, inplace=True)
        if sort:
            df.sort_values('18Q3', ascending=sort_ascending, inplace=True)
        if head > 0:
            df = df.head(head)
        return df


    def toBaseDiff(self, base='17Q1', sort=True, sort_ascending=False, head=0):
        df = self.astype('float')
        df.columns = df.columns.str[-4:]
        for i in range(0, len(df.index)):
            df.iloc[i] = df.iloc[i].subtract(df.ix[i, base])
        df = df.iloc[:, -7:]
        df.dropna(how='all', axis=0, inplace=True)
        if sort:
            df.sort_values('18Q3', ascending=sort_ascending, inplace=True)
        if head > 0:
            df = df.head(head)
        return df
