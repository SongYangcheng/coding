#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :paths.py
# @Project   :yolo_server
# @Function  :集中定义项目中所有的重要的路径信息，使用pathlib模块, 可自动适配不同操作系统的路径分隔符
from pathlib import Path
from typing import List

ROOT_DIR: Path = Path(__file__).resolve().parent.parent

# 定义项目的核心目录信息
CONFIGS_DIR: Path = ROOT_DIR / "configs"  # 配置文件目录
DATA_DIR: Path = ROOT_DIR / "data"  # 所有数据集相关的目录
RUNS_DIR: Path = ROOT_DIR / "runs"  # YOLO 运行结果目录
MODELS_DIR: Path = ROOT_DIR / "models"  # 模型相关的目录

PRETRAINED_MODELS_DIR: Path = MODELS_DIR / "pretrained"  # 预训练模型目录
CHECKPOINTS_DIR: Path = MODELS_DIR / "checkpoints"  # 训练好的模型目录

SCRIPTS_DIR: Path = ROOT_DIR / "scripts"  # 项目中各类脚本目录
LOGGING_DIR: Path = ROOT_DIR / "logging"  # 日志文件统一存放目录

# 定义数据集的目录信息
RAW_DATA_DIR: Path = DATA_DIR / "raw"  # 原始数据集目录
# RAW_IMAGES_DIR: Path = RAW_DATA_DIR / "images"  # 原始图片数据集目录
# RAW_ANNOTATIONS_DIR: Path = RAW_DATA_DIR / "annotations"  # 原始标注数据集目录，可以放放各种格式的标注文件

YOLO_STAGED_LABELS_DIR: Path = RAW_DATA_DIR / "yolo_staged_labels"  # 标准转换过程中生成的标签文件目录临时的

TRAIN_DIR: Path = DATA_DIR / "train"
VAL_DIR: Path = DATA_DIR / "val"
TEST_DIR: Path = DATA_DIR / "test"

TRAIN_IMAGES_DIR: Path = TRAIN_DIR / "images"
TRAIN_LABELS_DIR: Path = TRAIN_DIR / "annotations"

VAL_IMAGES_DIR: Path = VAL_DIR / "images"
VAL_LABELS_DIR: Path = VAL_DIR / "annotations"

TEST_IMAGES_DIR: Path = TEST_DIR / "images"
TEST_LABELS_DIR: Path = TEST_DIR / "annotations"

# 其他辅助目录信息
DOCS_DIR: Path = ROOT_DIR / "docs"
UNIT_TEST_DIR: Path = ROOT_DIR / "tests"
TEST_SAMPLES_DIR: Path = ROOT_DIR / "test_samples"
TEST_SAMPLES_IMAGES_DIR: Path = TEST_SAMPLES_DIR / "images"

def get_dirs_to_initialize() -> List[Path]:
    """
    获取需要初始化的目录列表
    :return:
    """
    return [
        CONFIGS_DIR,
        DATA_DIR,
        RUNS_DIR,
        MODELS_DIR,
        PRETRAINED_MODELS_DIR,
        CHECKPOINTS_DIR,
        SCRIPTS_DIR,
        LOGGING_DIR,
        RAW_DATA_DIR,
        # RAW_IMAGES_DIR,
        # RAW_ANNOTATIONS_DIR,
        YOLO_STAGED_LABELS_DIR,
        TRAIN_IMAGES_DIR,
        TRAIN_LABELS_DIR,
        VAL_IMAGES_DIR,
        VAL_LABELS_DIR,
        TEST_IMAGES_DIR,
        TEST_LABELS_DIR,
        DOCS_DIR,
        UNIT_TEST_DIR,
        TEST_SAMPLES_DIR,
        TEST_SAMPLES_IMAGES_DIR
    ]

# def get_raw_data_dirs_to_check() -> Dict[str, Path]:
#     """
#     获取需要检查的原始数据集目录列表
#     :return:
#     """
#     return {
#         "RAW_IMAGES_DIR": RAW_IMAGES_DIR,
#         "RAW_ANNOTATIONS_DIR": RAW_ANNOTATIONS_DIR
#     }

if __name__ == "__main__":
    # 运行时获取实际路径信息
    dir_to_create = get_dirs_to_initialize()
    print("\n===== 初始化目录信息 =====")
    for p in dir_to_create:
        p.mkdir(parents=True, exist_ok=True)
    print("\n===== 创建完成 =====")