from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType

c = (
    Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, bg_color="#f2f2f2"))
    .add(
        "",
        [list(z) for z in zip(Faker.week, Faker.values())],
        center=["50%", "50%"],#图表位置50%水平，50%垂直
        radius=["50%", "80%"],#半径范围50-80
    )
    # .set_colors(["#5470C6", "#91CC75", "#FAC858", "#EE6666", "#73C0DE", "#3BA272", "#FC8452"])

    .set_global_opts(
        title_opts=opts.TitleOpts(title="Pie-使用数据集设置数据")
    )
    .render("html/pie_pyecharts_plus3.html")
)