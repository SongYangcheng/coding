import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
df = pd.read_csv(r'D:\python_demo\coding\data\new_accidents.csv', encoding='utf-8')
print(df.columns.tolist())
df = df.dropna().reset_index(drop=True) #drop=True表示重置索引
df['事故时间'] = pd.to_datetime(df['accidenttime']).dt.hour
plt.rcParams['font.family'] = ['SimHei', 'Times New Roman']
df['时段'] = df['事故时间'].apply(lambda x: '白天' if x >= 6 and x < 20 else '夜间')
df['时段1'] = df['事故时间'].apply(lambda x: 0 if x <= 12 and x >=0 else 1)
#将天气情况以/分割为列表形式
df['天气状况'] = df['天气状况'].str.split('/')
#用时间判断天气上午为0下午为1
df['天气状况'] = df.apply(lambda x: x['天气状况'][0] if x['时段1'] == 0 else x['天气状况'][1], axis=1)
# 双条形图分为白天和夜间两部分
# 先计算各类别，并保证白天/夜间都包含相同的类别顺序（缺失的填 0）
day_weather = df[df['时段'] == '白天']['天气状况'].value_counts()
night_weather = df[df['时段'] == '夜间']['天气状况'].value_counts()

# 合并索引（保持出现顺序），并按该索引重建序列，缺失填 0
categories = day_weather.index.union(night_weather.index) #union方法合并两个索引
day = day_weather.reindex(categories, fill_value=0)
night = night_weather.reindex(categories, fill_value=0)

fig, axes = plt.subplots(figsize=(10, 6), dpi=200, facecolor='white')
width = 0.35
x = np.arange(len(categories))

# 绘制并调整柱子位置, 面向对象方法
axes.bar(x - width/2, day.values, width=width, color='skyblue', label='白天')
axes.bar(x + width/2, night.values, width=width, color='lightcoral', label='夜间')
#面向pyplot方法
plt.title('不同天气状况下的事故数量分布', fontsize=16)
plt.xlabel('天气状况', fontsize=14)
plt.ylabel('事故数量', fontsize=14)

# 在柱子上添加数值标签
for xi, v in zip(x - width/2, day.values):
    axes.text(xi, v + max(day.max(), night.max())*0.02 + 1, str(int(v)), ha='center', fontsize=10)
for xi, v in zip(x + width/2, night.values):
    axes.text(xi, v + max(day.max(), night.max())*0.02 + 1, str(int(v)), ha='center', fontsize=10)

plt.legend()
plt.xticks(x, categories, rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.show()