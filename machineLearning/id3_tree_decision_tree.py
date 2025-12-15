# coding: utf-8

# 导入必要的科学计算与绘图库
import numpy as np  # 用于高效的数值计算和数组操作
import csv  # 用于读取 CSV 文件
import matplotlib.pyplot as plt  # 用于绘制决策树


class ID3Classifier:
    """
    ID3 决策树分类器 (符号显示)

    算法特点:
    1. 核心指标: 信息增益 (Information Gain)。
       计算公式: Gain(D, A) = Entropy(D) - Entropy(D|A)
    2. 树结构: 多叉树 (Multi-way split)。
    3. 局限性: 容易偏向取值较多的特征 (已被 C4.5 的增益率改进)。
    """

    def __init__(self):
        """初始化模型状态"""
        self.tree = None  # 存储训练好的决策树 (字典结构)
        self.vocab = {}  # 词表: 字符串 -> 整数 ID
        self.inv_vocab = {}  # 逆词表: 整数 ID -> 字符串
        self.feat_idx_map = {}  # 特征名映射: 特征名 -> 列索引

    def fit(self, X, y, feature_names):
        """
        训练模型入口
        :param X: 特征矩阵
        :param y: 标签向量
        :param feature_names: 特征名称列表
        """
        # 1. 数据预处理: 将所有字符串数据编码为整数索引，加速后续计算
        # update=True 允许在训练时扩充词表
        X_enc = self._encode(X, update=True)
        y_enc = self._encode(y, update=True)

        # 2. 记录特征元数据，用于后续查找
        self.feature_names = np.array(feature_names)
        self.feat_idx_map = {name: i for i, name in enumerate(feature_names)}

        # 3. 初始化可用特征池 (存储列索引 [0, 1, 2...])
        active_features = list(range(len(feature_names)))

        # 4. 递归构建决策树
        self.tree = self._build_tree(X_enc, y_enc, active_features)
        return self.tree

    def predict(self, X):
        """
        预测入口
        :param X: 测试集特征矩阵
        :return: 预测结果数组
        """
        # 1. 将测试数据编码 (update=False, 遇到新词标记为 -1)
        X_enc = self._encode(X, update=False)

        # 2. 逐行预测，并将结果封装为 Numpy 数组返回
        return np.array([self._predict_row(self.tree, row) for row in X_enc])

    def _encode(self, data, update=True):
        """内部工具: 将字符串矩阵映射为整数矩阵"""
        # 展平数据以便统计唯一值
        flat = np.array(data).flatten()

        if update:
            # 找出当前词表中没有的新值
            new_vals = set(flat) - self.vocab.keys()
            start_idx = len(self.vocab)
            # 更新字典
            for i, val in enumerate(new_vals):
                self.vocab[val] = start_idx + i
                self.inv_vocab[start_idx + i] = val

        # 向量化查找: 将数据中的字符串替换为 ID
        mapper = np.vectorize(lambda x: self.vocab.get(x, -1))
        return mapper(data)

    def _decode(self, idx):
        """内部工具: 将整数 ID 还原为字符串"""
        return self.inv_vocab.get(int(idx), "Unknown")

    def _calc_entropy(self, y):
        """
        向量化计算香农熵 (Shannon Entropy)
        公式: H(D) = -sum(p_i * log2(p_i))
        """
        if len(y) == 0: return 0.0  # 空集熵为0

        # 统计各类别出现的次数
        _, counts = np.unique(y, return_counts=True)
        # 计算概率分布
        probs = counts / len(y)

        # 计算熵 (加 1e-9 防止 log2(0) 错误)
        return -np.sum(probs * np.log2(probs + 1e-9))

    def _build_tree(self, X, y, active_features):
        """
        递归构建 ID3 树的核心逻辑
        """
        # --- 停止条件 1 ---
        # 样本全属于同一类别，返回该类别 (叶节点)
        if len(np.unique(y)) == 1:
            return self._decode(y[0])

        # --- 停止条件 2 ---
        # 无特征可用 或 所有样本特征完全一致，返回多数类
        if not active_features or (len(X) > 0 and (X[:, active_features] == X[0, active_features]).all()):
            return self._decode(np.argmax(np.bincount(y)))

        # --- 选择最优特征 (ID3 核心: 信息增益) ---
        base_ent = self._calc_entropy(y)  # 当前节点的总熵
        best_gain = -1.0  # 记录最大增益
        best_feat_rel_idx = -1  # 最优特征在 active_features 中的相对索引
        n_samples = len(y)

        # 遍历每一个可用特征
        for i, feat_idx in enumerate(active_features):
            feat_vals = X[:, feat_idx]  # 获取该列数据
            unique_vals, counts = np.unique(feat_vals, return_counts=True)

            # 计算条件熵: H(D|A) = sum( (|Dv|/|D|) * H(Dv) )
            new_ent = 0.0
            for val, count in zip(unique_vals, counts):
                # 筛选出特征值为 val 的子样本标签
                sub_y = y[feat_vals == val]
                # 权重 * 子集熵
                new_ent += (count / n_samples) * self._calc_entropy(sub_y)

            # 计算信息增益: Gain = H(D) - H(D|A)
            gain = base_ent - new_ent

            # 更新最优特征
            if gain > best_gain:
                best_gain = gain
                best_feat_rel_idx = i

        # --- 兜底处理 ---
        # 如果增益非常小，认为切分无意义，直接返回多数类
        if best_gain < 1e-6:
            return self._decode(np.argmax(np.bincount(y)))

        # --- 构建节点 ---
        # 获取最优特征的真实列索引和名称
        best_feat_abs_idx = active_features[best_feat_rel_idx]
        best_feat_name = self.feature_names[best_feat_abs_idx]

        tree = {best_feat_name: {}}

        # 生成剩余可用特征列表 (ID3 通常在分支后移除已用特征)
        next_features = active_features[:best_feat_rel_idx] + active_features[best_feat_rel_idx + 1:]

        # 获取该特征的所有取值，生成分支
        unique_vals = np.unique(X[:, best_feat_abs_idx])
        for val in unique_vals:
            # 布尔掩码筛选数据
            mask = (X[:, best_feat_abs_idx] == val)

            # 【关键】添加 "==" 前缀，用于可视化显示
            val_str = f"=={self._decode(val)}"

            # 递归构建子树
            tree[best_feat_name][val_str] = self._build_tree(X[mask], y[mask], next_features)

        return tree

    def _predict_row(self, tree, row):
        """单样本预测递归"""
        # 如果不是字典，说明到达叶子节点，返回类别
        if not isinstance(tree, dict): return tree

        # 获取当前根节点的特征名
        feat_name = list(tree.keys())[0]
        # 查找特征对应的列索引
        feat_idx = self.feat_idx_map.get(feat_name)

        if feat_idx is None: return "Error"  # 特征名不匹配

        # 获取测试样本在该特征上的值 (整数 ID)
        val_code = row[feat_idx]

        # 【关键】构造带有 "==" 的键名进行查找
        val_str = f"=={self._decode(val_code)}"

        # 查找子树
        subtree = tree[feat_name].get(val_str)

        # 处理未见过的特征值
        if subtree is None: return "Unknown"

        # 递归向下
        return self._predict_row(subtree, row)


