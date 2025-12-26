# -*- coding: utf-8 -*-
"""
# 预处理模块
# 包含数据加载、预处理和增强功能
"""
import cv2
import numpy as np
from pathlib import Path
import albumentations as A
from albumentations.pytorch import ToTensorV2
import torch
from torch.utils.data import Dataset, DataLoader
import yaml


class SafetyDataset(Dataset):
    """
    "安全监测数据集"
    """

    def __init__(self, images_dir, labels_dir, img_size=640, augment=False):
        self.images_dir = Path(images_dir)
        self.labels_dir = Path(labels_dir)
        self.img_size = img_size
        self.augment = augment

        # 获取所有图像文件
        self.img_files = sorted(list(self.images_dir.glob("*.jpg"))) + \
                         list(self.images_dir.glob("*.png"))

        # 数据增强配置
        if augment:
            self.transform = A.Compose([
                # 随机缩放裁剪: 从原图0.8-1.0倍的区域裁剪resize到指定尺寸, 提升模型对物体尺度跨性的鲁棒性
                A.RandomResizedCrop(height=img_size, width=img_size, scale=(0.8, 1.0), p=0.5),
                # 随机水平翻转: 以50%的概率翻转图像, 增加数据多样性, 适用于无左右朝向限制的目标检测任务
                A.HorizontalFlip(p=0.5),
                # 随机亮度与对比度调整: 亮度和对比度的调整范围为±20%, 概率50%, 模拟不同的光照条件
                A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.5),
                # 色彩抖动: 随机色彩和亮度调整, 色调偏移±20, 饱和度和亮度±30, 适应不同的色彩环境
                A.HueSaturationValue(hue_shift_limit=20, sat_shift_limit=30, val_shift_limit=20, p=0.5),
                # 随机添加高斯噪声: 噪声⽅差范围10-50, 概率30%, 提升模型的抗噪声能力
                A.GaussNoise(var_limit=(10.0, 50.0), p=0.3),
                # 随机高斯模糊: 模板大小3-7, 概率30%, 模拟图像失焦情况
                A.GaussianBlur(blur_limit=(3, 7), p=0.3),
                # 随机平移缩放旋转: 平移范围±10%, 缩放范围±20%, 旋转范围±15度, 概率50%, 增强目标姿态鲁棒性
                A.ShiftScaleRotate(shift_limit=0.1, scale_limit=0.2, rotate_limit=15, p=0.5),
                # 随机遮挡: 最多生成8个孔洞, 单个孔洞最大宽32, 概率30%, 模拟物体部分遮挡的场景
                A.CoarseDropout(max_holes=8, max_h_size=32, max_w_size=32, p=0.3),
                # 标准化: 使用ImageNet数据集的均值和标准差, 加速模型训练收敛
                A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
                # 将PIL图像/NumPy数组转换为PyTorch张量, 并调整通道顺序为[C, H, W]
                ToTensorV2(),
            ],
                bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']) # 边界框参数: 格式为Yolo (归一化中心坐标x, y, w, h)
            )
        else:
            # # 当图像无标注时, 仅传入图像和空的标注、标签列表 (无数据增强, 避免引入额外噪声)
            self.transform = A.Compose([
                A.Resize(height=img_size, width=img_size), # 直接resize到尺寸, 保证输入尺寸统一
                A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
                # 转换为PyTorch张量
                ToTensorV2(),
            ],
                bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels'])
            )

    def __len__(self):
        return len(self.img_files)

    def __getitem__(self, idx):
        # 加载图像
        img_path = self.img_files[idx]
        image = cv2.imread(str(img_path))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 加载标注
        label_path = self.labels_dir / f"{img_path.stem}.txt"
        bboxes = []
        class_labels = []

        # 判断标签文件是否存在
        if label_path.exists():
            # 只读取只读模式的字符串文件
            with open(label_path, "r") as f:
                for line in f:
                    # 去除每行首尾空字符, 并按空格分割成多个子段
                    parts = line.strip().split()
                    # 校验字段数量: YOLO格式标签需至少包含 类别ID + 4个边界框参数 (x, y, w, h)
                    if len(parts) >= 5:
                        # 提取第一个字段为目标类别ID, 并转换为整数类型
                        class_id = int(parts[0])
                        # 提取后4个字段为边界框参数 (x_center, y_center, width, height), 转换为浮点型
                        bbox = [float(p) for p in parts[1:5]]
                        # 将当前目标的类别ID添加到类别标签中
                        class_labels.append(class_id)
                        # 将边界框添加到边界框列表
                        bboxes.append(bbox)

        # 应用数据增强
        if self.augment and len(bboxes) > 0:
            # 当图像存在标注时, 图像、标注、类别标签进行同步变换
            # # 保证增强操作 (如裁剪、翻转) 同时作用于图像和对应的标准信息, 避免标签错位
            transformed = self.transform(image=image, bboxes=bboxes, class_labels=class_labels)
            # # 变换后的图像
            image = transformed['image']
            # # 变换后的标注框数据
            bboxes = transformed['bboxes']
            # # 提取变换后的类别标签数据
            class_labels = transformed['class_labels']
        else:
            # # 当图像无标注时, 仅传入图像和空的标注、标签列表
            transformed = self.transform(image=image, bboxes=[], class_labels=[])

        return {
            'image': image,
            'bboxes': torch.tensor(bboxes, dtype=torch.float32) if bboxes else torch.zeros((0, 4), dtype=torch.float32),
            'labels': torch.tensor(class_labels, dtype=torch.long) if class_labels else torch.zeros((0,), dtype=torch.long),
            'image_path': str(img_path)
        }


