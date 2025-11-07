from pyecharts import options as opts
from pyecharts.charts import Map, Geo, Bar, Grid
from pyecharts.globals import ChartType, SymbolType
from pyecharts.commons.utils import JsCode
import pandas as pd
import requests
import json

with open(r'data/word_data.txt', 'r', encoding='utf-8') as f:
    data_pair = json.load(f)

maps = (
    Map()
    .add('累计确诊',
         data_pair,
         'world')
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(), # 配置视觉映射组件
        title_opts=opts.TitleOpts(title='全球累计确诊病例分布')
    )
    .set_series_opts( # 设置系列选项
        label_opts=opts.LabelOpts(is_show=False) # 不显示标签

    )
).render('html/world_map.html')

#绘制Geo图
country_list = ['China', 'United States', 'Brazil', 'United Kingdom', 'Canada', 'Russia', 'India', 'Spain', 'Peru', 'Italy']
data_pair = [[x, y] for x, y in data_pair if x in country_list]

ftm_js = """ function(params){
return params.name + ' : '  + Number(params.value[2]);
} """
#从coord.txt中加载坐标数据
with open('data/crood_fixed.json', 'r', encoding='utf-8') as f:
    data_loc = json.load(f)
print(data_loc)
geo = (
    Geo(
        init_opts=opts.InitOpts(width="1200px", height="800px"),
        is_ignore_nonexistent_coord=True, # 忽略不存在的坐标点
    )
    .add_schema(maptype="world", # 使用世界地图
                is_roam=True, # 允许缩放和平移
                itemstyle_opts=opts.ItemStyleOpts( # 设置地图区域样式
                    area_color='#091632', #区域填充颜色
                    border_color='#1773c3', #地图边界颜色
                    opacity=1, # 透明度
                ))
)
#添加自定义坐标
for k, v in data_loc.items():
    geo.add_coordinate(k, v[0], v[1])

#添加涟漪散点效果
geo.add(
    "",
    data_pair,
    type_=ChartType.EFFECT_SCATTER # 涟漪散点图
)
#设置系列选项
geo.set_series_opts(
    label_opts=opts.LabelOpts( #  标签选项
        is_show=False,
        formatter=JsCode(ftm_js), # 使用JavaScript格式化标签
        position="right",
        color="#fff",
        font_size=12,
        font_weight='bold'
    )
)
#设置全局选项
geo.set_global_opts(
    title_opts=opts.TitleOpts(
        title="全球累计确诊病例分布及主要国家疫情情况",
        pos_left="center",
        title_textstyle_opts=opts.TextStyleOpts(color="#fff", font_size=20)
    ),
    visualmap_opts=opts.VisualMapOpts(
        min_=0,
        max_=10000000,
        range_text=["High", "Low"],
        is_calculable=True,
        pos_left="left",
        pos_bottom="center",
        textstyle_opts=opts.TextStyleOpts(color="#fff")
    )
)
geo.render('html/world_geo.html')
#创建柱形图对象
bar = Bar()
#添加x轴数据（国家名称）
bar.add_xaxis([x[0] for x in data_pair])
bar.add_yaxis(
    "",
    [i[1] for i in data_pair],
    itemstyle_opts=opts.ItemStyleOpts(
        border_color="#3398DB",
        opacity=0.7,
    )
)
#设置系列选项
bar.set_series_opts(
    label_opts=opts.LabelOpts(
        is_show=False,
        position="top",
        font_size=12,
        font_weight='bold',
        formatter='{d}: {c}' # 标签格式化b为国家名称，c为对应数值，d为排名
    )
)
#设置全局选项
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts( # x轴选项
        is_show=True,
    ),
    yaxis_opts=opts.AxisOpts( # y轴选项
        is_show=True,
    ),
    title_opts=opts.TitleOpts( # 标题选项
        title='Top10国家累计确诊病例数',
        pos_top='55%',
        pos_left='5%',
        title_textstyle_opts=opts.TextStyleOpts(font_size=12)
    ),
    visualmap_opts=opts.VisualMapOpts(
        is_show=False,
        max_=2e5,
        is_piecewise=False, # 是否分段
        dimension=1, # 根据x轴维度进行映射1代表y轴
        range_color=['rgba(219, 112, 147, 0.4)', 'rgba(238, 25, 27, 1)'],
    )
)
#反转坐标轴
bar.reversal_axis()
#创建Grid对象
grid = (
    Grid(
        init_opts=opts.InitOpts(width="1200px", height="800px")
    )
    #先添加柱形图，再添加Geo图

    .add(bar, grid_opts=opts.GridOpts(pos_top="60%", height="35%" ))  # 添加柱形图到Grid
    .add(geo, grid_opts=opts.GridOpts())  # 添加Geo图到Grid
).render("html/world_geo_bar.html")