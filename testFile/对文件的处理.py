import pandas as pd
import numpy as np

df = pd.read_csv('data/sales_records_20087_21000.csv')

print(df.head())
print("============================")
print(df.loc[df['amount'] == 1857]) #索引的时满足该条件的行

#将amount设置为索引直接可用loc查询
print("="*50)
df = df.set_index('amount')
df = df.sort_index() #对索引进行排序
print(df.loc[1857])
print(df)

#数值区间查询
print("="*50)
# df = np.sort(df)
print(df.loc[200:2000]) #loc的切片操作其必须为递增的


#表达式查询
print(df.loc[(df['status']=="已支付")&(df["city"]=="上海")])

#自定义查询
def above_average(df):
    return df['user_id'] > df['user_id'].mean()
print(df.loc[above_average(df)]) #返回user_id大于平均值的

#匿名函数

print(df.loc[lambda x:x['age_group'] == '26-35']) #查询年龄段在26-35的订单


