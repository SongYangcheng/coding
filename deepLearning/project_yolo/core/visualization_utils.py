"""
可视化工具模块
生成训练曲线、混淆矩阵等可视化图表
支持曲线平滑处理
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
import json
from scipy.ndimage import gaussian_filter1d
from scipy.signal import savgol_filter


# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def smooth_curve(data, method='gaussian', sigma=2, window=5):
    """
    平滑曲线
    
    Args:
        data: 原始数据
        method: 平滑方法 ('gaussian', 'savgol', 'moving_avg')
        sigma: 高斯平滑的标准差
        window: 窗口大小
    
    Returns:
        平滑后的数据
    """
    if len(data) < 3:
        return data
    
    if method == 'gaussian':
        # 高斯平滑（最平滑）
        return gaussian_filter1d(data, sigma=sigma)
    elif method == 'savgol':
        # Savitzky-Golay滤波（保持峰值）
        window = min(window, len(data) - 1)
        if window % 2 == 0:
            window += 1
        if window < 3:
            return data
        return savgol_filter(data, window, 2)
    elif method == 'moving_avg':
        # 移动平均
        return pd.Series(data).rolling(window=window, center=True).mean().fillna(method='bfill').fillna(method='ffill').values
    else:
        return data


class TrainingVisualizer:
    """训练可视化器"""
    
    def __init__(self, results_dir, smooth=True, smooth_method='gaussian', smooth_sigma=2):
        """
        初始化可视化器
        
        Args:
            results_dir: 训练结果目录
            smooth: 是否平滑曲线
            smooth_method: 平滑方法 ('gaussian', 'savgol', 'moving_avg')
            smooth_sigma: 平滑参数
        """
        self.results_dir = Path(results_dir)
        self.results_csv = self.results_dir / 'results.csv'
        self.smooth = smooth
        self.smooth_method = smooth_method
        self.smooth_sigma = smooth_sigma
        
        if not self.results_csv.exists():
            raise FileNotFoundError(f"结果文件不存在: {self.results_csv}")
        
        # 读取结果
        self.df = pd.read_csv(self.results_csv)
        self.df.columns = self.df.columns.str.strip()
    
    def _smooth_data(self, data):
        """平滑数据"""
        if self.smooth and len(data) > 3:
            return smooth_curve(data, method=self.smooth_method, sigma=self.smooth_sigma)
        return data
    
    def plot_loss_curves(self, save_path=None):
        """绘制损失曲线"""
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        fig.suptitle('训练损失曲线', fontsize=16, fontweight='bold')
        
        # Box Loss
        if 'train/box_loss' in self.df.columns:
            axes[0].plot(self.df['epoch'], self.df['train/box_loss'], 
                        label='Train', linewidth=2, color='#FF6B6B')
            if 'val/box_loss' in self.df.columns:
                axes[0].plot(self.df['epoch'], self.df['val/box_loss'], 
                            label='Val', linewidth=2, color='#4ECDC4')
            axes[0].set_xlabel('Epoch', fontsize=12)
            axes[0].set_ylabel('Box Loss', fontsize=12)
            axes[0].set_title('边界框损失', fontsize=14)
            axes[0].legend(fontsize=10)
            axes[0].grid(True, alpha=0.3)
        
        # Class Loss
        if 'train/cls_loss' in self.df.columns:
            axes[1].plot(self.df['epoch'], self.df['train/cls_loss'], 
                        label='Train', linewidth=2, color='#FF6B6B')
            if 'val/cls_loss' in self.df.columns:
                axes[1].plot(self.df['epoch'], self.df['val/cls_loss'], 
                            label='Val', linewidth=2, color='#4ECDC4')
            axes[1].set_xlabel('Epoch', fontsize=12)
            axes[1].set_ylabel('Class Loss', fontsize=12)
            axes[1].set_title('分类损失', fontsize=14)
            axes[1].legend(fontsize=10)
            axes[1].grid(True, alpha=0.3)
        
        # DFL Loss
        if 'train/dfl_loss' in self.df.columns:
            axes[2].plot(self.df['epoch'], self.df['train/dfl_loss'], 
                        label='Train', linewidth=2, color='#FF6B6B')
            if 'val/dfl_loss' in self.df.columns:
                axes[2].plot(self.df['epoch'], self.df['val/dfl_loss'], 
                            label='Val', linewidth=2, color='#4ECDC4')
            axes[2].set_xlabel('Epoch', fontsize=12)
            axes[2].set_ylabel('DFL Loss', fontsize=12)
            axes[2].set_title('分布焦点损失', fontsize=14)
            axes[2].legend(fontsize=10)
            axes[2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path is None:
            save_path = self.results_dir / 'loss_curves.png'
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ 损失曲线已保存: {save_path}")
        
        return fig
    
    def plot_accuracy_curves(self, save_path=None):
        """绘制准确率曲线"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('训练准确率曲线', fontsize=16, fontweight='bold')
        
        # Precision
        if 'metrics/precision(B)' in self.df.columns:
            axes[0, 0].plot(self.df['epoch'], self.df['metrics/precision(B)'], 
                           linewidth=2, color='#95E1D3')
            axes[0, 0].set_xlabel('Epoch', fontsize=12)
            axes[0, 0].set_ylabel('Precision', fontsize=12)
            axes[0, 0].set_title('精确率', fontsize=14)
            axes[0, 0].grid(True, alpha=0.3)
            axes[0, 0].set_ylim([0, 1])
        
        # Recall
        if 'metrics/recall(B)' in self.df.columns:
            axes[0, 1].plot(self.df['epoch'], self.df['metrics/recall(B)'], 
                           linewidth=2, color='#F38181')
            axes[0, 1].set_xlabel('Epoch', fontsize=12)
            axes[0, 1].set_ylabel('Recall', fontsize=12)
            axes[0, 1].set_title('召回率', fontsize=14)
            axes[0, 1].grid(True, alpha=0.3)
            axes[0, 1].set_ylim([0, 1])
        
        # mAP@0.5
        if 'metrics/mAP50(B)' in self.df.columns:
            axes[1, 0].plot(self.df['epoch'], self.df['metrics/mAP50(B)'], 
                           linewidth=2, color='#AA96DA')
            axes[1, 0].set_xlabel('Epoch', fontsize=12)
            axes[1, 0].set_ylabel('mAP@0.5', fontsize=12)
            axes[1, 0].set_title('平均精度 @0.5', fontsize=14)
            axes[1, 0].grid(True, alpha=0.3)
            axes[1, 0].set_ylim([0, 1])
        
        # mAP@0.5:0.95
        if 'metrics/mAP50-95(B)' in self.df.columns:
            axes[1, 1].plot(self.df['epoch'], self.df['metrics/mAP50-95(B)'], 
                           linewidth=2, color='#FCBAD3')
            axes[1, 1].set_xlabel('Epoch', fontsize=12)
            axes[1, 1].set_ylabel('mAP@0.5:0.95', fontsize=12)
            axes[1, 1].set_title('平均精度 @0.5:0.95', fontsize=14)
            axes[1, 1].grid(True, alpha=0.3)
            axes[1, 1].set_ylim([0, 1])
        
        plt.tight_layout()
        
        if save_path is None:
            save_path = self.results_dir / 'accuracy_curves.png'
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ 准确率曲线已保存: {save_path}")
        
        return fig
    
    def plot_combined_curves(self, save_path=None):
        """绘制综合训练曲线（Loss + Accuracy）"""
        fig = plt.figure(figsize=(20, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        fig.suptitle('YOLO 训练曲线 - 完整视图', fontsize=18, fontweight='bold')
        
        # 第一行：损失曲线
        ax1 = fig.add_subplot(gs[0, 0])
        if 'train/box_loss' in self.df.columns:
            ax1.plot(self.df['epoch'], self.df['train/box_loss'], 
                    label='Train', linewidth=2, color='#FF6B6B')
            if 'val/box_loss' in self.df.columns:
                ax1.plot(self.df['epoch'], self.df['val/box_loss'], 
                        label='Val', linewidth=2, color='#4ECDC4')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Box Loss')
        ax1.set_title('边界框损失')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        ax2 = fig.add_subplot(gs[0, 1])
        if 'train/cls_loss' in self.df.columns:
            ax2.plot(self.df['epoch'], self.df['train/cls_loss'], 
                    label='Train', linewidth=2, color='#FF6B6B')
            if 'val/cls_loss' in self.df.columns:
                ax2.plot(self.df['epoch'], self.df['val/cls_loss'], 
                        label='Val', linewidth=2, color='#4ECDC4')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Class Loss')
        ax2.set_title('分类损失')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        ax3 = fig.add_subplot(gs[0, 2])
        if 'train/dfl_loss' in self.df.columns:
            ax3.plot(self.df['epoch'], self.df['train/dfl_loss'], 
                    label='Train', linewidth=2, color='#FF6B6B')
            if 'val/dfl_loss' in self.df.columns:
                ax3.plot(self.df['epoch'], self.df['val/dfl_loss'], 
                        label='Val', linewidth=2, color='#4ECDC4')
        ax3.set_xlabel('Epoch')
        ax3.set_ylabel('DFL Loss')
        ax3.set_title('分布焦点损失')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 第二行：准确率指标
        ax4 = fig.add_subplot(gs[1, 0])
        if 'metrics/precision(B)' in self.df.columns:
            ax4.plot(self.df['epoch'], self.df['metrics/precision(B)'], 
                    linewidth=2, color='#95E1D3')
        ax4.set_xlabel('Epoch')
        ax4.set_ylabel('Precision')
        ax4.set_title('精确率')
        ax4.grid(True, alpha=0.3)
        ax4.set_ylim([0, 1])
        
        ax5 = fig.add_subplot(gs[1, 1])
        if 'metrics/recall(B)' in self.df.columns:
            ax5.plot(self.df['epoch'], self.df['metrics/recall(B)'], 
                    linewidth=2, color='#F38181')
        ax5.set_xlabel('Epoch')
        ax5.set_ylabel('Recall')
        ax5.set_title('召回率')
        ax5.grid(True, alpha=0.3)
        ax5.set_ylim([0, 1])
        
        ax6 = fig.add_subplot(gs[1, 2])
        if 'metrics/mAP50(B)' in self.df.columns and 'metrics/mAP50-95(B)' in self.df.columns:
            ax6.plot(self.df['epoch'], self.df['metrics/mAP50(B)'], 
                    label='mAP@0.5', linewidth=2, color='#AA96DA')
            ax6.plot(self.df['epoch'], self.df['metrics/mAP50-95(B)'], 
                    label='mAP@0.5:0.95', linewidth=2, color='#FCBAD3')
        ax6.set_xlabel('Epoch')
        ax6.set_ylabel('mAP')
        ax6.set_title('平均精度')
        ax6.legend()
        ax6.grid(True, alpha=0.3)
        ax6.set_ylim([0, 1])
        
        # 第三行：学习率和综合指标
        ax7 = fig.add_subplot(gs[2, :])
        if 'lr/pg0' in self.df.columns:
            ax7_lr = ax7.twinx()
            ax7_lr.plot(self.df['epoch'], self.df['lr/pg0'], 
                       label='Learning Rate', linewidth=2, 
                       color='#FFA07A', linestyle='--')
            ax7_lr.set_ylabel('Learning Rate', color='#FFA07A')
            ax7_lr.tick_params(axis='y', labelcolor='#FFA07A')
            ax7_lr.legend(loc='upper right')
        
        if 'metrics/mAP50-95(B)' in self.df.columns:
            ax7.plot(self.df['epoch'], self.df['metrics/mAP50-95(B)'], 
                    label='mAP@0.5:0.95', linewidth=3, color='#4169E1')
        ax7.set_xlabel('Epoch', fontsize=12)
        ax7.set_ylabel('mAP@0.5:0.95', fontsize=12)
        ax7.set_title('学习率调度与模型性能', fontsize=14)
        ax7.legend(loc='upper left')
        ax7.grid(True, alpha=0.3)
        
        if save_path is None:
            save_path = self.results_dir / 'training_curves_complete.png'
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ 综合训练曲线已保存: {save_path}")
        
        return fig
    
    def print_final_metrics(self):
        """打印最终指标"""
        print("\n" + "=" * 60)
        print("最终训练指标")
        print("=" * 60)
        
        last_row = self.df.iloc[-1]
        
        metrics = {
            'Precision': 'metrics/precision(B)',
            'Recall': 'metrics/recall(B)',
            'mAP@0.5': 'metrics/mAP50(B)',
            'mAP@0.5:0.95': 'metrics/mAP50-95(B)',
            'Box Loss (Val)': 'val/box_loss',
            'Class Loss (Val)': 'val/cls_loss',
            'DFL Loss (Val)': 'val/dfl_loss'
        }
        
        for name, col in metrics.items():
            if col in self.df.columns:
                value = last_row[col]
                print(f"  {name:20s}: {value:.4f}")
        
        print("=" * 60)
    
    def generate_all_plots(self):
        """生成所有可视化图表"""
        print("\n生成训练可视化图表...")
        
        self.plot_loss_curves()
        self.plot_accuracy_curves()
        self.plot_combined_curves()
        self.print_final_metrics()
        
        print("\n✓ 所有可视化图表生成完成")


if __name__ == "__main__":
    print("可视化工具测试")
    print("=" * 60)
    print("使用方法:")
    print("  visualizer = TrainingVisualizer('runs/helmet_detection/train')")
    print("  visualizer.generate_all_plots()")
    print("=" * 60)
