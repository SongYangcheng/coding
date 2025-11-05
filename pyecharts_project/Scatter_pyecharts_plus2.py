import json #在地图可视化中可使用
import pandas as pd
import numpy as np
from pyecharts.charts import Scatter, Bar
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode
#读取CSV文件中的汽车数据
data = pd.read_csv(r'D:\python_demo\coding\pyecharts_project\data\cars.csv')
#数据处理，车名(name),燃油效率(mpg), 发动机功能(hp)
#将数据转换为别表格式，每一行是[车名, 燃油效率, 发动机功能]
data_pair = data[['name', 'mpg', 'hp']].values.tolist()
#查看处理后的数据格式
for i in range(3):
    print(data_pair[i])

#=======自定义JavaScript格式化函数========
#标签格式化函数
label_js = """
function(params){
console.log(params);
return params.data[2]}"""
#提示框格式化函数
tooltip_js = """
function(params){
console.log(params);
return params.data[0] +
'<br/>燃油效率: ' + params.data[1] +
'<br/>发动机功能: ' + params.data[2];
}"""

#=======定义样式=======
#散点样式：粉色圆点
style_1 = {
    "color": 'pink', #点颜色
    'border_color': 'rgba(255, 105, 180, 0.8)', #边框颜色
    'border_width': 1, #边框宽度
    'opacity': 0.7, #点透明度
}
#========创建散点图========
sca = (
    Scatter(
        init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width='1200px', height='700px')

    )
    .add_xaxis([i[1] for i in data_pair]) #燃油效率(mpg)
    .add_yaxis(
        series_name="汽车信息",
        #Y轴数据：发动机功率(hp)
        #这里X是mpg， Y是hp
        y_axis=[i[2] for i in data_pair], #发动机功能(hp)
        symbol_size=10, #点大小
        #标签配置
        label_opts=opts.LabelOpts(
        formatter=JsCode(label_js),
        position='top', #标签在散点的上方
        distance=4, #标签与散点的距离
        font_size=10, #标签字体大小
        ),#散点样式配置
        itemstyle_opts=opts.ItemStyleOpts(**style_1)
    )
    .set_global_opts(
        xaxis_opts=opts.AxisOpts(
            type_='value',
            min_=10,
            max_=35,
            split_number=12,
            name='燃油效率 (mpg)',
            name_location='top',#名称位置：顶部
            name_gap=30, #名称与轴线距离
            axisline_opts=opts.AxisLineOpts(
                is_show=True,
            ),
            splitline_opts=opts.SplitLineOpts(is_show=True)#显示分割线
        ),
        yaxis_opts=opts.AxisOpts(
            type_='value',
            min_=40,
            max_=360,
            split_number=10,
            name='发动机功能 (hp)',
            name_gap=50,
            axisline_opts=opts.AxisLineOpts(
                is_show=True
            ),
            splitline_opts=opts.SplitLineOpts(is_show=True),#显示分割线
        ),
        title_opts=opts.TitleOpts(
            title='汽车燃油效率与发动机功能散点图',
            pos_left='center',
            title_textstyle_opts=opts.TextStyleOpts(
                font_size=20,
            )
        ),
        #配置图例 - 避免遮挡三代你
        legend_opts=opts.LegendOpts(
            pos_top='65%',
            pos_left='center',
        ),
        #鼠标悬停显示的信息
        tooltip_opts=opts.TooltipOpts(
            formatter=JsCode(tooltip_js),
            trigger='item',
            axis_pointer_type='cross', #指示器

    ),
    toolbox_opts=opts.ToolboxOpts(
        is_show=True,
        feature={
            "saveAsImage": {},
            "dataZoom": {},
            "restore": {},
            "dataView": {}
        }
    ),
    )
)
#渲染图表
#保存为HTML文件
sca.render(r'html\Scatter_pyecharts_plus2.html')
