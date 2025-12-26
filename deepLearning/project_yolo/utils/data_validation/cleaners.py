#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 文件清洗模块
# 提供无效数据文件的清理功能

import sys
import logging
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class InvalidSample:
    """无效样本数据结构"""
    image_path: Path
    label_path: Path
    error_message: str
    split_name:str

def delete_invalid_files(invalid_samples: List[InvalidSample],
                         auto_delete: bool = False
                        ) -> Dict[int, int]:


    if not invalid_samples:
        logger.info("没有需要删除的无效样本")
        return 0.0

    logger.warning(f"发现{len(invalid_samples)}个无效样木")

    # 显示前10个示例
    print("\n无效样本示例(前10个):")
    for i, sample in enumerate(invalid_samples[: 10], 1):
        print(f" {i}. {sample.image_path.name} - {sample.error_message}")

    if len(invalid_samples) > 10:
        print(f" ... 还有{len(invalid_samples) - 10}个")

        # 确认删除
    if not auto_delete:
        if not sys.stdin.isatty():
            logger.info("非交互环境且未指定 - - auto - delete, 跳过删除")
            return 0,0

        print(f"\n是否删除这 {len(invalid_samples)}个无效样本?")
        response = input("请输入‘yes’确认删除:").strip().lower()

        if response != 'yes':
            logger.info("用户取消删除操作")
            return 0,0
    # 执行删除
    deleted_images = 0
    deleted_labels = 0

    for sample in invalid_samples:
        try:
            # 删除图像
            if sample.image_path.exists():
                sample.image_path.unlink()
                deleted_images += 1
                logger.debug(f"已删除图像:{sample.image_path}")

            # 删除标签
            if sample.label_path.exists():
                sample.label_path.unlink()
                deleted_labels += 1
                logger.debug(f"已删除标签:{sample.label_path}")
        except Exception as e:
            logger.error(f" {sample.image_path.name}: {e}")

    logger.info(f"删除完成:{deleted_images}个图像,{deleted_labels}")
    return deleted_images,deleted_labels
