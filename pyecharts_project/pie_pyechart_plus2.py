from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType

c = (
    Pie()
    .add_dataset(
        source=[
            ["产品", "2012", "2013", "2014", "2015", "2016", "2017"],
            ["衬衫", 43.3, 85.8, 93.7, 95.5, 102.9, 130.6],
            ["羊毛衫", 83.1, 73.4, 55.1, 82.5, 105.2, 92.3],
            ["雪纺衫", 86.4, 65.2, 82.5, 89.7, 83.5, 106.6],
            ["裤子", 72.4, 53.9, 39.1, 41.1, 47.2, 48.7],
            ["高跟鞋", 72.4, 53.9, 39.1, 41.1, 47.2, 48.7],
            ["袜子", 52.4, 39.9, 29.1, 29.1, 34.2, 37.7],
        ]
    )
    .add(
        series_name='衬衫',
        data_pair=[],#指定数据
        radius=[30, 60],#半径范围30-60
        center=["25%", "50%"],
        encode={"itemName": "产品", "value": "2012"},#指定使用哪一列数据
    )
    .add(
        series_name='衬衫',#指定系列名称
        data_pair=[],#数据留空
        radius=60,#半径
        center=["50%", "75%"],#图表位置50%水平，75%垂直
        encode={"itemName": "产品", "value": "2013"},
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Pie-使用数据集设置数据")
    )
    .render("html/pie_pyechart_plus2.html")
)