from turtle import color
from networkx import number_of_walks
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, KFold, GridSearchCV
from sklearn. preprocessing import StandardScaler
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# 1. 读取数据集
df = pd. read_csv('prostate_cancer_data.csv')

#2. 查看数据结构‘train'列的分布
print("Data Structure:")
print(df.info())
print("\nDistribution of 'train' column:")
print(df['train'].value_counts())

# 3. 数据可视化
#设置seaborn样式
sns.set(style="whitegrid")
#散点图
plt.figure(figsize=(12, 8))
sns.scatterplot(x='lcavol', y='lpsa', hue='train', data=df)
plt.title('Scatter plot of lcavol vs lpsa')
plt.show()

# 4. 将Gleason评分转换为二分类并重新绘制箱型图
df['gleason_binary'] = df['gleason'].apply(lambda x: 1 if x > 6 else 0)
#重新绘制箱型图
plt.figure(figsize=(12, 8))
sns.boxplot(x='gleason_binary', y='lpsa', data=df)
plt.title('Box plot of lpsa by Gleason binary')
plt.show()

# 5. 计算相关矩阵并绘制相关图
# 计算相关矩阵
correlation_matrix = df. corr()

# 绘制相关矩阵的热力图
plt.figure(figsize=(12,8))
sns. heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f' )
plt.title('Correlation Matrix Heatmap' )
plt.show()

# 6. 使用Lasso回归进行模型训练
# 分离特征和目标变量
X = df[['lcavol', 'lweight', 'age', 'bph' , 'svi', 'lcp' , 'gleason' , 'pgg45']]
y = df['lpsa']

# 分割数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 归一化处理
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 7. 使用K 折交叉验证和 GridSearchCV 优化 Lasso 回归
# 定义 K 折交叉验证
kf = KFold(n_splits=5, shuffle=True, random_state=42)
# 定义 Lasso 回归模型
lasso = Lasso()

# 定义参数网格
param_grid = {'alpha': [0.001, 0.01, 0.1, 1, 10]}

# 使用 GridSearchCV 进行参数优化
grid_search = GridSearchCV(estimator=lasso, param_grid=param_grid, cv=kf, scoring='neg_mean_squared_error', n_jobs =- 1)
grid_search.fit(X_train_scaled, y_train)

# 获取最佳参数
best_params = grid_search.best_params_
print(f'Best Parameters: {best_params}')

# 使用最佳参数训练模型
best_lasso = Lasso(alpha=best_params['alpha'])
best_lasso.fit(X_train_scaled, y_train)
# 与特征集数量一致
# 与特征集数量一致

# 创建一个空的网格

y_pred = best_lasso.predict(X_test_scaled)

# 评估模型
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'\n均方误差: {mse}')
print(f'R^2 Score: {r2}')

# 查看 Lasso 回归的系数
print('Lasso 回归系数:', best_lasso.coef_)

# 8. 交叉验证结果
cv_results = grid_search.cv_results_
for mean_score, params in zip(cv_results['mean_test_score'], cv_results['params' ]) :
    print(f'参数: {params}, 平均均方误差: {-mean_score: .4f}' )

# 生成特征热力图
num_rows = 8
num_cols = 8

#创建一个空的网格
grid = np.zeros((num_rows, num_cols))
#创建一个Figure和Axes对象
fig, axes = plt.subplots(num_rows,num_cols, figsize=(15, 15))
#遍历每个子图
for i in range(num_rows):
    for j in range(num_cols):
        #如果当前单元在对角线上，只显示列名称
        if i == j:
            axes[i, j].text(0.5, 0.5, X.columns[i], ha='center', va='center', fontsize=12, color='black')
            axes[i, j].set_xticks([])
            axes[i, j].set_yticks([])
        else:
            #选择一部分数据
            subset = df.sample(n=50, random_state=i * num_cols + j)
            axes[i, j].scatter(subset[X.columns[j]], subset[X.columns[i]], alpha=0.6, color='red', s=10)
            axes[i, j].set_xticks([])
            axes[i, j].set_yticks([])
#调整子图间距
plt.tight_layout()
plt.suptitle('特征散点图网格', fontsize=16)
plt.subplots_adjust(top=0.95)
plt.show()


#KNN
from sklearn.neighbors import KNeighborsRegressor

# 1. 定义 K 近邻模型
knn = KNeighborsRegressor()

# 2. 定义参数网格
# 尝试不同的 K 值和权重类型
knn_param_grid = {
    'n_neighbors': [3, 5, 7, 9, 11],  # K 的数量
    'weights': ['uniform', 'distance'] # 邻居的权重
}

# 3. 使用 GridSearchCV 进行参数优化
knn_grid_search = GridSearchCV(estimator=knn, param_grid=knn_param_grid, cv=kf, scoring='neg_mean_squared_error', n_jobs=-1)
knn_grid_search.fit(X_train_scaled, y_train)

# 获取最佳参数并训练模型
knn_best_params = knn_grid_search.best_params_
print(f'KNN 最佳参数: {knn_best_params}')

