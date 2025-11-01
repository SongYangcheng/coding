from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.faker import Faker #引入Faker模块生成数据

bar = (
    Bar()
    .add_xaxis(Faker.choose()) #生成X轴数据
    .add_yaxis("商家A", Faker.values()) #生成Y轴数据
    .add_yaxis("商家B", Faker.values()) #生成Y轴数据

    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例"))
    .render(r"html\bar_chart_faker.html")
)
print('OVER')