#数据统计分析
"""
YOLO数据集统计分析模块-负责数据，计算和集合各类数据分布指标
本模块专注于数据集的“统计分析”(Analysis)部分,回答的问题是:
“这个数据表长什么样?类别平衡吗?目标大小和形状分布如何?”

核心功能包括:
- 统计每个类别的实例数(instance_count),出现图像数(image_count)
- 计算边界框的归一化面积(area)和长宽比(aspect ratio)的平均值和标准差
- 支持 detection 和 segmentation 两种任务(分割任务使用外接矩形计算面积/长宽比)
- 使用 dataclass 结构化存储统计结果,便于后续报告生成或可视化

所有统计均基于归一化坐标,不读取图像像素内容、效率高、隐私安全
"""

import math
import logging
from pathlib import Path
from dataclasses import dataclass,field
from typing import List,Dict,Optional
#从常量模块中导入任务类型和检测格式字段数
from utils.data_validation.constants import TaskType,DETECTION_FIELDS

logger = logging.getLogger(__name__)

#1，数据结构定义（使用dataclass装饰器）
@dataclass
class ClassStatistics:
    """
    单个类别完整统计数据的容器
    使用 @dataclass 装饰器的原因和好处:
    - Python 的dataclass 是Python 3.7+提供的"数据类”装饰器，它会自动为类生成_init_
    - 你只需要声明字段类型和默认值,就能得到一个干净、标准的类
    - 相比手动写_init __ (self,class_id, class_name, ... ),代码更简洁,更不容易出错
    - 特别适合”纯数据容器”(DTO- Data Transfer Object)场景,正好是我们这里的需求

    _repr、_eq_等常用方法
    """
    class_id:int
    class_name:str

    instance_count:int = 0
    image_count:int = 0
    bbox_areas:List[float] = field(default_factory = list)
    bbox_aspect_ratios:List[float] = field(default_factory = list)

    #===========================================================
    #使用@property装饰器定义计算属性
    #===========================================================

    @property
    def avg_area(self) -> float:
        """
        计算该类别所有bbox的平均归一化面积
        @property 装饰器的作用:
            - 让方法可以像"属性”一样被访问:obj.avg_area 而不是 obj.avg_area()
            - 实现"延迟计算”:只有在访问时才计算,不占用额外的存储空间
            - 保持接口简洁:调用者不需要知道这是计算得来的还是存储的
            - 这是Python 中实现“getter"的标准做法
        """
        #三元表达式处理空列表情况，避免除以0的错误
        return sum(self.bbox_areas) / len(self.bbox_aspect_ratios) if self.bbox_areas else 0.0

    @property
    def std_area(self) -> float:
        """
        该类别bbox面积的标准差（调用外部统一函数计算）
        :return:
        """
        return calculate_std(self.bbox_areas)

    @property
    def avg_aspect_ratio(self) -> float:
        """该类别所有bbox的平均长宽比"""
        return sum(self.bbox_aspect_ratios) / len(self.bbox_aspect_ratios) if self.bbox_areas else 0.0

    @property
    def std_aspect_ratio(self) -> float:
        """该类别的长度比的标准差"""
        return calculate_std(self.bbox_aspect_ratios)

@dataclass

class SplitStatistics:

    """单个数据集划分(train/val/test)的统计奎总容器。

    同样使用 @dataclass,自动生成初始化和打印方法。"""

    split_name: str# 划分名称,如"train"
    total_images: int = 0# 该划分总图像数
    total_instances: int = 0# 该划分总实例数(所有类别之和)
    class_stats: Dict[int, ClassStatistics] = field(default_factory=dict)

    def get_class_stat(self,class_id:int,class_name:str) -> ClassStatistics:
        """
        获取指定类别的统计对象（附加载模式）
        :param class_id:
        :param class_name:
        :return:
        """
        if class_id not in self.class_stats:
            self.class_stats[class_id] = ClassStatistics(class_id = class_id)
        return self.class_stats[class_id]