knn_best = KNeighborsRegressor(**knn_best_params)
knn_best.fit(X_train_scaled, y_train)

# 4. 评估模型
knn_y_pred = knn_best.predict(X_test_scaled)
knn_mse = mean_squared_error(y_test, knn_y_pred)
knn_r2 = r2_score(y_test, knn_y_pred)

print(f'\nKNN 均方误差: {knn_mse:.4f}')
print(f'KNN R^2 分数: {knn_r2:.4f}')

#=================岭回归================
from sklearn.linear_model import Ridge

# 1. 定义岭回归模型
ridge = Ridge()

# 2. 定义参数网格 (alpha)
ridge_param_grid = {'alpha': [0.001, 0.01, 0.1, 1, 10, 100]}

# 3. 使用 GridSearchCV 进行参数优化
ridge_grid_search = GridSearchCV(estimator=ridge, param_grid=ridge_param_grid, cv=kf, scoring='neg_mean_squared_error', n_jobs=-1)
ridge_grid_search.fit(X_train_scaled, y_train)

# 获取最佳参数并训练模型
ridge_best_params = ridge_grid_search.best_params_
print(f'\n岭回归 最佳参数: {ridge_best_params}')

ridge_best = Ridge(alpha=ridge_best_params['alpha'])
ridge_best.fit(X_train_scaled, y_train)

# 4. 评估模型
ridge_y_pred = ridge_best.predict(X_test_scaled)
ridge_mse = mean_squared_error(y_test, ridge_y_pred)
ridge_r2 = r2_score(y_test, ridge_y_pred)

print(f'岭回归 均方误差: {ridge_mse:.4f}')
print(f'岭回归 R^2 分数: {ridge_r2:.4f}')
#==============================弹性网格================
from sklearn.linear_model import ElasticNet

# 1. 定义弹性网络模型
en = ElasticNet()

# 2. 定义参数网格
# l1_ratio: L1 (Lasso) 和 L2 (Ridge) 混合的比例
en_param_grid = {
    'alpha': [0.01, 0.1, 1],
    'l1_ratio': [0.1, 0.5, 0.9]
}

# 3. 使用 GridSearchCV 进行参数优化
en_grid_search = GridSearchCV(estimator=en, param_grid=en_param_grid, cv=kf, scoring='neg_mean_squared_error', n_jobs=-1)
en_grid_search.fit(X_train_scaled, y_train)

# 获取最佳参数并训练模型
en_best_params = en_grid_search.best_params_
print(f'\n弹性网 最佳参数: {en_best_params}')

en_best = ElasticNet(**en_best_params)
en_best.fit(X_train_scaled, y_train)

# 4. 评估模型
en_y_pred = en_best.predict(X_test_scaled)
en_mse = mean_squared_error(y_test, en_y_pred)
en_r2 = r2_score(y_test, en_y_pred)

print(f'弹性网 均方误差: {en_mse:.4f}')
print(f'弹性网 R^2 分数: {en_r2:.4f}')

#============梯度提升回归================
from sklearn.ensemble import GradientBoostingRegressor

# 1. 定义梯度提升模型
gbr = GradientBoostingRegressor(random_state=42)

# 2. 定义参数网格
# 关键参数：
# 'n_estimators': 树的数量
# 'learning_rate': 每棵树贡献的权重
# 'max_depth': 每棵树的最大深度
kf = KFold(n_splits=5, shuffle=True, random_state=42)
gbr_param_grid_aggressive = {
    'n_estimators': [100, 300, 500],
    'learning_rate': [0.05, 0.1, 0.3], # 尝试更大的学习率
    'max_depth': [3, 4, 5],
    'subsample': [0.7, 0.9] # 引入随机性，防止过拟合
}

# 3. 使用 GridSearchCV 进行参数优化
gbr_grid_search = GridSearchCV(estimator=gbr, param_grid=gbr_param_grid_aggressive, cv=kf, scoring='neg_mean_squared_error', n_jobs=-1)
gbr_grid_search.fit(X_train_scaled, y_train)

# 获取最佳参数并训练模型
gbr_best_params = gbr_grid_search.best_params_
print(f'\n梯度提升 最佳参数: {gbr_best_params}')

gbr_best = GradientBoostingRegressor(**gbr_best_params, random_state=42)
gbr_best.fit(X_train_scaled, y_train)

# 4. 评估模型
gbr_y_pred = gbr_best.predict(X_test_scaled)
gbr_mse = mean_squared_error(y_test, gbr_y_pred)
gbr_r2 = r2_score(y_test, gbr_y_pred)

print(f'梯度提升 均方误差: {gbr_mse:.4f}')
print(f'梯度提升 R^2 分数: {gbr_r2:.4f}')

# 查看特征重要性
feature_importances = pd.Series(gbr_best.feature_importances_, index=X.columns).sort_values(ascending=False)
print('\n特征重要性 (前 3 个):\n', feature_importances.head(3))