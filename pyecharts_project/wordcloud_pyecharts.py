import pandas as pd
from pyecharts.charts import WordCloud
from pyecharts import options as opts
import ast

with open(r'D:\python_demo\coding\pyecharts_project\data\网页-词云图数据.txt', 'r', encoding='utf-8') as f:
        content = f.read()

# 将字符串转换为列表，并将数值字符串转为整数
data_list = ast.literal_eval(content)
data = [(word, int(value)) for word, value in data_list]
(
    WordCloud()
    .add(series_name="热点分析", data_pair=data, word_size_range=[6, 66])
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="热点词云图",
            title_textstyle_opts=opts.TextStyleOpts(font_size=23),
        ),
        tooltip_opts=opts.TooltipOpts(is_show=True),
    )
    .render(r"html/热点词云图.html")
)