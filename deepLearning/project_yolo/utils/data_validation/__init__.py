#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
YOLO 数据集模块验证功能, 包括:
    - 配置文件验证
    - 文件完整性检查
    - 标签格式式验证
    - 数据统计分析
    - 划分唯一性检查
    - 无效样本清理
    - 可视化图表生成
    - 验证报告生成
"""

__version__ = "1.0.0"
__author__ = "0.0"

# 导出核心类和函数
from .constants import (
    IMG_EXTENSIONS,
    YOLO_SPLITS,
    ValidationMode,
    TaskType,
    DETECTION_FIELDS,
    SEGMENTATION_MIN_FIELDS,
)
from .validators import (
    load_yaml_config,
    validate_yaml_content,
    get_image_paths,
    validate_label_content,
    validate_image_label_pair,
    validate_split_uniqueness,
)
from .analyzers import (
    ClassStatistics,
    SplitStatistics,
    collect_split_statistics,
    aggregate_statistics,
)
from .cleaners import (
    InvalidSample,
    delete_invalid_samples,
)
from .reporters import (
    ValidationReport,
    ReportBuilder,
    save_report,
)

__all__ = [
    # 常量
    "IMG_EXTENSIONS",
    "YOLO_SPLITS",
    "ValidationMode",
    "TaskType",
    "DETECTION_FIELDS",
    "SEGMENTATION_MIN_FIELDS",
    # 验证器
    "load_yaml_config",
    "validate_yaml_content",
    "get_image_paths",
    "validate_label_content",
    "validate_image_label_pair",
    "validate_split_uniqueness",
    # 分析器
    "ClassStatistics",
    "SplitStatistics",
    "collect_split_statistics",
    "aggregate_statistics",
    # 清理器
    "InvalidSample",
    "delete_invalid_samples",
    # 报告器
    "ValidationReport",
    "ReportBuilder",
    "save_report",
]