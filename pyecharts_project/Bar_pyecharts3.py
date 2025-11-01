from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode #引入JsCode类其中可以写js代码设置图表样式
from pyecharts.globals import ThemeType #引入主题类型

list1 = [
    {"value": 335, "name": "直接访问"},
    {"value": 310, "name": "邮件营销"},
    {"value": 234, "name": "联盟广告"},
    {"value": 135, "name": "视频广告"},
    {"value": 1548, "name": "搜索引擎"},
]
list2 = [
    {"value": 325, "name": "直接访问"},
    {"value": 310, "name": "邮件营销"},
    {"value": 234, "name": "联盟广告"},
    {"value": 135, "name": "视频广告"},
    {"value": 1548, "name": "搜索引擎"},
]
list3 = [
    {"value": 315, "name": "直接访问"},
    {"value": 320, "name": "邮件营销"},
    {"value": 234, "name": "联盟广告"},
    {"value": 145, "name": "视频广告"},
    {"value": 1348, "name": "搜索引擎"},
]
c = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT)) #主题必须在初始化时设置
    .add_xaxis([1, 2, 3, 4, 5])
    .add_yaxis(
        "产品A",
        list1,
        stack="stack1", #堆叠系列名称相同
        category_gap="50%", #类目间柱子距离
    )
    .add_yaxis(
        "产品B",
        list2,
        stack="stack1", #堆叠系列名称相同
        category_gap="50%", #类目间柱子距离
    )
    .add_yaxis(
        "产品C",
        list3,
        stack="stack1", #堆叠系列名称相同
        category_gap="50%", #类目间柱子距离
    )
    .set_series_opts(
        label_opts=opts.LabelOpts( #设置文本标签
            position="right",
            formatter=JsCode(
                "function(x){return Number(x.data.value).toFixed(0);}" #js代码设置标签格式,toFixed(0)表示不保留小数
            ),
    )
)
    .render(r"html\bar_chart.html")
)