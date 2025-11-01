from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.faker import Faker #引入Faker模块生成数据
from pyecharts.globals import ThemeType #引入主题类型

c = (
    Bar({"theme": ThemeType.DARK}) #主题可以在初始时设置
    .add_xaxis(Faker.choose())
    .add_yaxis('男程序员A', Faker.values())
    .add_yaxis('女程序员B', Faker.values())
    .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例"))
).render(r"html\bar_chart_faker2.html")
print('OVER')