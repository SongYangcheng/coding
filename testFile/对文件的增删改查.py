import pandas as pd
import numpy as np

df = pd.read_csv('data/beijing_weather_2018.csv')
print(df.head)
print(df.describe())

#增加数据
#将api转换为整数，转换失败errors提示， 无效转为NaN
df['aqi'] = pd.to_numeric(df['aqi'], errors='coerce') 

df['city'] = '北京' #临时新增不影响元数据
print("成功添加city")
print(df.head())

#新曾温差列（最高温减去最低温）

df['bWendu_num'] = df['bWendu'].str.replace('℃', '').astype(int)
df['yWendu_num'] = df['yWendu'].str.replace('℃', '').astype(int)

#计算温差
df['wencha'] = df['bWendu_num'] - df['yWendu_num']
df['wencha'] = df['wencha'].astype(str) + "℃"
print("温差:")
print(df[['ymd','bWendu', 'yWendu', 'wencha']].head())

#新增空气质量
df['aqi_pingjia'] = df['aqiLevel'].apply(lambda x:'良好'if x <= 2 else '污染')
print(df[['ymd', 'aqiLevel', 'aqiInfo', 'aqi_pingjia']].head())
#可以直接赋值
# df['ymd'] = df['ymd']
df['ymd3'] = 3
print("="*50)
print(df.head())

#2. 新增1行数据(指定新增日期为2019-01-01,避免与2018年日期重复)
new_row = {
'ymd': '2019-01-01',
'bWendu': '2℃',
'yWendu': '-7℃',
'tiangi':'晴',
'fengxiang':'东北风',
'fengli':'1-2级',
'aqi': '65',
'aqiInfo':'良',
'aqiLevel': 2,
'city':'北京',
'bWendu_num': 2,
'yWendu_num': -7,
'wencha': 9,
'aqi_pingjia':'良好'
}

df = df._append(new_row, ignore_index=True)
print("新增后数据行数:",len(df))#输出367

# 新增日期设为2018年之后,避免冲突
df['ymd'] = pd.date_range(
    start='2018-01-01',
    periods=367,
    freq='D',
).astype(str)

print(df[['ymd']].tail(5))

#数据备份
df_backup = df.copy()

#将2018-01-01风力改为从1-2改为2

df.loc[df['ymd']=='2018-01-01', 'fengli'] = '2级'
print("修改后")
print(df.loc[df['ymd']=='2018-01-01', 'fengli'])

#基于条件进行批量修改
df['aqi'] = df['aqi'].str.strip().astype(float)
df.loc[df['aqi'] > 200, 'aqi_pingjia'] = "严重污染"
print("修改重度污染")
print(df[["aqi","aqi_pingjia"]])
print(df)
#对数据的删除操作
# df = df[[col for col in df.columns if 'Unnamed' not in col]] #去除unname的列
# print(df)
#去除unname的列
df.drop('Unnamed: 0', axis=1, inplace=True)
print(df)

#对数据的查找操作

print(df.loc[:, ["bWendu", 'yWendu']])

print(df.iloc[100])
print(df.loc[100])

#条件查询

print("温度大于35°有", len(df.loc[df["bWendu_num"] > 35]))
print(df[['bWendu', 'yWendu']])
print(df["yWendu"])
print("="*50)
print(df.iloc[1:2, 1:2])
print(df.loc[:, ["yWendu", 'bWendu', 'aqi_pingjia']])
print(df.loc[[1, 2, 3]])
print(df[(df["ymd3"] > 2)])



