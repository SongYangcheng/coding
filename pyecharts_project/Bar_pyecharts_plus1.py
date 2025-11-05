import seaborn as sns
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar
from pathlib import Path
import webbrowser

# 加载数据并重命名为中文列
diamonds = sns.load_dataset('diamonds')
diamonds = diamonds.rename(columns={
    'cut': '切割质量',
    'price': '价格',
    'color': '颜色等级',
    'clarity': '净度等级',
    'carat': '克拉重量'
})

# 英文到中文映射（切割）
cut_zh_mapping = {
    'Fair': '一般',
    'Good': '好',
    'Very Good': '非常好',
    'Premium': '优质',
    'Ideal': '理想'
}

# 颜色映射
color_zh_mapping = {
    'D': '无色',
    'E': '近无色',
    'F': '近无色',
    'G': '近无色',
    'H': '微黄',
    'I': '微黄',
    'J': '微黄'
}

# 只保留我们关心的颜色等级
common_colors = ['D', 'E', 'F', 'G', 'H']
df = diamonds[diamonds['颜色等级'].isin(common_colors)].copy()

# 映射为中文列，便于展示
df['切割质量中文'] = df['切割质量'].map(cut_zh_mapping)
df['颜色中文'] = df['颜色等级'].map(color_zh_mapping)
print(df.head())
# 计算每组的平均价格,observed=True 输出实际存在的组合
grouped = df.groupby(['切割质量中文', '颜色中文'], observed=True)['价格'].mean().reset_index()
print(grouped.head())
# 指定切割质量的展示顺序（与映射保持一致）+确保包含映射值
cut_order_zh = ['一般', '好', '非常好', '优质', '理想']
grouped['切割质量中文'] = pd.Categorical(grouped['切割质量中文'], categories=cut_order_zh, ordered=True)
grouped = grouped.sort_values('切割质量中文')

# x 轴为切割质量
x_data = cut_order_zh

# 获取颜色系列（中文），保持稳定顺序
color_series = ['无色', '近无色', '微黄']

# 构建每个颜色在每个切割质量下的平均价格列表
y_data_dict = {col: [] for col in color_series}
for cut in x_data:
    sub = grouped[grouped['切割质量中文'] == cut]
    for col in color_series:
        row = sub[sub['颜色中文'] == col]
        y_data_dict[col].append(round(float(row['价格'].values[0]), 2) if len(row) > 0 else 0)

# 颜色映射（中文到色值）
series_color_map = {
    '无色': '#FFD700',
    '近无色': '#C0C0C0',
    '微黄': '#CD7F32'
}

# 构建柱状图
bar = (
    Bar(init_opts=opts.InitOpts(width='1200px', height='720px', bg_color='#ffffff'))
    .add_xaxis(x_data)
)

for color, y_data in y_data_dict.items():
    bar.add_yaxis(
        series_name=f"{color}钻石",
        y_axis=y_data,
        itemstyle_opts=opts.ItemStyleOpts(color=series_color_map.get(color, '#888888')),
        label_opts=opts.LabelOpts(is_show=False)
    )

# 全局样式
bar.set_global_opts(
    title_opts=opts.TitleOpts(
        title='不同切割质量和颜色等级钻石的平均价格',
        subtitle='数据来源：Seaborn Diamonds Dataset',
        pos_top='3%',
        pos_left='center',
        title_textstyle_opts=opts.TextStyleOpts(font_size=20),
        subtitle_textstyle_opts=opts.TextStyleOpts(font_size=12)
    ),
    legend_opts=opts.LegendOpts(pos_top='10%', pos_right='5%', orient='horizontal'),
    xaxis_opts=opts.AxisOpts(
        name='切割质量',
        name_textstyle_opts=opts.TextStyleOpts(font_size=14, padding=[10, 0, 0, 0]),
        axislabel_opts=opts.LabelOpts(rotate=0)
    ),
    yaxis_opts=opts.AxisOpts(
        name='平均价格 (美元)',
        name_textstyle_opts=opts.TextStyleOpts(font_size=14, padding=[0, 0, 10, 0]),
        axislabel_opts=opts.LabelOpts(formatter='{value}')
    ),
    tooltip_opts=opts.TooltipOpts(trigger='axis')
)
# 确保输出目录存在，并把文件路径构造为 URI 在浏览器中打开
out_path = Path(r'html/不同切割质量和颜色等级钻石的平均价格.html')
out_path.parent.mkdir(parents=True, exist_ok=True)
bar.render(str(out_path))
try:
    webbrowser.open(out_path.as_uri())
except Exception:
    # 如果在某些环境中无法自动打开浏览器，不影响文件生成
    pass