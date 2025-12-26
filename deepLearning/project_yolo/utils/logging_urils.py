import logging
import sys
import platform
from datetime import datetime
from pathlib import Path
from colorlog import ColoredFormatter
from cv2 import log
from pandas import Timestamp

def get_logger(base_path: Path, log_type: str = "general", model_name: str|None = None,
               log_level: int = logging.INFO, temp_log:bool = False, encoding: str = "utf-8", 
               logger_name: str = "SafeYolo") -> logging.Logger:
    """
    参数:
        base_path (Path): 日志文件的基础路径。
        log_type (str): 日志类型（如 "train", "val", "test", "general"）。
        model_name (str|None): 模型名称（可选）。
        log_level (int): 日志记录级别。
        temp_log (bool): 是否创建临时日志文件。
        encoding (str): 日志文件的编码格式。
        logger_name (str): 日志记录器的名称。
    
    """
    #1. 获取命名Logger使用固定名称可以确保项目所有的模块共享同一个日志记录器
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    logger.propagate = False  # 防止日志重复输出

    #2. 创建简短专属日志记录
    log_dir: Path = base_path / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    #3. 构建日志文件名称
    timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")[:21]
    #文件的前缀
    prefix = "temp" if temp_log else log_type.replace("_", "-")
    #定义文件名称
    filename_parts = [prefix, timestamp]
    if model_name:
        #清理模型名称的非法字符
        sanitized_model = "".join(c if c.isalnum() or c in "_" else "_" for c in model_name)
        filename_parts.append(sanitized_model)
    log_filename = str = "_".join(filename_parts) + ".log"
    log_file: Path = log_dir / log_filename
    #4. 创建文件处理器
    file_formatter = logging.Formatter(
        fmt="%(asctime)s-%(name)s-%(levelname)-8s-%(filename)s-%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler = logging.FileHandler(log_file, encoding=encoding)
    file_handler.setLevel(log_level)
    file_handler.addHandler(file_formatter)
    #5.创建控制台处理器配置文件Handler样式
    console_formatter = ColoredFormatter(
        fmt="%(log_color)s%(asctime)s-%(name)s-%(levelname)-8s-%(filename)s-%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
        secondary_log_colors={},
        style="%"
    )
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

if __name__ == "__main__":
    # 测试日志记录器
    print("\n=======环境信息==========")
    print(f"操作系统: {platform.system()} {platform.release()}")
    print(f"项目已经启动，当前环境为：{platform.system()} {platform.release()}")