from pandas import DataFrame
import pandas as pd
from sqlalchemy import create_engine

df = DataFrame({
    "班级": ['一年级', '二年级', '三年级'],
    '男生人数': [24, 34, 33],
    '女生人数': [24, 34, 23],
})

# 创建数据库引擎（注意无空格）
engine = create_engine('mysql+pymysql://root:AAAaaa211@127.0.0.1/student')
#数据库的写
df.to_sql('students', engine, if_exists='replace', index=False)
print("创建成功")
#数据库的读
sql_inf = pd.read_sql_table('students', engine)
print(f"使用read_sql_table进行读取{sql_inf}")

#将excel转化为CSV不保留任何索引
excel_df = pd.read_excel('data/beijing_weather_2018.xlsx')
excel_df.to_csv('data/beijing_weather_2018.csv', index=False) #index=False保存时不写入DataFrame
print("Excel文件成功转换为CSV文件")
#读取csv文件，删除残留索引列
df = pd.read_csv('data/beijing_weather_2018.csv')

#清楚残留索引列（unname）
print(df.head())
df = df[[col for col in df.columns if 'Unnamed' not in col]]

# print(df['ymd'])
print(df.shape)
print(df.head())

#设定索引为日期方便按照日期筛选
df.set_index('ymd', inplace=True) #inplace为True时直接修改df返回新元组, 不会修改原始df
#替换温度后缀为℃
df.loc[:, 'bWendu'] = df['bWendu'].str.replace('℃', '').astype('int32')
df.loc[:, 'yWendu'] = df['yWendu'].str.replace('℃', '').astype('int32')

#查询单个值
print(df.loc['2018-01-00', 'bWendu'])
#查询series
print(df.loc[['2018-01-00', "2018-01-01"],"bWendu"])
#查询dataframe
print(df.loc[['2018-01-00', "2018-01-01"], ['yWendu', "bWendu"]])
#按行区间查询
print(df.loc['2018-01-00':'2018-01-02', 'bWendu'])
#按列区间进行查询
print(df.loc['2018-01-00', 'bWendu':'yWendu'])
#行列区间都可以
print(df.loc['2018-01-00':'2018-01-02', 'bWendu':'yWendu'])
#简答查询
print(df.loc[df['yWendu'] < 10, :])

print(df.loc[(df['bWendu'] > 10) & (df['yWendu']) < 30 & (df['tianqi']=='晴')])

#直接写lambda表达式
print(df.loc[lambda df: (df['bWendu'] >= 15) & (df['yWendu'] >= 15), :])
#编写自己的函数
def query_my_data(df):
    return df.index.str.startswith('2018-01-00') & df['aqiLevel'] == 1
print(query_my_data(df).head())
