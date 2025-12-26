# 可视化输出
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""可视化输出模块

职责:
1. 格式化输出验证结果到日志系统
2. 提供统一的输出样式(标题、分节、表格等)
3. 输出数据集统计,类别分布、无效样本等信息

设计说明:
- 使用 Logger 而非 print,与项目日志系统统一
- 所有函数支持传入 Logger 参数,灵活配置不同调用场景
- 若未传入 Logger,则使用模块默认的 Logger(便于单独测试)
"""
import logging
from typing import Dict, List, Optional

# 导入数据类(用于类型注解)
from utils.data_validation.analyzers import SplitStatistics
from utils.data_validation.cleaners import InvalidSample

from utils.string_utils import (
        get_display_width,# 获取字符串的显示宽度
        pad_to_width,# 将字符串填充到指定的显示宽度(用于对齐)
        format_table_row,# 格式化表格的一行内容(生成规划的表格行字符串)
        format_table_separator# 格式化表格的分隔线(生成表格的横线分隔符)
)

# 内部工具函数

def _get_logger(logger: logging.Logger = None) -> logging.Logger:

    """获取 Logger 实例
    设计说明:
    如果使用方传入 Logger,则使用传入的 Logger;
    否则使用模块默认的 Logger(名称为"data_validation.visualizers")
    这样设计既支持集成到项目日志系统,又支持独立测试
    Args:
    Logger:外部传入的 Logger 实例,可为 None

    Returns:
    Logging.Logger:可用的 Logger 实例"""

    return logger if logger else logging.getLogger( __name__)

def _section(title: str, width: int = 60, char: str = "-") -> str:
    return f"\n{char * 3} {title} {char * (width - len(title) - 5)}"

def log_dataset_summary(
    yaml_path: str,
    nc: int,
    class_names: List[str],
    splits_info: Dict[str, Dict],
    logger: logging.Logger = None):
    # 输出标题
    log.info(_header("数据集摘要 Dataset Summary"))
    # 输出基本结构
    log.info(f"配置文件:{yaml_path}")
    log.info(f"类别数量:{nc}")
    log.info(f"类别列表:{','.join(class_names)}")
    log.info("")
    # 输出各划分信息
    log.info("数据集划分:")