#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
YOLO 统一训练脚本

整合所有训练功能：
- 支持多种模型 (YOLOv8/YOLO11, n/s/m/l/x)
- 支持多种任务 (detection/segmentation)
- 支持多种模式 (quick/standard/advanced)
- 自动检测 CUDA
- 完整的训练配置
- 可视化输出
"""

import argparse
import sys
import torch
from pathlib import Path
from ultralytics import YOLO
import yaml


def check_cuda():
    """检查 CUDA 可用性"""
    print("=" * 70)
    print("系统检查")
    print("=" * 70)
    
    cuda_available = torch.cuda.is_available()
    print(f"CUDA 可用: {cuda_available}")
    
    if cuda_available:
        print(f"CUDA 版本: {torch.version.cuda}")
        print(f"GPU 数量: {torch.cuda.device_count()}")
        print(f"GPU 名称: {torch.cuda.get_device_name(0)}")
        print(f"GPU 内存: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
        return True
    else:
        print("⚠️ CUDA 不可用，将使用 CPU 训练（速度较慢）")
        return False


def merge_all_datasets(data_dir='data'):
    """合并所有数据集到 data/merged_all"""
    import shutil
    
    merged_path = Path(data_dir) / 'merged_all'
    train_img = merged_path / 'images' / 'train'
    train_lbl = merged_path / 'labels' / 'train'
    val_img = merged_path / 'images' / 'val'
    val_lbl = merged_path / 'labels' / 'val'
    
    # 创建目录
    for p in [train_img, train_lbl, val_img, val_lbl]:
        p.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "=" * 70)
    print("合并所有数据集")
    print("=" * 70)
    
    total_train = 0
    total_val = 0
    
    # 1. 复制 data/8 (主数据集)
    print("\n1. 复制 data/8 数据集...")
    for img in Path(data_dir, '8/train/images').glob('*.jpg'):
        shutil.copy2(img, train_img / f"d8_{img.name}")
        lbl = Path(data_dir, '8/train/labels') / f"{img.stem}.txt"
        if lbl.exists():
            shutil.copy2(lbl, train_lbl / f"d8_{img.stem}.txt")
        total_train += 1
    
    for img in Path(data_dir, '8/valid/images').glob('*.jpg'):
        shutil.copy2(img, val_img / f"d8_{img.name}")
        lbl = Path(data_dir, '8/valid/labels') / f"{img.stem}.txt"
        if lbl.exists():
            shutil.copy2(lbl, val_lbl / f"d8_{img.stem}.txt")
        total_val += 1
    print(f"   ✓ data/8: {total_train} 训练, {total_val} 验证")
    
    # 2. 复制 data/11 (额外数据)
    print("\n2. 复制 data/11 数据集...")
    count_11 = 0
    for img in Path(data_dir, '11/train/images').glob('*.jpg'):
        shutil.copy2(img, train_img / f"d11_{img.name}")
        lbl = Path(data_dir, '11/train/labels') / f"{img.stem}.txt"
        if lbl.exists():
            shutil.copy2(lbl, train_lbl / f"d11_{img.stem}.txt")
        count_11 += 1
        total_train += 1
    print(f"   ✓ data/11: {count_11} 训练图像")
    
    # 3. 复制 data/raw/yolotxt
    print("\n3. 复制 data/raw/yolotxt 数据集...")
    count_raw = 0
    if Path(data_dir, 'raw/yolotxt/images').exists():
        for img in Path(data_dir, 'raw/yolotxt/images').glob('*.jpg'):
            shutil.copy2(img, train_img / f"raw_{img.name}")
            lbl = Path(data_dir, 'raw/yolotxt/annotations') / f"{img.stem}.txt"
            if lbl.exists():
                shutil.copy2(lbl, train_lbl / f"raw_{img.stem}.txt")
            count_raw += 1
            total_train += 1
    print(f"   ✓ data/raw/yolotxt: {count_raw} 训练图像")
    
    print(f"\n✓ 合并完成!")
    print(f"  总训练图像: {total_train}")
    print(f"  总验证图像: {total_val}")
    print(f"  总计: {total_train + total_val} 张图像")
    
    return True


def check_dataset(data_yaml, data_dir='data'):
    """检查数据集配置和标注质量"""
    data_path = Path(data_yaml)
    
    # 如果使用合并数据集，先执行合并
    if 'merged_all' in str(data_yaml):
        if not (Path(data_dir, 'merged_all/images/train').exists() and 
                len(list(Path(data_dir, 'merged_all/images/train').glob('*.jpg'))) > 100):
            print("\n检测到使用合并数据集，开始合并...")
            merge_all_datasets(data_dir)
    
    if not data_path.exists():
        print(f"\n❌ 数据集配置不存在: {data_yaml}")
        print("\n可用数据集:")
        print(f"  - {data_dir}/merged_all/data.yaml (合并所有数据 - 推荐)")
        print(f"  - {data_dir}/8/data.yaml (YOLOv8 - 7,035张)")
        print(f"  - {data_dir}/11/data.yaml (YOLO11 - 7,035张)")
        return False
    
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        print(f"\n✓ 数据集配置: {data_yaml}")
        print(f"  类别数: {config.get('nc', 'N/A')}")
        print(f"  类别名: {config.get('names', 'N/A')}")
        
        # 检查标注质量
        print("\n检查标注质量...")
        
        # 获取数据集根目录
        if f'{data_dir}/8' in str(data_yaml):
            dataset_path = Path(data_dir, '8')
            print(f"  使用 {data_dir}/8 数据集")
        elif f'{data_dir}/11' in str(data_yaml):
            dataset_path = Path(data_dir, '11')
            print(f"  使用 {data_dir}/11 数据集")
        else:
            dataset_path = Path(config.get('path', data_path.parent))
        
        train_labels = dataset_path / 'train' / 'labels'
        
        if train_labels.exists():
            sample_labels = list(train_labels.glob("*.txt"))[:20]
            if sample_labels:
                problem_count = 0
                total_checked = 0
                total_objects = 0
                
                for label_file in sample_labels:
                    try:
                        with open(label_file, 'r') as f:
                            lines = f.readlines()
                            if not lines:
                                continue
                            
                            file_objects = 0
                            for line in lines:
                                line = line.strip()
                                if line:
                                    parts = line.split()
                                    if len(parts) == 5:
                                        w, h = float(parts[3]), float(parts[4])
                                        total_checked += 1
                                        file_objects += 1
                                        if w > 0.9 and h > 0.9:
                                            problem_count += 1
                            
                            total_objects += file_objects
                    except:
                        continue
                
                if total_checked > 0:
                    problem_ratio = problem_count / total_checked
                    avg_objects = total_objects / len(sample_labels)
                    
                    print(f"  检查样本: {len(sample_labels)} 个文件")
                    print(f"  检查对象: {total_checked} 个")
                    print(f"  平均每图: {avg_objects:.1f} 个对象")
                    
                    if problem_ratio > 0.5:
                        print("\n⚠️  警告：数据集标注可能有问题")
                        print(f"  建议使用 {data_dir}/8/data.yaml 或 {data_dir}/11/data.yaml")
                    else:
                        print("  ✓ 标注质量检查通过")
                        if avg_objects > 1.5:
                            print(f"  ✓ 支持多目标检测（平均{avg_objects:.1f}个/图）")
        
        # 提示可用的额外数据
        raw_default = Path(data_dir, "raw/default/images")
        if raw_default.exists():
            raw_count = len(list(raw_default.glob("*.jpg")))
            if raw_count > 0:
                print(f"\n💡 提示: {data_dir}/raw/default/ 有额外 {raw_count} 张图像可用")
                print("   (VOC格式，需要转换后才能使用)")
        
        return True
    except Exception as e:
        print(f"\n❌ 读取配置失败: {e}")
        return False


def get_training_config(mode='standard'):
    """
    获取训练配置（优化版：提高小目标检测精度）
    
    Args:
        mode: 训练模式 (quick/standard/advanced)
    
    Returns:
        dict: 训练配置字典
    """
    base_config = {
        # 优化器
        'optimizer': 'AdamW',
        'lr0': 0.01,
        'lrf': 0.01,
        'momentum': 0.937,
        'weight_decay': 0.0005,
        
        # 学习率调度
        'cos_lr': True,
        'warmup_epochs': 5,      # 增加预热轮数，平滑启动
        'warmup_momentum': 0.8,
        'warmup_bias_lr': 0.1,
        
        # 训练设置
        'save': True,
        'amp': True,
        'plots': True,
        'verbose': True,
        
        # 数据增强（优化以提高精度）
        'hsv_h': 0.015,
        'hsv_s': 0.7,
        'hsv_v': 0.4,
        'degrees': 5.0,      # 增加旋转，提高鲁棒性
        'translate': 0.1,
        'scale': 0.5,
        'shear': 2.0,        # 增加剪切变换
        'perspective': 0.0,
        'flipud': 0.0,
        'fliplr': 0.5,
        'mosaic': 1.0,
        'mixup': 0.1,        # 添加mixup增强
        'copy_paste': 0.1,   # 添加copy-paste增强
        
        # 其他
        'pretrained': True,
        'seed': 42,
        'deterministic': False,
        'single_cls': False,  # 单类别检测
        'rect': False,
        'close_mosaic': 10,
        'resume': False,
        'val': True,
        'cache': False,
        
        # 优化小目标检测
        'box': 7.5,          # box loss权重
        'cls': 0.5,          # cls loss权重
        'dfl': 1.5,          # dfl loss权重
        
        # 平滑训练优化
        'dropout': 0.0,      # Dropout（可选，0表示不使用）
        'label_smoothing': 0.0,  # 标签平滑（0-0.1，减少过拟合）
    }
    
    if mode == 'quick':
        # 快速模式：减少轮数，简化增强
        base_config.update({
            'patience': 20,
            'save_period': 10,
            'mosaic': 0.5,
            'mixup': 0.0,
            'copy_paste': 0.0,
        })
    elif mode == 'advanced':
        # 高级模式：更强的数据增强和平滑训练
        base_config.update({
            'degrees': 10.0,
            'mixup': 0.15,
            'copy_paste': 0.15,
            'label_smoothing': 0.1,  # 标签平滑，减少过拟合
        })
    
    return base_config


def train_model(
    model_name='yolov8s',
    task='detect',
    data_yaml='data/8/data.yaml',
    epochs=50,
    batch=8,
    imgsz=640,
    device=None,
    mode='standard',
    project='runs/train',
    name='exp',
    data_dir='data'
):
    """
    训练模型（优化版：平滑训练曲线）
    
    Args:
        model_name: 模型名称 (yolov8n/s/m/l/x, yolo11n/s/m/l/x)
        task: 任务类型 (detect/segment)
        data_yaml: 数据集配置文件
        epochs: 训练轮数
        batch: 批次大小
        imgsz: 图像大小
        device: 设备 (None=自动, 0=GPU0, cpu=CPU)
        mode: 训练模式 (quick/standard/advanced)
        project: 项目目录
        name: 实验名称
        data_dir: 数据目录
    """
    print("\n" + "=" * 70)
    print("训练配置")
    print("=" * 70)
    print(f"模型: {model_name}")
    print(f"任务: {task}")
    print(f"数据集: {data_yaml}")
    print(f"数据目录: {data_dir}")
    print(f"轮数: {epochs}")
    print(f"批次: {batch}")
    print(f"图像大小: {imgsz}")
    print(f"模式: {mode}")
    
    # 自动选择设备
    if device is None:
        device = 0 if torch.cuda.is_available() else 'cpu'
    print(f"设备: {device}")
    
    # 构建模型文件名
    suffix = '-seg' if task == 'segment' else ''
    model_file = f"{model_name}{suffix}.pt"
    
    print(f"\n加载模型: {model_file}")
    model = YOLO(model_file)
    
    # 获取训练配置
    train_config = get_training_config(mode)
    
    # 开始训练
    print("\n" + "=" * 70)
    print("开始训练")
    print("=" * 70)
    
    # 预估时间
    time_per_epoch = 5 if 'n' in model_name else (8 if 's' in model_name else 15)
    estimated_time = epochs * time_per_epoch / 60
    print(f"预计训练时间: {estimated_time:.1f} 小时")
    print("按 Ctrl+C 可随时停止\n")
    
    try:
        # 配置 MLflow 以避免 Windows 路径问题
        import os
        mlflow_dir = Path(project) / 'mlflow'
        mlflow_dir.mkdir(parents=True, exist_ok=True)
        os.environ['MLFLOW_TRACKING_URI'] = f'file:///{mlflow_dir.absolute().as_posix()}'
        
        print(f"MLflow 跟踪目录: {mlflow_dir.absolute()}")
        
        results = model.train(
            data=data_yaml,
            epochs=epochs,
            batch=batch,
            imgsz=imgsz,
            device=device,
            workers=2,
            project=project,
            name=name,
            exist_ok=True,
            
            # 平滑训练优化
            patience=50,           # 增加早停耐心值，让训练更充分
            save_period=10,        # 更频繁保存，便于恢复
            
            **train_config
        )
        
        # 训练完成
        print("\n" + "=" * 70)
        print("✅ 训练完成!")
        print("=" * 70)
        
        results_dir = Path(model.trainer.save_dir)
        print(f"\n结果目录: {results_dir}")
        print(f"最佳模型: {results_dir / 'weights' / 'best.pt'}")
        print(f"最后模型: {results_dir / 'weights' / 'last.pt'}")
        
        # 验证模型
        print("\n" + "=" * 70)
        print("验证模型")
        print("=" * 70)
        
        metrics = model.val()
        
        print(f"\n最终性能:")
        print(f"  mAP@0.5: {metrics.box.map50:.4f}")
        print(f"  mAP@0.5:0.95: {metrics.box.map:.4f}")
        print(f"  Precision: {metrics.box.mp:.4f}")
        print(f"  Recall: {metrics.box.mr:.4f}")
        
        # 生成可视化
        try:
            from visualization_utils import TrainingVisualizer
            print("\n生成可视化图表...")
            visualizer = TrainingVisualizer(results_dir)
            visualizer.generate_all_plots()
            print("✓ 可视化完成")
        except Exception as e:
            print(f"⚠️ 可视化失败: {e}")
        
        return results_dir
        
    except KeyboardInterrupt:
        print("\n\n⚠️ 训练被用户中断")
        print("提示: 可以使用 resume=True 继续训练")
        return None
    except Exception as e:
        print(f"\n❌ 训练失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    parser = argparse.ArgumentParser(
        description='YOLO 统一训练脚本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 使用合并数据集训练（默认，推荐）
  python train.py
  
  # 快速训练
  python train.py --model yolov8n --epochs 30 --mode quick
  
  # 标准训练（推荐）
  python train.py --model yolov8s --epochs 50 --mode standard
  
  # 高级训练
  python train.py --model yolov8m --epochs 100 --mode advanced
  
  # 使用单个数据集
  python train.py --data data/8/data.yaml
  
数据集说明:
  - data/merged_all/data.yaml: 合并所有数据集（默认，约10,000+张）
  - data/8/data.yaml: YOLOv8格式，7,035张
  - data/11/data.yaml: YOLO11格式，7,035张
  - data/raw/yolotxt/: 额外519张
  
  建议: 使用merged_all获得最佳效果
        """
    )
    
    # 必需参数
    parser.add_argument('--data', type=str, default='data/merged_all/data.yaml',
                       help='数据集配置文件路径 (默认: data/merged_all/data.yaml - 合并所有数据集)')
    parser.add_argument('--data-dir', type=str, default='data',
                       help='数据目录路径 (默认: data)')
    
    # 模型参数
    parser.add_argument('--model', type=str, default='yolov8s',
                       choices=['yolov8n', 'yolov8s', 'yolov8m', 'yolov8l', 'yolov8x',
                               'yolo11n', 'yolo11s', 'yolo11m', 'yolo11l', 'yolo11x'],
                       help='模型大小')
    parser.add_argument('--task', type=str, default='detect',
                       choices=['detect', 'segment'],
                       help='任务类型')
    
    # 训练参数
    parser.add_argument('--epochs', type=int, default=50,
                       help='训练轮数')
    parser.add_argument('--batch', type=int, default=8,
                       help='批次大小')
    parser.add_argument('--imgsz', type=int, default=640,
                       help='图像大小')
    parser.add_argument('--device', type=str, default=None,
                       help='设备 (None=自动, 0=GPU0, cpu=CPU)')
    
    # 模式参数
    parser.add_argument('--mode', type=str, default='standard',
                       choices=['quick', 'standard', 'advanced'],
                       help='训练模式')
    
    # 输出参数
    parser.add_argument('--project', type=str, default='runs/train',
                       help='项目目录')
    parser.add_argument('--name', type=str, default='exp',
                       help='实验名称')
    
    args = parser.parse_args()
    
    # 系统检查
    check_cuda()
    
    # 检查数据集
    if not check_dataset(args.data, args.data_dir):
        sys.exit(1)
    
    # 开始训练
    result = train_model(
        model_name=args.model,
        task=args.task,
        data_yaml=args.data,
        epochs=args.epochs,
        batch=args.batch,
        imgsz=args.imgsz,
        device=args.device,
        mode=args.mode,
        project=args.project,
        name=args.name,
        data_dir=args.data_dir
    )
    
    if result:
        print("\n" + "=" * 70)
        print("🎉 训练流程完成!")
        print("=" * 70)
        print("\n下一步:")
        print("  1. 查看训练曲线")
        print("  2. 测试模型: python modern_gui_app.py")
        print(f"  3. 模型路径: {result}/weights/best.pt")


if __name__ == '__main__':
    main()
