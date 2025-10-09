import pandas as pd
import numpy as np

#生成日期时间索引，模拟六天的销售统计信息
dates = pd.date_range(start="2025-01-01", periods=6, freq="D")

print("========步骤1：生成日期的时间索引===========")
print(dates)

print(f"索引类型：{type(dates)}")

#用numpy数组生成业务数据（模拟电商平台每日4个核心指标）
#指标说明:
#- 订单量(order_count):每日下单总笔数(100-300笔随机)
#- 客单价(avg_order_value):每笔订单平均金额(80-150元随机,保留1位小数)
#- 支付转化率(payment_rate):下单后完成支付的比例(0.85-0.98随机,保留3位小数)
#- 退货率(return_rate):已支付订单中申请退货的比例(0.02-0.08随机,保留3位小数)
np.random.seed(42) # 设置随机种子,确保数据可复现

business_data = np.array([np.random.randint(100, 300, size=6), 
                          np.round(np.random.uniform(80, 150, size=6), 1), #客单价
                          np.round(np.random.uniform(0.85,0.98, size=6), 3),#支付率 
                          np.round(np.random.uniform(0.02, 0.08, size=6), 3),#退货率 
                          ]).T

#生成日期DataFrame
df = pd.DataFrame(data=business_data,
                  index=dates,
                  columns=['order_count', 'avg_order_value', 'payment_rate', 'return_rate'])

print("===========步骤2-3:生成代扣日期索引的电商日销售DataFrame======")

print(df)

#4.验证数据类型并补充业务逻辑

df['order_count'] = df['order_count'].astype(int)
print("========步骤4：修改数据类型=========")
print("数据类型详细")
print(df.dtypes)

#5.基于日期索引的基础业务分析
print('=======步骤5：基于日期索引的业务分析=====')

#筛选1月3日后的销售数据
df_after_jan3 = df[df.index >= '2025-01-03']

print("筛选后的数据为:")
print(df_after_jan3)

df['actual_payment'] = df['order_count'] * df['avg_order_value'] *df['payment_rate']

df['actual_payment'] = df['actual_payment'].round(2) 
print("新增实际支付金额后的指标DataFrame")
print(df[['order_count', 'avg_order_value', 'payment_rate','actual_payment']])

#统计六天内的核心指标均值

print("6天核心指标范围")
print(f"平均日订单量:{df['order_count'].mean():.0f}")
print(f"平均客单价:{df['avg_order_value'].mean():.2f}")
print(f"平均退货率:{df['return_rate'].mean():.2f}")
print(f"平均实际支付:{df['actual_payment'].mean():.2f}")
print(f"平均支付转换率:{df['payment_rate'].mean():.2f}")

print("🤣")
