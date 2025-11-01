#coding:UTF-8
from snapshot_selenium import snapshot #使用selenium爬取网页截图
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.render import make_snapshot

def bar_chart() -> Bar: #自定义函数，将该函数的对象作为Bar ->为返回类型
    c = (
        Bar()
        .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
        .add_yaxis("商家B", [15, 25, 16, 55, 45, 70])
        .reversal_axis() #交换X轴和Y轴
        .set_global_opts(
            legend_opts = opts.LegendOpts(pos_right="10%", pos_top="20%"), #图例位置
            title_opts=opts.TitleOpts(title="商品销量统计", subtitle="双商家对比"),
        )
    )
    return c
#利用爬虫库,保存图片
make_snapshot(snapshot, bar_chart().render(r"html\bar_chart.html"), r"images\bar_chart.png")
print('OVER')