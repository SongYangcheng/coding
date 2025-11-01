from pyecharts.charts import Bar
from pyecharts import options as opts

bar = (
    Bar()
    .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
    .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
    .add_yaxis("商家B", [15, 25, 16, 55, 45, 70])
    .set_global_opts(
        title_opts=opts.TitleOpts(title="商品销量统计", subtitle="双商家对比"),
        xaxis_opts=opts.AxisOpts(name="商品类型"),
        yaxis_opts=opts.AxisOpts(name="销量")
    )
)
print('hello')
bar.render(r"html\bar_chart.html")