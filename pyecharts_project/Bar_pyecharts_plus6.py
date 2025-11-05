# -*- coding: utf-8 -*-
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.globals import ThemeType, JsCode #导入主题和样式操作
import pandas as pd
import numpy as np
from pathlib import Path

data = pd.read_excel(r'D:\python_demo\coding\data\奖牌.xlsx')
dt = data.loc[:, ['赛事', '参赛人数']].sort_values(by='参赛人数').values.tolist()
print(dt)
base_itemstyle = {
    'color': "#5470C6",
    'shadowBlur': 10, #阴影模糊大小
    'shadowColor': 'rgba(0, 0, 0, 0.3)', #阴影颜色
    'shadowOffsetX': 2, #阴影水平偏移
    'shadowOffsetY': 2, #阴影垂直偏移
    "borderRadius": [2, 2, 2, 2], #柱子圆角
    'opacity': 1, #不透明度
}

#创建水平柱状图
bar = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    .add_xaxis( #添加X轴数据, 在水平柱状图为纵轴
        [i[0][:5] for i in dt]
    )
    .add_yaxis( #添加Y轴数据
        '参赛人数',
        [i[1] for i in dt],
        itemstyle_opts=base_itemstyle
    )
    .reversal_axis() #交换X轴和Y轴
    .set_series_opts( #系列配置
        label_opts=opts.LabelOpts(
            position='right',
            formatter="{b}:{c}人",
            color='#00c5d2'
        )
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="历年奥运会中国参赛人数",
        ),
        #X轴配置
        xaxis_opts=opts.AxisOpts(
            name='参赛人数'
        ),
        #Y轴配置
        yaxis_opts=opts.AxisOpts(
            name='赛事'
        )
    )
)
out_dir = Path('html')
out_dir.mkdir(parents=True, exist_ok=True)
out_file = out_dir / '历年奥运会中国参赛人数统计柱形图.html'
bar.render(str(out_file))
print(f"图表已生成：{out_file}")  #打印提示信息，告知用户图表已成功生成