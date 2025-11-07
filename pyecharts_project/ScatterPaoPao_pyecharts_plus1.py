import json #在地图可视化中可使用
import pandas as pd
import numpy as np
from pyecharts.charts import Scatter, Bar
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode
from pathlib import Path

data = pd.read_excel(r'D:\python_demo\coding\pyecharts_project\data\1990-2015_GDP.xlsx')
data['GDP'] = data['GDP'].astype(int)/2000
data['all_GDP'] = data['all_GDP'].astype(int)
data['life'] = data['life'].astype(int)
print(data[['GDP', 'all_GDP', 'life']])
print(data['country'].unique())

data_x = data[data['year']==1990]['GDP'].tolist()
data_y = data[data['year']==1990]['life'].tolist()

#数据正常显示
dt = data[data['year']==1990][['GDP', 'life', 'all_GDP', 'country']].values.tolist()
dt2 = data[data['year']==2015][['GDP', 'life', 'all_GDP', 'country']].values.tolist()

tool_js = """function(param) {return param.seriesName + '-' + param.data[4] + '<br/>'
+ 'GDP: ' + param.data[2] + '<br/>'
+ 'All_GDP: ' + param.data[3] + '<br/>'
+ 'Life: ' + param.data[1];}""" #提示框JS代码
#点渐变色设置
item_color_js = """new echarts.graphic.RadialGradient(0.4, 0.3, 1, [{
    offset: 0,
    color: 'rgba(255, 255, 255, 0.5)'
}, {
    offset: 1,
    color: 'rgba(255, 0, 0, 1)'
}])"""
item_color_js2 = """new echarts.graphic.RadialGradient(0.4, 0.3, 1, [{
    offset: 0,
    color: 'rgba(129, 227, 238)'
}, {
    offset: 1,
    color: 'rgba(0, 191, 255)'
}])""" #点渐变色设置

symbol_js = """function (data) {return Math.sqrt(data[3])/5e4;}""" #点大小计算JS代码
item_style = {#点样式
    'shadowBlur': 10,
    'shadowOffsetX': 0,#阴影X偏移
    'shadowOffsetY': 0,
    'shadowColor': 'rgba(0, 0, 0, 0.5)',
    'color': JsCode(item_color_js) #点颜色
}
item_style2 = { #点样式
    'shadowBlur': 10,
    'shadowOffsetX': 0,#阴影X偏移
    'shadowOffsetY': 5,
    'shadowColor': 'rgba(0, 0, 0, 0.5)',
    'color': JsCode(item_color_js2)
}

#直接使用echarts的配色方案
bg_color_js = """
new echarts.graphic.RadialGradient(0.3, 0.3, 0.8, [{
    offset: 0,
    color: '#f7f8fa'
}, {
    offset: 1,
    color: '#cdd0d5'
}])
"""
scatter = (
    Scatter(init_opts=opts.InitOpts(bg_color=JsCode(bg_color_js)))
    .add_xaxis(data_x)
    .add_yaxis('1990年', [[i[1], i[0], i[2], i[3]] for i in dt],
               itemstyle_opts=item_style, #点样式
               label_opts=opts.LabelOpts(is_show=True), #显示标签
               symbol_size=JsCode(symbol_js), #点大小，使用js计算
               )
    .add_yaxis('2015年', [[i[1], i[0], i[2], i[3]] for i in dt2],
               itemstyle_opts=item_style2,
               label_opts=opts.LabelOpts(is_show=True),
               symbol_size=JsCode(symbol_js),
               )
    .set_global_opts( #全局配置1
        #y轴配置
        yaxis_opts=opts.AxisOpts(name='人均寿命', type_='value', is_scale=True, #is_scale:不强制从0开始
                                 splitline_opts=opts.SplitLineOpts(is_show=True), #显示分割线
                                #  linestyle_opts=opts.LineStyleOpts(type_='dashed') #虚线
                                 ),
        #x轴配置
        xaxis_opts=opts.AxisOpts(name='GDP', type_='value',
                                is_scale=True, #is_scale:不强制从0刻度开始
                                splitline_opts=opts.SplitLineOpts(is_show=True) #显示分割线4
                                ),
        tooltip_opts=opts.TooltipOpts( #提示框配置
            is_show=True,
            formatter=JsCode(tool_js),
            trigger='item', #触发类型，默认数据项触发
            axis_pointer_type='cross' #指示器类型为十字准星
        ),
        legend_opts=opts.LegendOpts(pos_left='right', pos_top='10%', 
                                    orient='vertical', #图例垂直显示，默认水平
                                    textstyle_opts=opts.TextStyleOpts(font_size=16)),
        title_opts=opts.TitleOpts(title='1990-2015年各国GDP与人均寿命散点图',
                                  #让小标题居中显示
                                  subtitle='数据来源：联合国数据',
                                  pos_top='2%',
                                  pos_left='center',)
    )
)

# 确保输出目录存在
out_dir = Path('html')
out_dir.mkdir(parents=True, exist_ok=True)
out_file = out_dir / 'ScatterPaoPao_pyecharts_plus1.html'

try:
    scatter.render(str(out_file))
    print(f"散点图已生成：{out_file}")
except Exception as e:
    print(f"生成散点图失败：{e}")