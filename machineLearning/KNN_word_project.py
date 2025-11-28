import numpy as np
import re  # 正则表达式
import pandas as pd
from scipy.sparse import hstack  # 稀疏矩阵的水平堆叠
from sklearn.neighbors import KNeighborsClassifier  # KNN分类器
from sklearn.datasets import fetch_20newsgroups  # 大量新闻词汇
from sklearn.feature_extraction.text import TfidfVectorizer  # 文本特征提取
from sklearn.model_selection import train_test_split, GridSearchCV  # 数据集划分和网格搜索
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix  # 分类准确率、分类报告和混淆矩阵
from sklearn.pipeline import Pipeline  # 管道
from sklearn.preprocessing import StandardScaler  # 标准化
from sklearn.decomposition import TruncatedSVD  # 奇异值分解
from sklearn.feature_selection import SelectKBest, f_classif  # 特征选择
from sklearn.base import BaseEstimator, TransformerMixin  # 自定义转换器

# 1. 优化特征提取器
class OptimizedTextFeatureExtractor(BaseEstimator, TransformerMixin):
    def __init__(self, 
                 word_ngram=(1, 3),
                 word_max_features=10000,
                 char_ngram=(2, 4),
                 char_max_features=4000,
                 word_min_df=2,
                 word_max_df=0.7, # 过滤过于常见词
                 char_min_df=2,
                 char_max_df=0.7):
        
        # 保存参数
        self.word_ngram = word_ngram
        self.word_max_features = word_max_features
        self.word_min_df = word_min_df
        self.word_max_df = word_max_df
        
        self.char_ngram = char_ngram
        self.char_max_features = char_max_features
        self.char_min_df = char_min_df
        self.char_max_df = char_max_df
        
        # [修复] 初始化词级 TF-IDF 向量化器
        # 原代码漏掉了这个对象的初始化，导致 fit 时对 float 报错
        self.word_tfidf = TfidfVectorizer(
            analyzer='word',
            ngram_range=self.word_ngram,
            max_features=self.word_max_features,
            min_df=self.word_min_df,
            max_df=self.word_max_df,
            stop_words='english' # 词级通常建议去除停用词
        )

        # 初始化字符级 TF-IDF 向量化器
        self.char_tfidf = TfidfVectorizer(
            analyzer='char_wb',
            ngram_range=self.char_ngram,
            max_features=self.char_max_features,
            min_df=self.char_min_df,
            max_df=self.char_max_df,
            sublinear_tf=True
        )

    def fit(self, X, y=None):
        # [修复] 正确调用 vectorizer 的 fit
        self.word_tfidf.fit(X) 
        self.char_tfidf.fit(X)
        return self

    def transform(self, X):
        # [修复] 正确调用 vectorizer 的 transform
        word_features = self.word_tfidf.transform(X)
        char_features = self.char_tfidf.transform(X)
        
        # 堆叠特征
        return hstack([word_features, char_features])

# ------- 2. 文本清洗（技术特征）-------
def clean_text(text):
    text = re.sub(r'<.*?>', '', text)  # 移除HTML标签
    # 保留字母、数字、点、连字符（保留版本号和技术术语特征）
    text = re.sub(r'[^a-zA-Z0-9\s\./-]', '', text) 
    text = re.sub(r'\s+', ' ', text).strip()  # 移除多余空格
    return text.lower()

# ------- 3. 数据加载与划分 -------
if __name__ == "__main__":
    # 定义需要加载的新闻类别
    categories = [
        'comp.graphics', 'sci.space', 'rec.sport.hockey', 'talk.politics.misc'
    ]
    
    print("正在加载数据集 (可能需要下载)...")
    newsgroups = fetch_20newsgroups(
        subset='all',
        categories=categories,
        remove=('footers', 'quotes'),
    )
    
    # 清洗数据
    cleanned_data = [clean_text(doc) for doc in newsgroups.data]
    print(f"清洗后的文本总数: {len(cleanned_data)}")
    print(f"分类类别: {newsgroups.target_names}\n")

    # [优化] test_size 从 15 改为 0.15 (15%)，原代码只有15个样本太少
    X_train, X_test, y_train, y_test = train_test_split(
        cleanned_data, newsgroups.target,
        test_size=0.15,
        random_state=42,
        stratify=newsgroups.target
    )

    # -------------------- 4. 优化Pipeline --------------------
    pipeline = Pipeline([
        ('text_features', OptimizedTextFeatureExtractor()),
        ('select_kbest', SelectKBest(f_classif, k=6000)),
        ('svd', TruncatedSVD(n_components=300, random_state=42)),
        ('scaler', StandardScaler(with_mean=False)), # SVD后保持数据分布
        ('knn', KNeighborsClassifier(
            metric='cosine',
            weights='distance',
            algorithm='brute',
            n_jobs=-1
        ))
    ])

    # -------------------- 5. 网格搜索参数 --------------------
    # 为了演示运行速度，这里缩小了参数范围，实际运行时可增加候选值
    param_grid = {
        'knn__n_neighbors': [5], # 示例：只测试 k=5
        # 注意：由于我们在 __init__ 中手动赋值了参数给内部 vectorizer
        # 若要通过 GridSearch 调整内部 vectorizer 参数，需要改写 set_params
        # 或者简化为直接传入参数。此处为了代码运行通过，主要调整顶层参数。
        'select_kbest__k': [4000, 6000],
    }

    grid_search = GridSearchCV( #初始化网格搜索⚠️⚠️⚠️⚠️真正起作用的代码
        estimator=pipeline, #管道模型
        param_grid=param_grid, #设置参数网格
        cv=3, #三折交叉验证
        scoring='accuracy', #评估指标为准确率
        n_jobs=-1, #使用所有CPU核心
        verbose=1 #输出详细日志
    )

    # ---------------- 6. 训练与评估 ----------------
    print("开始优化KNN训练 (GridSearch)...")
    grid_search.fit(X_train, y_train)

    print(f"\n最佳参数组合: {grid_search.best_params_}")
    print(f"交叉验证最高准确率: {grid_search.best_score_:.4f}\n")

    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_pred)

    print("="*50)
    print(f"测试集最终准确率: {test_accuracy:.4f}")
    print("\n详细分类报告:")
    print(classification_report(
        y_test, y_pred,
        target_names=newsgroups.target_names,
        digits=4
    ))

    print("\n混淆矩阵 (行=真实类别, 列=预测类别):")
    conf_matrix = confusion_matrix(y_test, y_pred)
    conf_df = pd.DataFrame(
        conf_matrix,
        index=newsgroups.target_names,
        columns=newsgroups.target_names
    )
    print(conf_df)
    print("="*50)

    # ---------------- 7. 自定义文本测试 ----------------
    sample_texts = [  # [修复] 拼写错误 sameple -> sample
        "NVIDIA released a new GPU 24GB VRAM for 3D rendering in games",
        "Astronauts on the ISS completed a spacewalk to repair the solar panel",
        "The hockey team won the championship by scoring 3 goals in the final",
        "The government announced a new tax policy to reduce income inequality",
    ]
    sample_cleaned = [clean_text(text) for text in sample_texts]
    sample_preds = best_model.predict(sample_cleaned)

    print("\n自定义文本分类测试:")
    for i, (text, pred) in enumerate(zip(sample_texts, sample_preds), 1):
        print(f"\n{i}. 文本: {text}")
        print(f"    预测类别: {newsgroups.target_names[pred]}")
        # 这里的正确类别是硬编码的，仅用于展示
        print(f"    正确类别: {['comp.graphics', 'sci.space', 'rec.sport.hockey', 'talk.politics.misc'][i-1]}")