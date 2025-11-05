import json #在地图可视化中可使用
import pandas as pd
import numpy as np
from pyecharts.charts import Scatter, Bar
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode

data = pd.read_excel(r'D:\python_demo\coding\pyecharts_project\data\subject1.xlsx')
data_pair = data[['Month', 'Average', 'Peak']].copy()
def to_numeric(value):
    try:
        return float(value)
    except:
        return 0.0
    
data_pair['Average'] = data_pair['Average'].apply(to_numeric)
data_pair['Peak'] = data_pair['Peak'].apply(to_numeric)

#去重
data_pair.drop_duplicates(subset=['Month'], keep='first', inplace=True) #去除重复保留第一次出现的行

#pd.date_range():生成时间序列
#start=data_pair['Month'].min()：起始时间
#end=data_pair['Month'].max()：结束时间
#freq='MS'：频率为每月开始
#strftime('%Y-%m')：格式化为'年-月'
all_months = pd.date_range(start=data_pair['Month'].min(), end=data_pair['Month'].max(), freq='MS').strftime('%Y-%m').tolist()
all_months = [month for month in all_months]
data_pair.set_index('Month', inplace=True)#set_index():设置索引, inplace=True:在原数据上修改
#reindex():重新索引, fill_value=0:缺失值填充为0
#reset_index():重置索引,转为数据表格中的第一列
data_pair = data_pair.reindex(all_months, fill_value=0).reset_index().rename(columns={'index': 'Month'})
print(data_pair.head())
data_pair = data_pair.values.tolist()
#定义样式
style_1 = {
    'normal': {
        'color': '#FFA500',
        'shadowBlur': 0,
        'shadowColor': '#FFA500',
        'shadowOffsetX': 0,
        'shadowOffsetY': 0, # 阴影Y轴偏移
        'width': 0,
        'opacity': 1  # 点的透明度
    }
}
style_2 = {
    'normal': {
        'color': "#2FFF00",
        'shadowBlur': 0,
        'shadowColor': '#2FFF00',
        'width': 0,
        'opacity': 1  # 点的透明度
    }
}
#创建散点图
sca = (
    Scatter(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, bg_color="#FFFFFF"))
    .add_xaxis([i[0] for i in data_pair])
    .add_yaxis(
        "平均在线",
        [i[1]/10000 for i in data_pair],
        symbol_size=8,
        itemstyle_opts=style_1,
    )
    .add_yaxis(
        '竞赛在线峰值',
        [i[2]/10000 for i in data_pair],
        symbol_size=8,
        symbol='circle',
        itemstyle_opts=style_2,
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title='多数据系列散点图'),
        tooltip_opts=opts.TooltipOpts(
            trigger='axis', axis_pointer_type='cross'
        ),
        xaxis_opts=opts.AxisOpts(
            type_='category',
            boundary_gap=False
        ),
        yaxis_opts=opts.AxisOpts(
            type_='value',
            splitline_opts=opts.SplitLineOpts(is_show=True),
            axislabel_opts=opts.LabelOpts(formatter="{value} 万"),
        ),
    )
    .set_series_opts(
        label_opts=opts.LabelOpts(is_show=False)
    )
)
sca.render(r'html/Scatter_pyecharts_plus3.html')