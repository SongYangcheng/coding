from __future__ import annotations  
import platform   # 平台相关信息
import re
import sys
import time
import logging
from pathlib import Path
from typing import Optional

from matplotlib.style import available
from numpy import isin
import torch
from ultralytics import __version__ as ultralytics_version

from utils.string_utils import pad_to_width, format_table_row, format_table_separator

def _format_size(bytes_size: int | float | None) -> str:
    """简洁内存硬盘大小格式化"""
    if not bytes_size or not isinstance(bytes_size, (int, float)):
        return "N/A"
    if bytes_size >= 1024 ** 3:
        return f"{bytes_size/(1024 ** 3):.2f}GB"
    if bytes_size >= 1024 ** 2:
        return f"{bytes_size/(1024 ** 3):.2f}MB"
    return f"{bytes_size / 1024:.2f}KB"

def get_basic_device_info() -> dict:
    """
    获取基础设备信息（无额外依赖）
    return：
    dict: 结构化信息字典
    """
    cpu_name = platform.processor() or platform.machine() or "Unknown CPU"
    cpu_cores = platform.machine() or "Unknown Cores"
    try:
        import psutil # 仅在可用时导入
        memory = psutil.virtual_memory() # type: ignore
        total_ram = _format_size(memory.total)
        ram_usage_percent = f"{memory.percent:.1f}%"
    except ImportError:
        total_ram = "unknown"
        available_ram = "unknown"
        ram_usage_percent = "unknown"
        memory = None
    
    #GPU信息
    cuda_available = torch.cuda.is_available()
    gpu_info = {
        "CUDA 可用": cuda_available,
        "GPU 数量": torch.cuda.device_count() if cuda_available else 0,
    }
    if cuda_available:
        for i in range(torch.cuda.device_count()):
            gpu_name = torch.cuda.get_device_name(i)
            gpu_memory = _format_size(torch.cuda.get_device_properties(i).total_memory)
            gpu_info[f"GPU {i} 名称"] = gpu_name
            gpu_info[f"GPU {i} 内存"] = gpu_memory
    return {
        "系统信息":{
            "操作系统": platform.system() + " " + platform.release(),
            "平台": platform.platform(),
            "处理器": cpu_name,
            "CPU 核心数": cpu_cores,
            "总内存": total_ram,
            "内存使用率": ram_usage_percent,
            "Python 版本": platform.python_version(),
            "当前时间": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        },
        "PyTorch 信息":{
            "PyTorch 版本": torch.__version__,
            "CUDA 版本": torch.version.cuda,
            "cuDNN 版本": torch.backends.cudnn.version(),
        },
        "Ultralytics 信息":{
            "Ultralytics 版本": ultralytics_version,
        },
        "GPU 信息": gpu_info,
    }

def log_device_info(logger: Optional[logging.logger] = None) -> dict: #->None表示返回无值
    """
    记录设备信息到日志或控制台
    参数:
        logger (Optional[logging.Logger]): 可选的日志记录器实例。如果未提供，则打印到控制台。
    返 回:
        dict: 结构化信息字典
    """
    if logger is None:
        logger = logging.getlogger(__name__)
    info = get_basic_device_info()
    logger.info("训练环境预览")
    logger.info("-" * 40)
    key_width = 20

    for category, datails in info.items():
        logger.info(f"{category}".center(60))
        logger.info("-" * 40)
        if isinstance(datails, dict):
            for key, value in datails.items():
                logger.info(f"{pad_to_width(key, key_width)}: {value}")
        else:
            logger.info(f"{datails}")
    return info