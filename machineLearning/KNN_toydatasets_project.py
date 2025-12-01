"""KNN算法在玩具数据集上的应用示例"""
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

# 生成样本数为200，特征数为2，分类数为2的数据集
data = make_blobs(n_samples=200, n_features=2, centers=2, cluster_std=1.0, random_state=8)
X, Y = data  # 解包数据集，X为特征数据，Y为标签数据

# 创建KNN分类器实例
clf = KNeighborsClassifier()
# 使用数据集对分类器进行训练
clf.fit(X, Y)

# 绘制图形
# 计算特征空间的边界范围
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
# 生成网格点坐标
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02), np.arange(y_min, y_max, 0.02))
# 对网格点进行预测
z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

# 将预测结果 reshape 成网格形状
z = z.reshape(xx.shape)
# 绘制背景色（分类区域）
plt.pcolormesh(xx, yy, z, cmap=plt.cm.Pastel1)
# 绘制数据点
plt.scatter(X[:, 0], X[:, 1], s=80, c=Y, cmap=plt.cm.spring, edgecolors='k')
# 设置x周范围
plt.xlim(xx.min(), xx.max())
# 设置y轴范围
plt.ylim(yy.min(), yy.max())
# 添加图表标题
plt.title("Classifier: KNN")

# 把待分类的数据点的分类进行判断
res = clf.predict([[6.75, 4.82]])
# 在图上添加分类结果的文本
plt.text(6.9, 4.5, 'Classification flag: ' + str(res))

# 显示图表
plt.show()