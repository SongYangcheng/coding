# 常量定义
#职责：定义项目中使用的常量，便于统一管理和修改
""""常量定义模块：定义数据集合验证过程中使用的所有常量，包括：
- 支持的图像格式
- YOLO数据集的划分
- 文件编码
- 日志前缀
"""
#支持的图像文本扩展名
from tarfile import DEFAULT_FORMAT
from tkinter import SE

from pyparsing import Word


IMG_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif"]

#YOLO的数据集的划分标准
YOLO_SPLITS = ["train", "val", "test", "trainval"]
#默认文件编码
DEFAULT_FILE_ENCODING = "utf-8"
# 验证模式
class ValidationMode:
    SPMPLE = "sample"  # 采样验证模式
    FULL = "full"      # 全量验证模式

#人物类型
class TaskType:
    DETECTION = "detection"  # 目标检测
    SEGMENTATION = "segmentation"  # 图像分割

#YOLO标签格式要求
DETECTION_FIELDS = 5 #单个目标标准信息必须包含的字段总数为5：class_id + x_center + y_center + width + height
SEGMENTATION_FIELDS = 7 #class_id + 至少三个坐标点，定义了YOLO实例分割中，单个目标标注信息最小的字段总数为class_id + 至少三个坐标点
#默认采样参数
DEFAULT_SAMPLE_RATIO = 0.1 #该参数表示默认的采样比例，均值为0.1（10%为验证样本）
DEFAULT_MIN_SAMPLE_COUNT = 20 #该参数表示默认的最小采样数量，均值为20（至少20个样本用于验证）
SEGMENTATION_MIN_FIELDS = 20 #实例分割模式最小字段数