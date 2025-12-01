import pandas as pd
import joblib
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier # K-近邻分类器
from sklearn.metrics import accuracy_score # 计算模型的准确率
from tqdm import tqdm # 进度条

# 加载MNIST数据集
print("开始加载MNIST数据集...")
mnist = fetch_openml(name='mnist_784', version=1)
print("MNIST数据集加载完成")

# 提取特征和标签
print("开始提取特征和标签...")
X = pd.DataFrame(mnist["data"])
y = pd.Series(mnist.target).astype('int')
print("特征和标签提取完成")

# 分隔数据集
print("开始分割数据集...")
# 注意：这里变量名写成了 X_trian (应为 X_train)，但只要后面保持一致不影响运行
X_trian, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"数据集分割完成, 训练集大小: {X_trian.shape}, 测试集大小: {X_test.shape}")

# 实例化K-最近邻分类器
print("开始实例化K-最近邻分类器...")
estimator = KNeighborsClassifier(n_neighbors=3)
print("K-最近邻分类器实例化完成")

# 训练模型
print("开始训练模型...")
estimator.fit(X_trian, y_train)
print("模型训练完成")

# 预测数据集
print("开始预测数据集...")
with tqdm(total=len(X_test), desc="预测进度", ncols=100) as pbar:
    y_pred = estimator.predict(X_test)
    pbar.update(len(X_test))
print("预测完成")

# 计算准确率
print("开始计算模型准确率...")
accuracy = accuracy_score(y_test, y_pred)
print(f"模型准确率: {accuracy:.4f}")

# 保存模型
model_path = './mnist_784.pth'
print(f"开始保存模型到 {model_path}...")
joblib.dump(estimator, model_path)
print("模型保存完成")