from pandas import DataFrame
import pandas as np
from sqlalchemy import create_engine

df = DataFrame({
    "班级": ['一年级', '二年级', '三年级'],
    '男生人数': [24, 34, 33],
    '女生人数': [24, 34, 23],
})

# 创建数据库引擎（注意无空格）
engine = create_engine('mysql+pymysql://root:AAAaaa211@127.0.0.1/student')

df.to_sql('students', engine, if_exists='replace', index=False)
print("创建成功")

sql_inf = np.read_sql_table('students', engine)
print(sql_inf)