def create_dataloaders(data_yaml_path, batch_size=16, img_size=640, workers=4):
    """
    创建数据加载器

    Args:
        data_yaml_path (str): 数据集配置文件路径, 包含训练/验证集路径、类别等信息
        batch_size (int, optional): 图像缩放后的尺寸, 默认16
        img_size (int, optional): 图像缩放后的尺寸, 默认640
        workers (int, optional): 数据加载的进程数, 默认4

    Returns:
        tuple: (train_dataloader, val_dataloader)
    """
    # 读取数据集的配置文件 (YAML格式), 解析训练集、验证集的路径等信息
    with open(data_yaml_path, 'r', encoding='utf-8') as f:
        data_config = yaml.safe_load(f)

    # 获取数据根路径, 并转换为Path对象 (方便路径拼接操作)
    base_path = Path(data_config['path'])

    # 创建满足条件的数据集的实例操作
    # 创建训练集实例操作
    train_dataset = SafetyDataset(
        images_dir=base_path / data_config['train'],  # 训练集图像文件的路径
        labels_dir=base_path / data_config['train'].replace('images', 'labels'),  # 训练集标签文件夹路径
        img_size=img_size,  # 图像缩放尺寸
        augment=True  # 开启训练阶段的数据增强
    )

    # 创建验证数据集实例
    val_dataset = SafetyDataset(
        images_dir=base_path / data_config['val'],  # 验证集图像文件的路径
        labels_dir=base_path / data_config['val'].replace('images', 'labels'),  # 验证集标签文件夹路径
        img_size=img_size,  # 图像缩放尺寸
        augment=False  # 关闭验证阶段的数据增强, 避免引入额外噪声
    )

    # 创建数据加载器
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,  # 训练集打乱顺序
        num_workers=workers,
        pin_memory=True,  # 加速CPU到GPU的数据传输
        collate_fn=lambda batch: {k: [d[k] for d in batch] for k in batch[0]}  # 自定义collate_fn以支持列表
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,  # 验证集不打乱顺序
        num_workers=workers,
        pin_memory=True,
        collate_fn=lambda batch: {k: [d[k] for d in batch] for k in batch[0]}
    )

    return train_loader, val_loader