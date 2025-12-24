#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
文件清理模块

职责：
- 删除验证失败的图像和标签文件
- 记录删除操作
- 提供安全的删除机制（二次确认）
"""

import logging
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple
import sys

logger = logging.getLogger(__name__)

@dataclass
class InvalidSample:
    """无效样本数据类"""
    image_path: Path
    label_path: Path
    error_message: str
    split_name: str


def delete_invalid_samples(
    invalid_samples: List[InvalidSample],
    auto_delete: bool = False
) -> Tuple[int, int]:
    """
    删除无效样本的图像和标签文件

    Args:
        invalid_samples: 无效样本列表
        auto_delete: 是否自动删除 (不询问确认)

    Returns:
        Tuple[int, int]: (删除的图像数, 删除的标签数)
    """
    if not invalid_samples:
        logger.info("没有需要删除的无效样本")
        return 0, 0
    
    logger.warning(f"发现 {len(invalid_samples)} 个无效样本")

    # 显示前10个示例
    print("\n无效样本示例 (前10个): ")
    for i, sample in enumerate(invalid_samples[:10], 1):
        print(f"  {i}. {sample.image_path.name} - {sample.error_message}")
    
    if len(invalid_samples) > 10:
        print(f"  ...还有 {len(invalid_samples) - 10} 个")

    # 确认删除
    if not auto_delete:
        if not sys.stdin.isatty():
            logger.info("非交互环境且未指定 --auto-delete 跳过删除")
            return 0, 0
        
        print(f"\n是否删除这 {len(invalid_samples)} 个无效样本? ")
        response = input("请输入 'yes' 确认删除: ").strip().lower()

        if response != 'yes':
            logger.info("用户取消删除操作")
            return 0, 0
    
    # 执行删除
    deleted_images = 0
    deleted_labels = 0

    for sample in invalid_samples:
        try:
            # 删除图像
            if sample.image_path.exists():
                sample.image_path.unlink()
                deleted_images += 1
                logger.debug(f"已删除图像: {sample.image_path}")
            
            # 删除标签
            if sample.label_path.exists():
                sample.label_path.unlink()
                deleted_labels += 1
                logger.debug(f"已删除标签: {sample.label_path}")
        except Exception as e:
            logger.error(f"删除失败 {sample.image_path.name}: {e}")
    
    logger.info(f"删除完成: {deleted_images} 个图像, {deleted_labels} 个标签")
    return deleted_images, deleted_labels