def calculate_std(data:List[float]) -> float:
    """
    计算样本标准差（Sample Standard Deviation）
    - 统计雪上,当从样本估计总体标准差时,使用n-1(贝塞尔校正)能得到无偏估计
    - 更适合我们这种”小样本推断总体”的场景
    - 如果数据少于2个,直接返回 0.0
    """
    if len(data) < 2:
        return 0.0
    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data) / (len(data) - 1)
    return math.sqrt(variance)

def parse_detection_label(parts: List[str]) -> Optional[Dict]:

    """解析一行检测任务(bounding box)的标签,提取所需统计指标。

    YOLO 检测格式:class_id x_center y_center width height (均为归一化)
    我们只需要width 和 height,来计算面积和长宽比"""

    if len(parts) != DETECTION_FIELDS: # 必须正好5个字段
        return None

    try:
        # 第一个字段(索引为9)转换为整数,代表目标的类别ID
        class_id = int(parts[0])
        # 将第4、5个字段(索引[3,4]转换为浮点数,分别代表月标的宽度和高度)
        w, h = float(parts[3]), float(parts[4])

        #校验宽高合法性
        if w > 0 and h > 0:
            return {
                "class_id": class_id,
                "width": w,
                "height": h,
                "area": w * h,
                "aspect_ratio": w / h
                }
    except (ValueError,IndexError):
        pass
    return None

def parse_segmentation_label(parts: List[str]) -> Optional[Dict]:
    """
    解析一行分割任务 (polygon) 的标签, 提取所需统计信息。

    YOLO 分割格式: class_id x1 y1 x2 y2 ... xn yn (归一化坐标)
    我们计算其外接矩形 (bounding box) 的宽高、面积、长宽比, 用于近似统计
    """
    # # 验证标签格式的合法性: 至少包含1个类别id + 3对坐标 (共7个元素)
    # # 并且坐标数量模2不等于0: 至少 class + 3 对坐标, 且坐标必须成对
    if len(parts) < 7 or len(parts) % 2 != 0:
        return None

    try:
        class_id = int(parts[0])
        # # 将第2个切片, 提取所有y2切片, 提取所有y坐标
        points = [float(p) for p in parts[1:]]  # 将除class_id外所有内容转换成浮点数, 得到所有坐标值列表

        # # 步长为2切片, 提取所有x坐标 (索引0, 2, 4, .....)
        xs = points[0::2]
        # # 步长为2切片, 提取所有y坐标 (索引1, 3, 5, .....)
        ys = points[1::2]

        # 计算外接矩形的宽度: x坐标的最大值 - 最小值
        w = max(xs) - min(xs)
        # 计算外接矩形的高度: y坐标的最大值 - 最小值
        h = max(ys) - min(ys)

        # # 过滤掉边界框的高位0的无效外接矩形
        if w > 0 and h > 0:
            # # 返回包含类别ID和外接矩形信息的字典
            return {
                "class_id": class_id,  # 目标类别ID
                "width": w,  # 外接矩形的宽度
                "height": h,  # 外接矩形的高度
                "area": w * h,  # 外接矩形面积
                "aspect_ratio": w / h  # 外接矩形长宽比
            }
        else:
            return None
    except (ValueError, IndexError):
        pass  # 转换失败视为无效数据, 忽略错误
    return None


def analyze_label_lines(lines: List[str],
                        task_type: str = TaskType.DETECTION
                        ) -> List[Dict]:
    """
    分析整个标签文件的所有行, 提取每条有效的统计信息

    Args:
        lines: 标签文件按行分割的内容
        task_type: 任务类型, 决定使用哪个解析器

    Returns:
        成功解析标签项列表 (每个元素是一个dict, 包含class_id, area 等)
    """
    results = []
    parser = parse_detection_label if task_type == TaskType.DETECTION else parse_segmentation_label

    for line in lines:
        parts = line.strip().split()  # 分割字符串, 移除首尾空格
        if not parts:  # 跳过空行
            continue

        parsed = parser(parts)
        if parsed:
            results.append(parsed)

    return results


