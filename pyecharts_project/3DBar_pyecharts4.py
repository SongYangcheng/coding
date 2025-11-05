import pandas as pd
import pandas as pd
import seaborn as sns
from pyecharts import options as opts
from pyecharts.charts import Scatter3D
from pyecharts.globals import ThemeType

# 加载数据
penguins = sns.load_dataset("penguins")
print(penguins.head())

# 只保留需要的列并去掉缺失值
df = penguins[['bill_length_mm', 'body_mass_g', 'flipper_length_mm', 'species']].dropna()

# 定义每个物种的颜色
species_color = {
    "Adelie": "#e74c3c",
    "Chinstrap": "#3498db",
    "Gentoo": "#2ecc71"
}

# 按物种分组，构建每个系列的三维点列表 [x=喙长, y=体重, z=鳍长]
series_points = {}
for species, grp in df.groupby('species'):
    pts = grp.apply(lambda r: [float(r['bill_length_mm']), float(r['body_mass_g']), float(r['flipper_length_mm'])], axis=1).tolist()
    series_points[species] = pts

# 构建 3D 散点图，每个物种作为一个系列（便于分别着色）
scatter3d = Scatter3D(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width="1200px", height="800px"))

for species, pts in series_points.items():
    scatter3d.add(series_name=species,
                  data=pts,
                  symbol_size=8,
                  itemstyle_opts=opts.ItemStyleOpts(color=species_color.get(species, '#888888')))

scatter3d.set_global_opts(
    title_opts=opts.TitleOpts(
        title="企鹅三维散点图",
        subtitle="喙长 vs 体重 vs 鳍长",
        title_textstyle_opts=opts.TextStyleOpts(font_size=20)
    ),
    xaxis3d_opts=opts.Axis3DOpts(name="喙长 (mm)"),
    yaxis3d_opts=opts.Axis3DOpts(name="体重 (g)"),
    zaxis3d_opts=opts.Axis3DOpts(name="鳍长 (mm)")
)

scatter3d.render(r"html/penguins_3d_scatter.html")
