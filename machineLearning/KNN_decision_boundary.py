# 【决策边界绘制】
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap
from sklearn import neighbors, datasets

# 设置字体，防止中文乱码（如果系统有Times New Roman则使用，否则可能需要调整）
plt.rcParams['font.sans-serif'] = 'Times New Roman' 

# 【数据导入】
# 导入鸢尾花数据集
iris = datasets.load_iris()

# 只使用前两个特征：萼片长度和萼片宽度
X = iris.data[:, :2]

# 标签的向量
y = iris.target # 3类标签，0-山鸢尾，1-变色鸢尾，2-维吉尼亚鸢尾

# 【绘制网格】
# 生成网格
h = .02  # 网格中的步长

# 计算第一个特征（萼片长度）的最小值和最大值，并稍微扩展范围
x1_min, x1_max = X[:, 0].min() - 0.2, X[:, 0].max() + 0.2

# 计算第二个特征（萼片宽度）的最小值和最大值，并稍微扩展范围
x2_min, x2_max = X[:, 1].min() - 0.2, X[:, 1].max() + 0.2

# 创建网格点矩阵
xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, h), np.arange(x2_min, x2_max, h))

# 【模型训练】
# 近邻数量
k_neighbors = 4  # 设置k近邻算法中k的值，即选择4个最近邻居进行分类
# knn分类器
clf = neighbors.KNeighborsClassifier(k_neighbors)  # 创建k近邻个分类器对象
# 拟合数据
clf.fit(X, y)  # 使用寻来数据X和标签y对分类器进行训练

# 查询点
# np.c_ 可以将不同的一维数据合并成一个二维数组，类似于沿列方向 (column-wise) 进行堆叠
# 在这段代码中 np.c_[xx1.ravel(), xx2.ravel()] 将两个一维数组xx1.ravel()和xx2.ravel()合并为一个二维数组
# 预测 & 调整形状
# 注意：这里将预测和reshape合并在了一行
y_predict = clf.predict(np.c_[xx1.ravel(), xx2.ravel()]).reshape(xx1.shape)

# 【决策边界可视化】
# 可视化
# 创建图形和对象
# fig, ax = plt.subplots()

# 定义浅色系（填充角色区域）和深色系（绘制样本点）的颜色映射
cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF']) # 浅红色系和蓝色系的浅色
cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF']) # 对应深色的样本点颜色

fig, ax = plt.subplots(figsize=(8, 6))

# 绘制决策区域
plt.contourf(xx1, xx2, y_predict, cmap=cmap_light, alpha=0.8) # 使用预测结果填充决策区域，使用浅色背景

# 绘制决策边界
# plt.contourf 绘制等高线/轮廓线
# levels=[0, 1, 2] 表示强制绘制"等高线层级"这里对应0，1的边界（实际上类别改变的位置就是决策边界）
# 自定义颜色 colors=['red', 'green', 'blue']
plt.contour(xx1, xx2, y_predict, levels=[-0.5, 0.5, 1.5, 2.5], 
            colors=['red', 'green', 'blue'], linewidths=2) # 绘制不同类别的决策边界

# 绘制数据点
sns.scatterplot(x=X[:, 0], y=X[:, 1], hue=iris.target_names[y], # 显示原始数据点
                palette=['#1f77b4', '#ff7f0e', '#2ca02c'], alpha=1.0, # 使用深色调色盘
                linewidth=1, edgecolors=[1, 1, 1]) # 数据点的边缘颜色为白色

# 图形装饰
plt.xlim(xx1.min(), xx1.max()) # 设置x轴范围
plt.ylim(xx2.min(), xx2.max()) # 设置y轴范围
plt.title("k-NN classifier (k = %i, weights = 'uniform')" % (k_neighbors)) # 图形标题
plt.xlabel(iris.feature_names[0]) # x轴标签
plt.ylabel(iris.feature_names[1]) # y轴标签
ax.grid(linestyle='--', linewidth=0.25, color=[0.5, 0.5, 0.5]) # 设置网格线样式
plt.tight_layout() # 自动调整子图参数以使图形填满整个图像区域
plt.axis('equal') # 设置坐标轴比例相同
plt.show()