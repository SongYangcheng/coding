"""
训练器模块
包含完整的训练流程、EMA、学习率调度和可视化
"""
import sched
import torch
import numpy as np
from pathlib import Path
from datetime import datetime

from core import optimize
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg') # 非交互式后端
from ultralytics import YOLO
import yaml
import json

class Trainer:
    """训练器类"""

    def __init__(
        self,
        model,
        data_yaml,
        project_name='run/train',
        epochs=100,
        batch_size=16,
        img_size=640,
        device='cuda',
        user_ema=True,
        optimizer_type='Auto',
        scheduler_type='cosine',
        save_period=10,
    ):
        """
        Args:
            model: YOLO模型实例
            data_yaml: 数据集配置文件路径
            project_name: 项目输出目录
            epochs: 训练轮数
            batch_size: 批次大小
            img_size: 图像大小
            device: 设备('cuda' 或 'cpu')
            user_ema: 是否使用ema
            optimizer_type: 优化器类型
            scheduler_type: 学习率调度器类型
            save_period: 保存周期
        """

        self.model = model
        self.data_yaml = data_yaml
        self.epochs = epochs
        self.batch_size = batch_size
        self.img_size = img_size
        self.device = device
        self.user_ema = user_ema
        self.optimizer_type = optimizer_type
        self.scheduler_type = scheduler_type
        self.save_period = save_period

        # 创建输出目录
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.save_dir = Path(project_name) / timestamp
        self.save_dir.mkdir(parents=True, exist_ok=True)

        # 训练历史
        self.history = {    # 创建历史记录字典，用于保存训练过程中的各类关键指标
            'train_loss': [],       # 训练集损失值列表，按训练轮次/迭代次数存储
            'val_loss': [],         # 验证集损失值列表，按验证轮次存储
            'metrics': {            # 目标检测核心任务评估指标的字典
                'mAP50': [],        # 交并比阈值为0.5时的平均精度均值列表
                'mAP50-95': [],     # 交并比阈值从0.5到0.95 (步长0.05) 的平均精度均值列表
                'precision': [],    # 精确率列表，衡量预测为正样本的准确性
                'recall': [],       # 召回率列表，衡量真实正样本被检出的比例
            },
            'lr': [],               # 学习率列表，按训练轮次/迭代次数存储，用于监督学习率变化
        }

        print(f"\n{'='*80}")
        print(f" 训练器初始化")
        print(f"{'-'*80}")
        print(f" 输出目录: {self.save_dir}")
        print(f" 训练配置:")
        print(f" 轮数: {epochs}")
        print(f" 批次大小: {batch_size}")
        print(f" 图像大小: {img_size}")
        print(f" 设备: {device}")
        print(f" EMA: {'启用' if user_ema else '禁用'}")
        print(f" 优化器: {optimizer_type}")
        print(f" 学习率调度: {scheduler_type}")

