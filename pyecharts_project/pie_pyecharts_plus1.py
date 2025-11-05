from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType

c = (
    Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, bg_color="#ffffff"))
    .add("", #为系列名称留空
         [list(z) for z in zip(Faker.week, Faker.values())])#数据处理
         #设置颜色
    # .set_colors(["blue", "green", "yellow", "red", "pink", "orange", "purple"])
    .set_global_opts(title_opts=opts.TitleOpts(title="Pie-设置颜色"))
    #{b}: {c}：{d}表示标签显示名称和对应值,百分比
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}\n{d}%"))
    .render("html/pie_pyecharts_plus1.html")
)