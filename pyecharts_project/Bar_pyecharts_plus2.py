import seaborn as sns
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Scatter, Bar
from pyecharts.globals import ThemeType
from pathlib import Path

df = pd.read_csv(r'D:\python_demo\coding\pyecharts_project\data\austria_tfr_data.csv')
#计算生育率的同比变化
print(df.columns.tolist())
df['Change'] = df['Total Fertility Rate'].diff()
#将变化值放大1000倍并取值
df['Change_Value'] = (df['Change'] * 1000).round(0)
df = df.dropna()
years = df['Year'].astype(str).tolist()
changes = df['Change'].tolist()
change_values = df['Change_Value'].astype(int).tolist()
tfr_values = df['Total Fertility Rate'].tolist()

colors = ["#FF9999" if c >= 0 else "#9999FF" for c in changes]

bar = (
    Bar(
        init_opts=opts.InitOpts(
            width="1000px",
            height="600px",
            theme=ThemeType.DARK,
            bg_color="#2c2E3E"
        )
    )
    .add_xaxis(years)
    .add_yaxis(
        series_name="生育率变化值（放大1000倍）",
        y_axis=change_values,
        label_opts=opts.LabelOpts(
            is_show=True,  # 显示标签
            position='inside',  # 标签位置：柱子内部
            formatter="{c}",  # 标签内容格式化
            font_size=10,
            color="#FFFFFF",
        ),
        itemstyle_opts=opts.ItemStyleOpts(color='#FF9999'),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title='生育率变化值（放大1000倍）',
            subtitle='奥地利历年生育率变化分析',
            pos_left='center',
            pos_top='3%', #上移避免与图例重叠
            title_textstyle_opts=opts.TextStyleOpts(font_size=20, color='#FFFFFF'), #主标题样式
            subtitle_textstyle_opts=opts.TextStyleOpts(font_size=14, color='#FFFFFF') #副标题样式
        ),
        xaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(rotate=45, font_size=10),
            name='年份',
            name_textstyle_opts=opts.TextStyleOpts(color='#FFFFFF')
        ),
        yaxis_opts=opts.AxisOpts(
            name='变化值（x1000）', #说明y轴放大比例
            name_textstyle_opts=opts.TextStyleOpts(color="#FFFFFF"), #x轴名称颜色：白色
            axislabel_opts=opts.LabelOpts(color="#FFFFFF") #轴标签颜色：白色
        ),
        #提示框配置
        tooltip_opts=opts.TooltipOpts(
            trigger='axis',
            formatter="{b}<br/>变化值：{c}"
        ),
        datazoom_opts=[
            opts.DataZoomOpts(
                type_='slider',
                range_start=0,
                range_end=100,
                pos_bottom='5%'
            ),
            opts.DataZoomOpts(
                type_='inside'
            )
        ],
        legend_opts=opts.LegendOpts(
            pos_top='12%',
            pos_left='center',
            textstyle_opts=opts.TextStyleOpts(color="#FFFFFF")
        )
    ).set_series_opts(
        markpoint_opts=opts.MarkPointOpts(
            data=[
                opts.MarkPointItem(type_='max', name='最大值'),
                opts.MarkPointItem(type_='min', name='最小值')
            ],
            label_opts=opts.LabelOpts(color="#FFFFFF")
        )
    )
)

# 确保输出目录存在并保存
out_path = Path("html/austria_tfr_changes.html")
out_path.parent.mkdir(parents=True, exist_ok=True)
bar.render(str(out_path))
print("已生成")
print("关键信息统计")