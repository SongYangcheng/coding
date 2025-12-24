#数据统计分析
"""
YOLO数据集统计分析模块---负责数据，计算和集合各类数据分布指标
本模块专注于数据收集的统计分析功能，回答的问题是：
"这个数据长什么样子？类别平衡吗？目标大小和形状分布如何？"
核心功能模块：
- 统计每个类别的示例数，出现图像数
- 计算边界框的面积和纵横比分布的平均值和标准差
- 支持detection 和 segmentation 两种任务类型的分析
- 使用dataclass结构化存储统计结果，便于后续报告生成或者可视化
所有统计均基于归一化坐标，不读取图像内容，效率高，隐私安全
"""
import math
import logging
from collections import defaultdict
from pathlib import Path
from dataclasses import dataclass, field #dataclass用于简化类定义，field用于定义默认工厂
from typing import List, Dict, Optional  #Optional用于表示可选字段

#从常量模块导入统一的管理配置项，避免魔法值散落
from utils.constants import TaskType, DETECTION_FIELDS, SEGMENTATION_FIELDS
logger = logging.getLogger(__name__)  #配置模块级日志记录器

#===================数据统计分析核心模块===================
@dataclass
class ClassStatistics:
    """
    使用@dataclass装饰器的原因和好处：
    - python的dataclass 模块是python3.7+提供的数据类装饰器
    - 通过@dataclass，可以自动生成初始化方法(__init__)等常用方法，简化代码
    - 使代码更简洁易读，专注于数据结构定义
    - 适合纯数据容器类的定义
    """
    class_id: int  #类别ID
    class_name: str #类别名称

    instance_count: int = 0
    image_count: int = 0

    #bbox_areas 和 bbox_aspect_ratios使用field(default_factory=list)
    #原因：如果写=[]， 所有示例会共享同一个list
    #default_factory=list 确保每个实例都有自己的独立列表
    #field 用于定义dataclass字段的默认值或工厂函数
    bbox_areas: List[float] = field(default_factory=list)  #存储边界框面积的列表
    bbox_aspect_ratios: List[float] = field(default_factory=list)  #存储边界框纵横比的列表

    #使用@property装饰器定义计算属性
    @property
    def avg_area(self) -> float:
        """计算该类别所有的bbox的平均归一化面积
        @property 装饰器的作用：
        - 让方法可以像属性一样访问，无需加括号：obj.avg_area而不是obj.avg_area()
        - 适合计算属性，提升代码可读性
        - 实现”延迟计算“：只有在访问该属性时才进行计算
        - 这是python中实现"getter"方法的一种方式
        """
        # 三元表达式处理空列表情况,避免除以e的错误
        # 1. 当iself.bbox_areas 非空时:计算所有面积的综合/面积的数量,得到平均值
        #2. 当 self.bbox_areas 为空时:直接返回0.e,保证程序的健壮性
        return sum(self.bbox_areas) / len(self.bbox_aspect_ratios) if self.bbox_areas else 0.0

    @property
    def std_area(self) -> float:
        """计算该类别所有bbox的面积标准差"""
        return calculate_std(self.bbox_areas)

    @property
    def avg_aspect_ratio(self) -> float:
        """计算该类别所有 bbox 的平均长宽比(width/height)"""
        return sum(self.bbox_aspect_ratios) / len(self.bbox_aspect_ratios) if self.bbox_areas else 0.0
    @property
    def std_aspect_ratio(self) -> float:
        """计算该类别所有 bbox 的长宽比标准差"""
        return calculate_std(self.bbox_aspect_ratios)
    
@dataclass
class SplitStatistics:
    """
    存储数据集划分（train/val/test）级别的统计信息
    """
    split_name: str  #划分名称
    total_images: int = 0  #该划分下的图像总数
    total_instances: int = 0  #该划分下的目标实例总数
    class_stats: Dict[int, ClassStatistics] = field(default_factory=dict)  #类别ID到ClassStatistics的映射

    def get_class_stats(self, class_id: int, class_name: str) -> ClassStatistics:
        """获取指定类别的统计信息，若不存在则创建新的ClassStatistics实例"""
        if class_id not in self.class_stats:
            self.class_stats[class_id] = ClassStatistics(class_id=class_id, class_name=class_name)
        return self.class_stats[class_id]
    
#2.调用工具函数
def calculate_std(values: List[float]) -> float:
    """
    计算样本标准差
    为什么要用n-1而不是n？
    - 使用n-1计算样本标准差是为了获得无偏估计
    - 当我们从总体中抽取样本时，样本的均值通常会偏离总体均值
    - 使用n-1可以补偿这种偏差，使得样本标准差更接近总体标准差
    Args:
        values (List[float]): 数值列表
    Returns:
        float: 计算得到的标准差
    """
    if len(values) < 2:
        return 0.0
    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1) 
    return math.sqrt(variance)

#3. 标签解析函数
def parse_detection_label(parts: List[str]) -> Optional[Dict]:
    """
    解析一行检测任务的标签，提取所需统计指标
    YOLO检测格式：class_id x_center y_center width height (均为归一化坐标)
    我们需要width 和 height 来计算面积的长款比
    
    """
    if len(parts) != DETECTION_FIELDS:
        return None
    try:
        #第一个字段(索引为0)转换为整数，代表目标类别ID
        class_id = int(parts[0])
        #将第4，5字段
        w, h = float(parts[3]), float(parts[4])

        #校验宽高合法性：宽和高必须大于0，避免后续计算面积/长宽比时出错或者负数值错误
        if w > 0 and h > 0:
            #数据通过，返回包含目标关键信息的字典
            return {
                "class_id": class_id,
                "width": w,
                "heigth": h,
                "area": w * h,
                "aspect_ratio": w / h
            }
    except (ValueError, IndexError):
        pass

    return None

def parse_segmentation_label(parts: List[str]) -> Optional[Dict]:
    """
    解析一行分割任务标签，
    YOLO分割格式：class_id x1 y1 x2 y2 x3 y3 ... (均为归一化坐标)
    我们计算其外接矩形的宽高，面积，长宽比等指标
    """
