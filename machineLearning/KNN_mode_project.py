import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
try:
    import matplotlibx
except Exception:
    matplotlibx = None

st.set_page_config(layout='wide')
if matplotlibx is not None:
    try:
        plt.style.use(matplotlibx.styles.pitaya_smoothie['light'])
    except Exception:
        plt.style.use('default')
else:
    plt.style.use('default')
plt.rcParams['figure.dpi'] = 100
plt.rcParams['font.sans-serif'] = 'Times New Roman'

raw_data_x = [[3.3935, 2.3313], [3.11, 1.7815], [1.3438, 3.3684], [1.9, 2.4],
              [2.5, 3.6], [1.7, 4], [3.5823, 4.6792], [2.2804, 2.8670],
              [7.4234, 4.6965], [5.7451, 3.5340], [9.1722, 2.5111],
              [7.7928, 3.4241], [7.9398, 0.7916], [6.2, 2.4], [4.5, 2.3],
              [4.6, 2.4]]
raw_data_y = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
data = pd.DataFrame(raw_data_x)
data['y'] = raw_data_y
data.columns = ['x1', 'x2', 'y']
st.markdown('# KNN算法演示')

with st.sidebar:
    x1 = st.slider("请输入x的第一个坐标", 0, 10, 5)
    x2 = st.slider("请输入x的第二个坐标", 0.0, 5.0, 2.5)
    K = st.slider("请输入邻居的数量", 1, 10, 3)
st.info(f'你输入的数据是: {x1, x2}')
x = np.array([x1, x2])

def creat_plot(datapair, x_point):
    fig = plt.figure(figsize=(7, 7), dpi=100)
    # 绘制标签为0的点：筛选y=0的数据，取x1/x2为横纵坐标，点大小30，图例标注"蓝色:0"
    plt.scatter(datapair[datapair['y'] == 0]['x1'],
                datapair[datapair['y'] == 0]['x2'], s=30, label='蓝色: 0')
    # 绘制标签为1的点：筛选y=1的数据，取x1/x2为横纵坐标，点大小30，图例标注"橙色:1"
    plt.scatter(datapair[datapair['y'] == 1]['x1'],
                datapair[datapair['y'] == 1]['x2'], s=30, label='橙色: 1')
    # 使用星形标记，点大小为100（突出显示）
    plt.scatter(x_point[0], x_point[1], marker='*', s=100)
    plt.legend(prop={'family': 'SimHei'})
    # 设置y轴范围：指定0到5（确保数据在合理的范围内）
    plt.ylim(0, 5)
    plt.title('原始数据目标点分布', fontproperties='SimHei')
    # 获取当前坐标轴对象，设置横纵坐标等比例（确保图形不失真）
    ax = plt.gca()
    ax.set_aspect('equal')
    # 返回画布对象
    return fig

def knn_classify(k, data_pair, x_point):
    # 将目标预测点转换为numpy数组，方便后续矩阵运算
    x_point = np.array(x_point)
    # 计算目标点与所有样本点的欧式距离
    # 1. 计算各维度插值的平方
    # 2. 按行求和（得带平方和）
    # 3. 对平方和开根号（得到欧式距离）
    if k <= 0 or k > len(data_pair):
        raise ValueError('K must be between 1 and the number of samples')
    # 计算距离时采用 numpy/SSE 方式，返回 pd.Series
    dists = np.sqrt(((data_pair[['x1', 'x2']] - x_point) ** 2).sum(axis=1))
    # 对距离 Series 尽心升序排序，inplace=True表示直接修改原对象
    dists.sort_values(inplace=True)
    # 对距离最小的前k个样本的索引（即k个最近邻的索引）
    indexes = dists.index[:k]
    # 统计k个最近邻的类别分布:
    # 1. 根据索引对应的类别标签
    # 2. 统计各类别的出现次数
    # 3. 转换为字典格式（键：类别，值：次数）
    results = data_pair.loc[indexes, 'y'].value_counts().to_dict()
    # 返回分类统计结果，距离Series、近邻索引、类别统计字典这些信息
    return f"统计显示：类目1橙色点：有{results.get(1, 0)}个，类目2蓝色点：有{results.get(0, 0)}个", dists, indexes, results

def creat_plot_with_neighbor(data_pair, x_point, neighbor, indexes, dists):
    fig = plt.figure(figsize=(7, 7), dpi=100)
    # 绘制类别为0的样本点：蓝色，大小为30，图例标签标注'蓝色: 0'
    plt.scatter(data_pair[data_pair['y'] == 0]['x1'], data_pair[data_pair['y'] == 0]['x2'], s=30, label='蓝色: 0')
    # 绘制类别为1的样本点：橙色，大小为30，图例标签标注'橙色: 1'
    plt.scatter(data_pair[data_pair['y'] == 1]['x1'], data_pair[data_pair['y'] == 1]['x2'], s=30, label='橙色: 1')
    # 绘制目标预测点：星形标记，大小100，突出显示待分类点
    plt.scatter(x_point[0], x_point[1], marker='*', s=100)

    # 设置图表标题：显示当前选择去的邻居数量，指定字体避免乱码
    plt.title(f'当前邻居数量为{neighbor}个', fontproperties='SimHei')
    # 创建圆形：以目标点为圆心，以第K个近邻的距离为半径（k=neighbor），不填充颜色
    # distance series 已排序，取第 neighbor 个值作为半径
    radius = float(dists.iloc[neighbor - 1])
    circle = patches.Circle(tuple(x_point), radius, fill=False)
    # 获取当前坐标轴对象，添加圆形（直观展示近k近邻的范围）
    ax = plt.gca()
    ax.add_patch(circle)

    # 设置横纵坐标等比例，保证圆形不被拉伸变形
    ax.set_aspect('equal')
    # 设置图例：指定黑体，确保中文正常显示
    plt.legend(prop={'family': 'SimHei'})

    # 设置y轴范围为0到5，使数据分布在合适的视野内
    plt.ylim(0, 5)
    # 返回画布对象
    return fig

info, dis, index, result = knn_classify(k=K, data_pair=data, x_point=x)
left, right = st.columns(2)
left.pyplot(creat_plot(data, x))
right.pyplot(creat_plot_with_neighbor(data, x, K, index, dis))

st.success(info)
if result.get(0, 0) > result.get(1, 0):
    st.info('目标点预测结果为: 0')
elif result.get(0, 0) < result.get(1, 0):
    st.info('目标点预测结果为: 1')
else:
    st.info('目标点邻居数量一致，建议更换邻居的数量，设为奇数个')