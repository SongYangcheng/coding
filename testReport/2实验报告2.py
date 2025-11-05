import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
np.random.seed(42) #设置随机种子，保证每次生成数据一致
custom_rc = {
    # 字体设置：使用无衬线字体
    "font.family": "sans-serif",
    
    # 脊线设置：去顶/右脊
    "axes.spines.right": False,
    "axes.spines.top": False,
    
    # 网格设置：只显示 y 轴网格，并设置细线
    "axes.grid": True,
    "axes.grid.axis": "y",
    "grid.linestyle": "-",
    "grid.linewidth": 0.5,
    "grid.color": "lightgray"
}

sns.set_theme(
    style="ticks", # 使用 'ticks' 样式作为基础，它默认不显示网格，方便我们自定义
    palette="colorblind", # 设置色盲友好调色板
    font_scale=1.2,       # 全局字体大小缩放因子（统一字号）
    rc=custom_rc          # 传入自定义的 rcParams
)
plt.rcParams['font.family'] = ['SimHei', 'Times New Roman']  #设置中文字体为SimHei
penguins = sns.load_dataset("penguins")
print(penguins.columns.tolist())
penguins = penguins.dropna().reset_index(drop=True)
fig, axes = plt.subplots(1, 2, figsize=(10, 6), dpi=200)

ax = axes[0]
sns.boxplot(
    data=penguins,
    x='species',
    y='body_mass_g',
    ax=ax,
    showfliers=False, # 不显示离群点
)
sns.stripplot(
    data=penguins,
    x='species',
    y='body_mass_g',
    ax=ax,
    jitter=True, #抖动
    alpha=0.5,
    size=5, #点经居中
)
ax.set_title('企鹅体重分布（不含离群点）', fontsize=16)
ax.set_xlabel('物种', fontsize=14)
ax.set_ylabel('体重 (g)', fontsize=14)
ax = axes[1]
sns.violinplot(
    data=penguins,
    x='species',
    y='body_mass_g',
    ax=ax,
    inner='quartile' # 显示四分位数, median为中位数
)
sns.stripplot(
    data=penguins,
    x='species',
    y='body_mass_g',
    ax=ax,
    jitter=True, #抖动
    alpha=0.5,
    size=5, #点经居中
)
plt.suptitle('企鹅体重分布比较', fontsize=20)
ax.set_title('企鹅体重分布（小提琴图）', fontsize=16)
ax.set_xlabel('物种', fontsize=14)
ax.set_ylabel('体重 (g)', fontsize=14)
plt.tight_layout() #调整子图间距，顶部留出标题空间
# plt.savefig(r'D:\python_demo\coding\seaborn_penguin_box_violin.png', dpi=300, bbox_inches='tight') #保存图片
# plt.savefig(r'D:\python_demo\coding\seaborn_penguin_box_violin.svg', bbox_inches='tight') #保存为矢量图
plt.show()