def train(self):
    """开始训练"""
    print(f"\n{'='*80}")
    print(f" 开始训练")
    print(f"{'='*80}\n")

    try:
        # 使用 Ultralytics 的训练接口
        results = self.model.train(
            data=self.data_yaml,
            epochs=self.epochs,
            batch=self.batch_size,
            imgsz=self.img_size,
            device=self.device,
            project=str(self.save_dir.parent),
            name=self.save_dir.name,
            exist_ok=True,

            # 优化器配置
            optimizer=self.optimizer_type,
            lr0=0.01,
            lrf=0.01,
            momentum=0.937,
            weight_decay=0.0005,
            warmup_epochs=3.0,
            warmup_momentum=0.8,
            warmup_bias_lr=0.1,

            # 学习率调度
            cos_lr=True if self.scheduler_type == 'cosine' else False,

            # EMA
            ema=self.user_ema,

            # 数据增强
            hsv_h=0.015,
            hsv_s=0.7,
            hsv_v=0.4,
            degrees=0.0,
            translate=0.1,
            scale=0.5,
            shear=0.0,
            perspective=0.0,
            flipud=0.0,
            fliplr=0.5,
            mosaic=1.0,
            mixup=0.0,
            copy_paste=0.0,
            auto_augment='randaugment',
            erasing=0.4,
            crop_fraction=1.0,

            # 训练设置
            patience=50,
            save=True,
            save_period=self.save_period,
            cache=False,
            pretrained=True,
            verbose=True,
            seed=42,
            deterministic=True,
            single_cls=False,
            rect=False,
            resume=False,
            amp=True,
            fraction=1.0,
            profile=False,
            freeze=None,

            # 损失权重
            box=0.75,
            cls=0.5,
            dfl=1.5,
            pose=12.0,
            kobj=1.0,
            label_smoothing=0.0,
            nbs=64,

            # 关闭mosaic的轮数
            close_mosaic=10,
        )

        print(f"\n{'='*80}")
        print(f"√ 训练完成!")
        print(f"{'='*80}")

        # 提取训练历史
        self._extract_training_history()

        # 绘制训练曲线
        self.plot_training_curves()

        # 验证最佳模型
        self.validate_best_model()

        # 保存训练配置
        self.save_training_cofing()

        return results

    except Exception as e:
        print(f"\n× 训练失败: {str(e)}")
        raise

def _extract_training_history(self):
    """从训练结果中提取历史数据"""
    result_csv = self.save_dir / 'results.csv'

    if result_csv.exists():
        import pandas as pd
        df = pd.read_csv(result_csv)
        df.columns = df.columns.str.strip()

        # 提取损失和指标
        if 'train/box_loss' in df.columns:
            self.history['train_loss'] = df['train/box_loss'].tolist()
        if 'val/box_loss' in df.columns:
            self.history['val_loss'] = df['val/box_loss'].tolist()
        if 'metrics/mAP50(B)' in df.columns:
            self.history['metrics']['mAP50'] = df['metrics/mAP50(B)'].tolist()
        if 'metrics/mAP50-95(B)' in df.columns:
            self.history['metrics']['mAP50-95'] = df['metrics/mAP50-95(B)'].tolist()
        if 'metrics/precision(B)' in df.columns:
            self.history['metrics']['precision'] = df['metrics/precision(B)'].tolist()
        if 'metrics/recall(B)' in df.columns:
            self.history['metrics']['recall'] = df['metrics/recall(B)'].tolist()
        if 'lr/box' in df.columns:
            self.history['lr'] = df['lr/box'].tolist()

def plot_training_curves(self):
    """绘制训练曲线"""
    print(f'\n绘制训练曲线....')

    fig, axes = plt.subplot(2, 3, figsize=(15, 12))
    fig.suptitle('Training Curves', fontsize=16, fontweight='bold')
    epochs = range(1, len(self.history['train_loss']) + 1) if self.history['train_loss'] else []
    #1. 损失曲线
    if self.history['train_loss'] and self.history['val_loss']:
        axes[0, 0].plot(epochs, self.history['train_loss'], label='Train Loss', color='blue')
        axes[0, 0].plot(epochs, self.history['val_loss'], label='Val Loss', color='orange')
        axes[0, 0].set_title('Loss Curve')
        axes[0, 0].set_xlabel('Epochs')
        axes[0, 0].set_ylabel('Loss')
        axes[0, 0].legend()
        axes[0, 0].grid()
    #2. mAP曲线
    if self.history['metrics']['mAP50'] and self.history['metrics']['mAP50-95']:
        axes[0, 1].plot(epochs, self.history['metrics']['mAP50'], label='mAP50', color='green')
        axes[0, 1].plot(epochs, self.history['metrics']['mAP50-95'], label='mAP50-95', color='red')
        axes[0, 1].set_title('mAP Curve')
        axes[0, 1].set_xlabel('Epochs')
        axes[0, 1].set_ylabel('mAP')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
    #3. 精确率曲线
    if self.history['metrics']['precision'] and self.history['metrics']['recall']:
        axes[0, 2].plot(epochs, self.history['metrics']['precision'], label='Precision', color='purple')
        axes[0, 2].plot(epochs, self.history['metrics']['recall'], label='Recall', color='brown')
        axes[0, 2].set_title('Precision & Recall Curve')
        axes[0, 2].set_xlabel('Epochs')
        axes[0, 2].set_ylabel('Value')
        axes[0, 2].legend()
        axes[0, 2].grid(True, alpha=0.3)
    #4. 学习率曲线
    if self.history['lr']:
        axes[1, 0].plot(epochs, self.history['lr'], label='Learning Rate', color='cyan')
        axes[1, 0].set_title('Learning Rate Curve')
        axes[1, 0].set_xlabel('Epochs')
        axes[1, 0].set_ylabel('Learning Rate')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].set_yscale('log')
    plt.tight_layout()

    #保存图像
    save_path = self.save_dir / 'training_curves.png'
    plt.savefig(save_path)
    plt.close()
    print(f'训练曲线已保存到: {save_path}')

