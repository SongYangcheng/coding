from pyecharts.charts import Bar, Line
from pyecharts import options as opts
from pyecharts.faker import Faker

c = (
    Bar()
    .add_xaxis(Faker.choose())
    .add_yaxis("商家A", Faker.days_values, stack="stack1")
    .add_yaxis("商家B", Faker.days_values, stack="stack1")
    .add_yaxis("商家C", Faker.days_values, stack='stack1')

    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例"))
    .render(r"html/多个商家.html")
)