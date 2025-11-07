from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType
from pathlib import Path

x_data = ['直线访问', "邮箱营销", "广告轰炸", "视频广告", "搜索分享"]
y_data = [335, 310, 234, 135, 1548]
data_pair = [list(z) for z in zip(x_data, y_data)]
data_pair.sort(key=lambda x: x[1])

pie = (
    Pie(init_opts=opts.InitOpts(bg_color="#2c343c"))
    .add(
        series_name='访问来源',
        data_pair=data_pair,
        rosetype="area",  # 玫瑰饼图，area 为面积模式（推荐），radius 为半径模式
        radius=["30%", "75%"],  # 外圆半径和内圆半径，使其成为环形玫瑰图
        center=["50%", "50%"],
        label_opts=opts.LabelOpts(is_show=True, position="outside"),  # 显示标签在外部
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="玫瑰饼图", 
            pos_left="center",  # 标题水平位置
            pos_top="20",  # 标题位置
            title_textstyle_opts=opts.TextStyleOpts(
                color="#fff",
                font_size=24,
            ),
        ),
        legend_opts=opts.LegendOpts(
            orient="vertical",
            pos_top="15%",
            pos_left="2%",
            textstyle_opts=opts.TextStyleOpts(color="#fff"),
        ),
    )
)

# 确保输出目录存在
out_dir = Path('html')
out_dir.mkdir(parents=True, exist_ok=True)
out_file = out_dir / 'pie_pyecharts_flower.html'

try:
    pie.render(str(out_file))
    print(f"玫瑰饼图已生成：{out_file}")
except Exception as e:
    print(f"生成玫瑰饼图失败：{e}")