# --- 绘图工具 (通用 Matplotlib 代码) ---
def plot_tree(tree_dict):
    """
    绘制决策树结构
    :param tree_dict: 树的字典表示
    """
    # 定义节点样式
    decision_node = dict(boxstyle="sawtooth", fc="0.8")  # 决策节点: 锯齿框
    leaf_node = dict(boxstyle="round4", fc="0.8")  # 叶子节点: 圆角框
    arrow_args = dict(arrowstyle="<-")  # 箭头样式

    def get_info(t):
        """计算树的宽度和深度，用于布局"""
        if not isinstance(t, dict): return 1, 1
        key = list(t.keys())[0]
        leafs, depth = 0, 0
        for k in t[key]:
            l, d = get_info(t[key][k])
            leafs += l
            depth = max(depth, d)
        return leafs, depth + 1

    def plot_node(txt, center, parent, node_type):
        """画节点"""
        ax.annotate(txt, xy=parent, xytext=center, xycoords='axes fraction',
                    textcoords='axes fraction', va="center", ha="center",
                    bbox=node_type, arrowprops=arrow_args)

    def plot_mid_text(cntr, parent, txt):
        """画连线上的文字"""
        x = (parent[0] - cntr[0]) / 2.0 + cntr[0]
        y = (parent[1] - cntr[1]) / 2.0 + cntr[1]
        ax.text(x, y, txt)

    def recursive_plot(t, parent, node_txt):
        """递归绘图主逻辑"""
        nonlocal x_off, y_off
        num_leafs, _ = get_info(t)
        first_str = list(t.keys())[0]

        # 计算当前节点坐标
        cntr = (x_off + (1.0 + float(num_leafs)) / 2.0 / total_w, y_off)

        plot_mid_text(cntr, parent, node_txt)
        plot_node(first_str, cntr, parent, decision_node)

        y_off -= 1.0 / total_d  # 下移一层
        for key in t[first_str]:
            if isinstance(t[first_str][key], dict):
                recursive_plot(t[first_str][key], cntr, str(key))
            else:
                x_off += 1.0 / total_w
                plot_node(t[first_str][key], (x_off, y_off), cntr, leaf_node)
                plot_mid_text((x_off, y_off), cntr, str(key))
        y_off += 1.0 / total_d  # 回溯

    # 初始化图形界面
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    ax = plt.subplot(111, frameon=False, xticks=[], yticks=[])
    total_w, total_d = get_info(tree_dict)
    x_off, y_off = -0.5 / total_w, 1.0
    recursive_plot(tree_dict, (0.5, 1.0), '')
    plt.show()


# --- 主程序入口 ---
if __name__ == "__main__":
    file_path = "./data/play_tennis1.csv"
    try:
        data = []
        # --- 健壮读取: 自动尝试编码 ---
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = list(csv.reader(f))
        except UnicodeDecodeError:
            print("提示: UTF-8 读取失败，尝试 GBK 编码...")
            with open(file_path, 'r', encoding='gbk') as f:
                data = list(csv.reader(f))

        if not data: raise ValueError("文件为空")

        # 数据切分
        feature_names = np.array(data[0][:-1])  # 特征名
        X = np.array([row[:-1] for row in data[1:]])  # 特征数据
        y = np.array([row[-1] for row in data[1:]])  # 标签数据

        print(">>> 正在训练 ID3 模型 (基于信息增益)...")
        clf = ID3Classifier()
        model = clf.fit(X, y, feature_names)

        print("\n[模型结构]:")
        print(model)

        # 预测验证
        y_pred = clf.predict(X)
        acc = np.mean(y == y_pred) * 100
        print(f"\n[训练集准确率]: {acc:.2f}%")

        # 绘图
        print("\n>>> 正在绘图...")
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']  # 适配中文
        plt.rcParams['axes.unicode_minus'] = False
        plot_tree(model)

    except Exception as e:
        print(f"程序运行出错: {e}")