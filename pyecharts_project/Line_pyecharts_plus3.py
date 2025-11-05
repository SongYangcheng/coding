#填充颜色

from pyecharts.charts import Line
from pyecharts import options as opts
from pyecharts.globals import ThemeType, JsCode
import pandas as pd
from pathlib import Path

#读取Excel文件
data = pd.read_excel(r"D:\python_demo\coding\pyecharts_project\data\subject1.xlsx")
print(data.head())

data['Month'] = data['Month'].apply(lambda x: x.strftime('%Y-%m'))
data_pair = data[data['Name'] == 'AI-NLP'][['Month', 'Average', 'Peak']].values.tolist()

#自定义线条样式（使用 LineStyleOpts）
line_style_1 = {
    "normal": {
    "type_":'solid',  # 实线
    "color":'#FF5733',    
    "shadowOffsetY":2, #阴影垂直偏移
    "shadowOffsetX":2, #阴影水平偏移
    "shadowBlur":10, #阴影模糊大小
    "shadowColor":'rgba(0, 0, 0, 0.3)', #阴影颜色
    }
}

line_style_2 = {
    "normal": {
    "type_":'dashed',  # 虚线
    "color":'#33FF57',
    "shadowOffsetY":2, #阴影垂直偏移
    "shadowOffsetX":2, #阴影水平偏移
    "shadowBlur":10, #阴影模糊大小
    "shadowColor":'rgba(0, 0, 0, 0.3)', #阴影颜色
    }
}
#自定义区域填充颜色
area_style_1 = {
    "normal": {
        "color": JsCode("""new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {offset: 0, color: 'rgba(255, 87, 51, 0.5)'},
            {offset: 1, color: 'rgba(255, 87, 51, 0)'} 
        ])"""),
        "opacity": 0.8,
        "shadowColor": 'rgba(255, 87, 51, 0.5)',
        "shadowBlur": 10,
    }
}
area_style_2 = {
    "normal": {
        "color": JsCode("""new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {offset: 0, color: 'rgba(51, 255, 87, 0.5)'},
            {offset: 1, color: 'rgba(51, 255, 87, 0)'}
        ])"""),
        "opacity": 0.8,
        "shadowColor": 'rgba(51, 255, 87, 0.5)',
        "shadowBlur": 10,
    }
}
#创建折线图
line = (
    Line(init_opts=opts.InitOpts(theme=ThemeType.DARK))
    .add_xaxis([item[0] for item in data_pair[::-1]])
    .add_yaxis('平均在线人数', [item[1]/1000 for item in data_pair[::-1]],
               is_smooth=True, #平滑曲线
               is_symbol_show=False, #不显示数据点符号
               linestyle_opts=line_style_1,
               areastyle_opts=area_style_1 #⚠️关键代码设置区域填充样式
               ) #应用自定义样式
    .add_yaxis('峰值在线人数', [item[2]/1000 for item in data_pair[::-1]],
               is_smooth=True, #平滑曲线
               is_symbol_show=False, #不显示数据点符号
               linestyle_opts=line_style_2,
               areastyle_opts=area_style_2 #⚠️关键代码设置区域填充样式
               ) #应用自定义样式
    .set_global_opts( #全局配置项
        title_opts=opts.TitleOpts(#设置标题
        title="基础折线图",
        pos_top='3%', #上移避免与图例重叠
        pos_left='center',
        ),
        tooltip_opts=opts.TooltipOpts( #设置提示框
            trigger="axis", #触发类型：轴触发还可选择'item'项触发
            axis_pointer_type="cross", #指示器类型：十字准星还可以选择'line'直线
        ),
        visualmap_opts=opts.VisualMapOpts( #设置区域颜色划分
            is_show=False, #隐藏visualmap组件
            is_piecewise=True,#区域分段显示
            pieces=[{
                "min": 0,
                "max": 300,
                "color": "#93CE07"
            },
                {
                    "min": 300,
                    "max": 600,
                    "color": "#FBDB0F"
                },
                {
                    "min": 600,
                    "max": 900,
                    "color": "#FC7D02"
                },
                {
                    "min": 900,
                    "max": 1500,
                    "color": "#FD0100"
                }]
        ),
        yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)) #显示y轴分割线
    )
    .set_series_opts( #设置系列配置项
        label_opts=opts.LabelOpts(is_show=False), #不显示标签
        markpoint_opts=opts.MarkPointOpts( #显示最大值和最小值
            data=[
                opts.MarkPointItem(type_="max", name="最大值"),
                opts.MarkPointItem(type_="min", name="最小值"),
            ]),
    )
)

# 确保输出目录存在
out_dir = Path('html')
out_dir.mkdir(parents=True, exist_ok=True)
out_file = out_dir / 'Line_pyecharts_plus3.html'

try:
    line.render(str(out_file))
    print(f"折线图已成功生成：{out_file}")
except Exception as e:
    print(f"生成折线图失败：{e}")