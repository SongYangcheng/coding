from pathlib import Path
from typing import list

from requests import get

ROOT_DIR: Path = Path(__file__).resolve().parent.parent

# 定义项目的核心目录信息
CONFIGS_DIR: Path = ROOT_DIR / "configs"
# 所有数据集相关目录
# YOLO 运行结果目录
#模型相关的目录
#正人央日的技心日承后品
DATA_DIR: Path = ROOT_DIR / "data"
RUNS_DIR: Path = ROOT_DIR / "runs"
MODELS_DIR: Path = ROOT_DIR / "models"
PRETRAINED_MODELS_DIR: Path = MODELS_DIR/"pretrained" # 预训练模型月录
CHECKPOINTS_DIR: Path = MODELS_DIR/"checkpoints" # 训练好的模型目录

SCRIPTS_DIR: Path = ROOT_DIR / "scripts" # 项目中的各类脚本目录
# 项目中的各类脚本目录
LOGGING_DIR: Path = ROOT_DIR/"loggint" # 日志文件统一存放目录

# 定义数据集的目录信息
RAW_DATA_DIR: Path = DATA_DIR / "raw"
DEFATULE_DIR1:Path = DATA_DIR/"8"
DEFATULE_DIR2:Path = DATA_DIR/"11"

YOLO_STAGED_DIR: Path = RAW_DATA_DIR / "yolo_staged_labels"  # YOLO格式标注数据集目录
TRAIN_DIR: Path = DATA_DIR / "train"  # 训练集目录
VAL_DIR: Path = DATA_DIR / "val"      # 验证集目录
TEST_DIR: Path = DATA_DIR / "test"    # 测试集目录

TRAIN_IMAGES_DIR: Path = TRAIN_DIR / "images"  # 训练集图像目录
TRAIN_LABELS_DIR: Path = TRAIN_DIR / "annotations"  # 训练集标签目录
VAL_IMAGES_DIR: Path = VAL_DIR / "images"
VAL_LABELS_DIR: Path = VAL_DIR / "annotations"

TEST_IMAGES_DIR: Path = TEST_DIR / "images"
TEST_LABELS_DIR: Path = TEST_DIR / "annotations"
# 其他辅助信息
DOCS_dir = ROOT_DIR / "docs"  # 项目文档目录
UNIT_TEST_DIR: Path = ROOT_DIR / "tests"  # 单元测试目录
TEST_SAMPLLES_DIR: Path = ROOT_DIR / "test_samples"  # 测试样本目录
TEST_SAMPLLES_DIR: Path = TEST_SAMPLLES_DIR / "images"  # 测试样本图像目录


def get_dirs_to_initialize() -> list[Path]:
    """获取需要在项目初始化时创建的目录列表"""
    return [
        CONFIGS_DIR,
        DATA_DIR,
        RUNS_DIR,
        MODELS_DIR,
        PRETRAINED_MODELS_DIR,
        CHECKPOINTS_DIR,
        SCRIPTS_DIR,
        LOGGING_DIR,
        # RAW_DATA_DIR,
        # TRAIN_DIR,
        VAL_DIR,
        TEST_DIR,
        TRAIN_IMAGES_DIR,
        TRAIN_LABELS_DIR,
        VAL_IMAGES_DIR,
        VAL_LABELS_DIR,
        TEST_IMAGES_DIR,
        TEST_LABELS_DIR,
        DOCS_dir,
        UNIT_TEST_DIR,
        TEST_SAMPLLES_DIR,
    ]
if __name__ == "__main__":
    #运行时获取实际路径依赖
    dir_to_create = get_dirs_to_initialize()
    print("初始化目录信息")
    for p in dir_to_create:
        p.mkdir(parents=True,exist_ok=True)
        print(f"已创建目录: {p}")