def validate_best_model(self):
    """验证最佳模型"""
    print(f'\n验证最佳模型....')
    best_model_path = self.save_dir / 'best_model.pt'
    if best_model_path.exists():
        model = YOLO(str(best_model_path))
        metrics = model.val(data=self.data_yaml)
        print("最佳模型")
        if hasattr(metrics, 'box'):
            print(f"mAP@0.5: {metrics.box.map50:.4f}, mAP@0.5:0.95: {metrics.box.map50_95:.4f}, Precision: {metrics.box.precision:.4f}, Recall: {metrics.box.recall:.4f}")
        
        #保存验证结果
        val_results = {
            'mAP50': metrics.box.map50,
            'mAP50-95': metrics.box.map50_95,
            'precision': metrics.box.precision,
            'recall': metrics.box.recall,
        }
        with open(self.save_dir / 'best_model_val_results.json', 'w') as f:
            json.dump(val_results, f, indent=4)
    else:
        print("未找到最佳模型文件，跳过验证。")
def save_training_config(self):
    config = {
    'model': str(self.model),
    "data_yaml": str(self.data_yaml),
    'epochs': self.epochs,
    'batch_size': self.batch_size,
    'img_size': self.img_size,
    'device': self.device,
    'use_ema': self.user_ema,
    'optimizer': self.optimizer_type,
    'scheduler': self.scheduler_type,
    'save_dir': str(self.save_dir),
    'timestamp': datetime.now().isoformat(),

    }

    with open(self.save_dir / 'training_config.json', 'w') as f:
        json.dump(config, f, indent=4)

    print(f"√训练配置已保存:{self.save_dir/'training_config.json'}")

def train_model(
    model_type='yolov8',
    size='n',
    task='detect',
    data_yaml='datasets/ ... ',
    epochs=50,
    batch_size=16,
    img_size=640,
    device='cuda',
    project_name='runs/train',

):
    """
        单个模型训练的便捷函数
        Args:
        model_type:模型类型('yolov8','yoLov11')
        size:模型大小('n','s','m','L','x')
        task:任务类型('detect','segment')
        data_yaml:数据集配置文件
        epochs:训练轮数
        batch_size:批次大小
        img_size: 图像大小
        device:设备
        project_name: 项目名称

        Returns:
        训练结果
    """
    from core.model_factory import ModelFactory
    model = ModelFactory.create_model(model_type, size, task)

    #创建训练器
    trainer = Trainer(
        model=model,
        data_yaml=data_yaml,
        project_name=project_name,
        epochs=epochs,
        batch_size=batch_size,
        device=device,
        user_ema=True,
        optimizer_type='Auto',
        scheduler_type='cosine',
    )
    #开始训练
    results = trainer.train()
    return results, trainer.save_dir
