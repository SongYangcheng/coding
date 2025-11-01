#coding:utf-8
from pyecharts.charts import Bar, Line
from pyecharts import options as opts

x_data = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月']

bar = (
    Bar()
    .add_xaxis(xaxis_data=x_data)
    .add_yaxis(
        series_name='蒸发量',
        y_axis=[2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3],
        label_opts=opts.LabelOpts(is_show=False), #不显示图例
    )
    .add_yaxis(
        series_name='降水量',
        y_axis=[2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3],
        label_opts=opts.LabelOpts(is_show=False), #不显示图例
    )
    .add_yaxis(
        series_name='平均温度',
        y_axis=[2.0, 2.2, 3.3, 4.5, 6.3, 10.2, 20.3, 23.4, 23.0, 16.5, 12.0, 6.2],
        label_opts=opts.LabelOpts(is_show=False), #不显示图例

    )
    .extend_axis(
        yaxis=opts.AxisOpts(
            name="平均温度",
            type_="value",
            min_="0",
            max_='25',
            interval=5,
            axislabel_opts=opts.LabelOpts(formatter="{value} °C"),
        )
    )
    .set_global_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger="axis",
            axis_pointer_type="cross"
        ),
        xaxis_opts=opts.AxisOpts(type_='category',
                                axispointer_opts=opts.AxisPointerOpts(is_show=True,
                                                                    type_="shadow")),
        yaxis_opts=opts.AxisOpts(
            name="水量",
            type_='value',
            min_='0',
            max_='250',
            interval=50,
            axislabel_opts=opts.LabelOpts(formatter="{value} ml"),
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
    )
)
line  = (
    Line() #同柱形图一样
    .add_xaxis(xaxis_data=x_data)
    .add_yaxis(
        series_name="平均温度",
        y_axis=[2.0, 2.2, 3.3, 4.5, 6.3, 10.2, 20.3, 23.4, 23.0, 16.5, 12.0, 6.2],
        yaxis_index=1, #指定使用的y轴
        label_opts=opts.LabelOpts(is_show=False), #不显示图例
        linestyle_opts=opts.LineStyleOpts(color="#ff0000"),
    )
)
bar.overlap(line).render(r"html/柱形图图表.html") #重叠柱形图和折线图
