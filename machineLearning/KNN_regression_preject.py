""""""
import matplotlib.pyplot as plt
import numpy as np 
from sklearn.datasets import make_regression # 生成回归数据集
from sklearn.neighbors import KNeighborsRegressor # KNN回归器
from sklearn.model_selection import train_test_split # 数据集划分

#生成数据为100，特征数为1的数据集合
X, Y = make_regression(n_samples=100, n_features=1, n_informative=1, noise=10.0, random_state=8)

#创建KNN回归器实例
reg = KNeighborsRegressor(n_neighbors=5)
#训练模型
reg.fit(X, Y)
z = np.linspace(-3, 3, 100).reshape(-1, 1)
#对数据进行预测
y_pred = reg.predict(z)
#绘制图形
plt.scatter(X, Y, color='blue', label='Data Points') # 绘制
plt.plot(z, y_pred, color='red', label='KNN Regression Line') # 绘制回归线
plt.title("KNN Regression on Toy Dataset")
plt.xlabel("Feature")
plt.ylabel("Target")
plt.legend()
plt.show()