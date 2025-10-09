import pandas as pd
import numpy as np

#基础读取CSV文件

df = pd.read_csv('testFile\ecommerce_orders.csv')

print('=====基础数据信息======')
print(df.head(3))

#高级读取：指定参数处理数据

#解析日期列，指定索引列，处理缺失值， 转换数据类型
df = pd.read_csv(
    'testFile\ecommerce_orders.csv',
    parse_dates=['order_date'], #将order_data解析成日期类型
    index_col='order_id', #将order_id设置为索引
    na_values=[''], #将空字符串视为缺失值
    dtype={
        'user_id': 'int32',
        'amount': "float32",
        'shipping_time': 'float32',
    },
    true_values=['True'],
    false_values=['False'] #指定哪些值被视为False
)

print('数据类型：')
print(df.dtypes)

print("\n数据概览：")
print(df.info())

#数据的清洗和转化
# df['product_category'].fillna("未知类别", inplace=True)

print("==========数据分析结果=============")

#计算会员与非会员的平均订单金额
member_analysis = df.groupby('is_member')['amount'].agg(['mean','count'])
member_analysis.columns = [
    '平均订单金额',
    '订单数量'
]
print(member_analysis.round(2))

#计算各支付方式订单占比
payment_analysis = df['payment_method'].value_counts(normalize=True) * 100
print("各支付方式占比")
print(payment_analysis.round(2).astype(str) + '%')

#分析订单日期分布
date_analysis = df.groupby('order_date')['amount'].sum()
print('每日总销售额')
print(date_analysis.round(2))