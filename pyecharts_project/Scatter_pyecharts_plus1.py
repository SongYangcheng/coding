import json #在地图可视化中可使用
import pandas as pd
import numpy as np
from pyecharts.charts import Scatter, Bar
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode

data = pd.read_csv(r'D:\python_demo\coding\pyecharts_project\data\GLB.Ts+dSST.csv')
#将数据从宽表转换为长表
print(data.head())
dt = data.iloc[:, :13].melt(id_vars='Year') #宽表转长表
print(dt.head())
maps = dict(zip(data.iloc[:, 1:13].columns.tolist(), range(1, 13))) #月份映射为数字
dt['month'] = dt['variable'].map(maps)
dt['date'] = pd.to_datetime(dt["Year"].astype(str) + '-' + dt["month"].astype(str)) #生成日期列
dt['date'] = pd.to_datetime(dt['date']).apply(lambda x:x.strftime('%Y-%m')) #格式化日期
#提取日期和温度值
data_pair = dt[['date', 'value']].values.tolist() #提取“date"和”value“

#定义标签格式化函数
label_js = """function(params){
(params >= 0) {
return ('+' + params);}
else {
return params;}}"""
#创建散点图
sca = (
    Scatter(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width='980px'))
    .add_xaxis([i[0] for i in data_pair])
    .add_yaxis("温度变化", [i[1] for i in data_pair], 
               symbol_size=8,
               itemstyle_opts=opts.ItemStyleOpts(
                   border_width=0.5,
                   opacity=0.5
               ),
               markline_opts=opts.MarkLineOpts(
                   data=[opts.MarkLineItem(y=0)],
                     label_opts=opts.LabelOpts(formatter="平均温度线", is_show=True, position="end"),
               ))
    .set_global_opts(title_opts=opts.TitleOpts(title="全球地表温度变化", #设置主标题
                                               subtitle="数据来源：NASA GISS"),#设置副标题
                    legend_opts=opts.LegendOpts(is_show=False),#隐藏图例
                    xaxis_opts=opts.AxisOpts(
                        type_="time",
                        split_number=20,
                        position="bottom",
                        offset=2, #偏移量
                        splitline_opts=opts.SplitLineOpts(is_show=True),
                        axisline_opts=opts.AxisLineOpts(is_show=False),
                        axistick_opts=opts.AxisTickOpts(is_show=False)
                    ),
                    yaxis_opts=opts.AxisOpts(
                        type_="value", #设置y轴类型为数值轴
                        min_=-0.8,
                        max_=1.4,
                        split_number=10,
                        name_gap='40', #轴名称与轴线距离
                        name="温度变化 (°C)",
                        name_textstyle_opts=opts.TextStyleOpts(font_size=14, color="#000000"),#轴名称样式
                        axistick_opts=opts.AxisTickOpts(is_show=False), #不显示轴线
                        splitline_opts=opts.SplitLineOpts(is_show=False), #不显示分割线
                        axislabel_opts=opts.LabelOpts(#显示标签
                            formatter=JsCode(label_js)#使用JS代码格式化标签
                        )
                    ),
                    tooltip_opts=opts.TooltipOpts( #设置提示框
                    trigger='item', #触发类型：数据项图形触发
                    axis_pointer_type='cross'
                    ),      
                    visualmap_opts=opts.VisualMapOpts(is_show=False,
                                      is_calculable=True, #显示拖拽用的手柄
                                      range_color=['blue', 'green', 'yellow', 'red'],
                                      min_=-0.8,
                                      max_=1.4)
                                      )  

    )
sca.render(r'html\Scatter_pyecharts_plus1.html')




