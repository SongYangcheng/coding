from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.faker import Faker
import random

c = (
    Map(init_opts=opts.InitOpts())
    .add("商家A", [list(z) for z in zip(Faker.provinces, Faker.values())],
         "china-cities",
         is_map_symbol_show=True, # 显示地图标记
         label_opts=opts.LabelOpts(is_show=True),# 显示标签   
         )
    # .add("商家B", [list(z) for z in zip(Faker.guangdong_city, Faker.values())],
    #      "china",
    #      is_map_symbol_show=True, # 显示地图标记
    #      label_opts=opts.LabelOpts(is_show=False),# 不显示标签
    #      )
    .set_global_opts(title_opts=opts.TitleOpts(title="Map-基本示例"),
                     visualmap_opts=opts.VisualMapOpts( #颜色映射配置
                         is_show=True,
                         max_=100,
                         min_=0,
                         range_color=["#ffffff", "#ff0000"]
                     ),
                     legend_opts=opts.LegendOpts(is_show=True) #明确显示图例，用于切换商家
                     )
    .render("html/map_base.html")
)