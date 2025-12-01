# 算距离：给待分类样本计算它与分类样本中每个样本的距离
# 找邻居：圈定与待分类样本距离最近的k个已知样本，作为待分类样本的邻居
# 做分类：根据这个k近邻中的大部分样本所属的类别来决定待分类属于哪个分类
import math  # 导入数学模块
import csv   # 导入csv模块
import operator  # 导入运算符模块
import random  # 导入随机模块
import numpy as np
import pandas as pd
from sklearn.datasets import make_blobs  # 从sklearn.datasets导入make_blobs函数

# 生成样本数据集 samples(样本数量) features(特征向量的维度) centers(类别个数)
def createDataSet(samples=100, features=2, centers=2):
    return make_blobs(n_samples=samples, n_features=features, centers=centers, cluster_std=1.0, random_state=8)

# 加载鸢尾花卉数据集 filename(数据集文件存放路径)
# 注意：这个函数在 main 中实际上未被调用，main 中使用了 pandas 读取
def loadIrisDataset(filename):
    with open(filename, 'rt') as csvfile:  # 打开CSV文件
        lines = csv.reader(csvfile)  # 读取CSV文件的每一行
        dataset = list(lines)  # 将读取的行数转换为列表
        for x in range(len(dataset)):  # 遍历数据集中的每一行
            for y in range(4): # 遍历每一行的前四个特征
                dataset[x][y] = float(dataset[x][y])  # 将特征值转换为浮点数
        return dataset  # 返回处理后的数据集

# 拆分数据集 dataset(要拆分的数据集) split(训练集所占比例) trainingSet(训练集) testSet(测试集)
def splitDataset(dataset, split, trainingSet=[], testSet=[]):
    for x in range(len(dataset)):  # 遍历数据集中的每一行
        if random.random() <= split:  # 如果随机数小于等于split比例
            trainingSet.append(dataset[x]) # 将该行添加到训练集中
        else:
            testSet.append(dataset[x]) # 否则将该行添加到测试集中

# 计算欧式距离
def euclideanDistance(instance1, instance2, length):
    distance = 0   # 初始化距离为0
    for x in range(length):  # 遍历特征长度
        distance += pow(instance1[x] - instance2[x], 2)  # 计算每个特征的平方差累加
    return math.sqrt(distance)

# 选择距离最近的K个实例
def getNeighbors(trainingSet, testInstance, k):
    distances = []  # 初始化距离列表
    length = len(testInstance) - 1  # 特征长度（不包括标签）
    for x in range(len(trainingSet)):  # 遍历训练集中的每一行
        dist = euclideanDistance(testInstance, trainingSet[x], length)  # 计算测试实例与训练实例的距离
        distances.append((trainingSet[x], dist))  # 将训练实际以及距离添加到距离列表中
    distances.sort(key=operator.itemgetter(1))  # 按距离排序
    
    neighbors = []  # 初始化邻居列表
    for x in range(k):  # 遍历前k个最近的实例
        neighbors.append(distances[x][0])  # 将最近的实例添加到邻居列表中
    return neighbors  # 返回邻居列表

# 获取距离最近的K个实例中占比倒较大的分类
def getResponse(neighbors):
    classVotes = {}  # 初始化分类投票字典
    for x in range(len(neighbors)):  # 遍历邻居列表
        response = neighbors[x][-1]  # 获取邻居的标签
        if response in classVotes:  # 如果标签已存在于字典中
            classVotes[response] += 1  # 增加该标签的票数
        else:
            classVotes[response] = 1 # 否则初始化该标签的票数为1
    sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True) # 按票数降序排序
    return sortedVotes[0][0]  # 返回票数最多的标签

# 计算准确率
def getAccuracy(testSet, predictions):
    correct = 0   # 初始化正确预测的数量
    for x in range(len(testSet)):  # 遍历测试集
        if testSet[x][-1] == predictions[x]:  # 如果预测结果与实际标签相同
            correct += 1  # 增加正确预测的数量
    return (correct / float(len(testSet))) * 100.0  # 返回准确率百分比

def main():
    # 使用鸢尾花数据进行分类
    s = 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
    print('From URL:', s)  # 打印数据来源
    dataset = pd.read_csv(s, header=None, encoding='utf-8')  # 从URL读取数据
    print(dataset) # 打印数据集

    # 将 DataFrame 转换为列表
    dataset = dataset.values.tolist()

    trainingSet = []  # 初始化训练集
    testSet = []  # 初始化测试集
    splitDataset(dataset, split=0.75, trainingSet=trainingSet, testSet=testSet) # 拆分数据集
    print('Train set:' + repr(len(trainingSet)))  # 打印训练集大小
    print('Test set:' + repr(len(testSet)))  # 打印测试集大小

    predictions = []  # 初始化预测列表
    k = 7  # 设置k值
    for x in range(len(testSet)):  # 返回测试集
        neighbors = getNeighbors(trainingSet, testSet[x], k)  # 获取最近的K个邻居
        result = getResponse(neighbors)  # 获取预测结果
        predictions.append(result) # 将预测结果添加到预测列表中
        print('>predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))  # 打印预测结果和实际结果
    accuracy = getAccuracy(testSet, predictions)  # 计算准确率
    print('Accuracy: ' + repr(accuracy) + '%')  # 打印准确率

if __name__ == '__main__':
    main()  # 主程序入口