import pandas as pd

import numpy as np

#生成时间索引排除周末

#freq="B"表示工作日， 自动跳过周六周日
stock = ['StockA', 'StockB']
time_idex = pd.date_range(start='2025-01-01', periods=10, freq="B")
indicators = ['Close', 'Volume'] #指标维度收盘价，成交量
#生成时间序列(模拟日度收盘价，基于随机数调整)


np.random.seed(42)

stock_close = np.random.rand(10) * 2 + 150 

stock_series = pd.Series(
    data=stock_close.round(2),
    index=time_idex,
    name="ClosePrice" #序列名称
)
stockA  = pd.DataFrame({
    'Close':np.random.uniform(100, 110, 10).round(2),
    'Volume': np.random.randint(100, 2000, 10)
}, index=time_idex 
)
stockA['Stock'] = 'StockA' #标记股票名称
stockB = pd.DataFrame({
    'Close':np.random.uniform(80, 90, 10).round(2),
    'Volume': np.random.randint(1000, 1500, 10)
}, index=time_idex 
)
stockB['Stock'] = 'StockB' #标记股票名称

#时间序列核心操作
print("========Time-Series========")
print("原始时间序列:")
print(stock_series)

#时间范围筛选（直接按日期字符串筛选）
print("1月5日后收盘价")
print(stock_series[stock_series.index >= '2025-01-05'])

#重采样
print("日度数据重采样为周度均值")
print(stock_series.resample('W').mean().round(2)) #resample()重采样

#滚动窗口（计算三日平均移动，用于观察价格趋势）
print("3日收盘价移动平均")
print(stock_series.rolling(window=3).mean().round(2)) #rolling()窗口滚动
#=========================================股票A和B的操作=================================
#合并为带Multiindex的DataFrame
#合并两个股票DataFrame
combined_df = pd.concat([stockA, stockB])
#设置多层索引
mulit_df = combined_df.set_index(['Stock', combined_df.index])

mulit_df.index.names = ['Stock', 'Date']

print("========================= MultiIndex DataFrame====================")
print("完整数据")
print(mulit_df)

#筛选单只股票的所有数据
print("筛选StockA的所有数据")
print(mulit_df.loc['StockA'])

#筛选特定日期的所有的股票数据
print("1-03当天所有的股票数据")
#按照第二层索引筛选用xs方法
print(mulit_df.xs('2025-01-03', level='Date'))

print("筛选所有股票的收盘价（Close）：")
print(mulit_df['Close'])

print("筛选StockB在2025-01-02到01-04的成交量")
print(mulit_df.loc[('StockB', slice('2025-01-02', '2025-01-04')), 'Volume'])#股票+日期范围， 指标