# ==============================================================================
# 4. 核心统计函数
# ==============================================================================
def collect_split_statistics(image_paths: List[Path],
                             split_name: str,
                             class_names: List[str],
                             task_type: str = TaskType.DETECTION
                             ) -> SplitStatistics:
    """
    对单个数据集划分 (train/val/test) 进行完整统计分析

    遍历所有图像 -> 找到对应的标签 -> 解析每行 -> 更新统计指标

    Args:
        image_paths: 该划分所有图像路径列表 (通常来自 validate_get_image_path.py)
        split_name: 划分名称, 用于填充 SplitStatistics
        class_names: 类别名称的列表 (从 data.yaml)
        task_type: 任务类型

    Returns:
        SplitStatistics: 包含该划分统计数据的 SplitStatistics 对象
    """
    # # 初始化数据集划分的统计对象, 传入名称、总图像数和列表
    stats = SplitStatistics(split_name=split_name, total_images=len(image_paths))

    # # 遍历读取该划分的所有图像路径
    for img_path in image_paths:
        # # 推理标签路径: 标准 YOLO 布局 格式 图像/.../images/... -> Labels/.../labels/...
        label_with = img_path.parent.parent / "labels" / (img_path.stem + ".txt")

        # # 检查标签文件是否存在, 不存在则判定为无标注图像并记录日志
        if not label_with.exists():
            logger.debug(f"\"标签文件不存在 ({img_path.name})\": {{label_path}}")
            continue  # 跳过当前图像, 不进行后续统计

        try:
            # # 以 utf-8 编码打开标签文件, 读取所有行并进行换行符替换
            with open(label_with, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
        except Exception as e:
            # # 捕获读取异常, 记录错误日志
            logger.error(f"\"读取标签文件失败: {{label_path}}, 错误: {e}\"")
            continue  # 读取失败则跳过当前图像

        # # 如果标签文件内容为空 (无标注目标), 跳过该图像的统计
        if not lines:
            continue

        # # 定义集合用于存储当前图像中出现的类别 (集合自动去重, 用于统计图像数量)
        classes_in_image = set()

        # # 解析解析后的所有标注项
        parsed_items = analyze_label_lines(lines, task_type)

        # # 遍历解析后的每一条标注数据
        for item in parsed_items:
            class_id = item["class_id"]  # 获取当前标注目标的类别ID
            # # 安全获取类别名称, 防止 class_id 超出列表长度导致索引越界
            class_name = class_names[class_id] if class_id < len(class_names) else f"Unknown_{class_id}"

            # # 获取当前类别的统计对象, 若不存在则在自动创建, class_name
            class_stat = stats.get_class_stat(class_id, class_name)

            # # 更新各项指标
            # # 更新当前类别的实例数量 (每一条标注对应一个实例)
            class_stat.instance_count += 1
            # # 记录当前目标的边界框面积, 用于后续统计面积指标
            class_stat.bbox_areas.append(item["area"])
            # # 记录当前目标的边界框长宽比, 用于后续统计长宽比指标
            class_stat.bbox_aspect_ratios.append(item["aspect_ratio"])

            # # 将当前类别ID加入集合, 实现单张图内多种类别去重
            classes_in_image.add(class_id)

        # # 统计当前图像中出现的实例总数
        stats.total_instances += len(parsed_items)

        # # 每图像只计算一次该类别的图像数
        for class_id in classes_in_image:
            # # 更新整个数据集划分的总实例数
            stats.class_stats[class_id].image_count += 1

    logger.info(f"\"{split_name.upper()} 划分统计完成: {{stats.total_images}} 张图像, {{stats.total_instances}} 个实例\"")
    return stats


# ==============================================================================
# 5. 统计聚合函数 (用于多划分汇总)
# ==============================================================================
def aggregate_statistics(split_stats_list: List[SplitStatistics]) -> Dict[str, SplitStatistics]:
    """
    将多个划分的统计结果集合, 便于后续统一报告或可视化

    Args:
        split_stats_list: 多个 SplitStatistics 对象列表

    Returns:
        dict: key 为 split_name, value 为对应的统计对象
    """
    aggregated = {stats.split_name: stats for stats in split_stats_list}
    logger.info(f"\"统计聚合完成, 共 {{len(aggregated)}} 个划分\"")
    return aggregated