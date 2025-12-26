"""
模型工厂模块
多支持 YOLO8、YOLO11 模型创建和配置
"""

from ultralytics import YOLO
import torch
import numpy as np
import torch.nn as nn
from pathlib import Path

class ModelEMA:
    """
    Model Exponential Moving Average (EMA)
    指数移动平均，用于模型的参数的平滑更新
    """

    def __init__(self, model, decay=0.9999, tau=2000, updates=0):
        """
        Args:
            model: 要跟踪的模型
            decay: EMA衰减率
            tau: EMA衰减变调增参数
            updates: 更新次数
        """
        self.ema = self._deepcopy_model(model)
        self.updates = updates
        # self.decay = lambda x:...  # 定义一个匿名函数，self.decay 作为EMA类的成员方法，
        #                            输入参数一般是当前训练的步数/轮次，输出是当前步对应的EMA衰减系数
        # decay * (1 - np.exp(-x / tau)) # 其中衰减系数上限值 (如0.999)，训练后期衰减
        #                                # x: 当训练的步数/轮次，随机项目的推进，x逐渐增大
        # tau = 时间常数，控制衰减系数上升的概率，是调整曲线陡峭程度的超参数
        #       tau越小 -> 衰减系数上升越快，能更快姐姐与decay上限
        #       tau越大 -> 衰减系数上升越慢，前期保持较低值的时间更长
        # np.exp(-x / tau): 指数衰减项，当x = 0 时，该项值为1，整体衰减系数为0；当x趋近于无穷大时，该项趋近于0，整体衰减系数趋近于decay
        self.decay = lambda x: decay * (1 - np.exp(-x / tau))

        # 遍历EMA模型的所有参数
        for p in self.ema.parameters():
            # 禁用EMA模型参数的梯度计算
            # 因为EMA是影子参数，仅通过原模型参数加权平均更新，无需反向传播优化
            p.requires_grad_(False)

    def _deepcopy_model(self, model):
        """深拷贝模型"""
        import copy
        ema_model = copy.deepcopy(model.model if hasattr(model, 'model') else model)
        ema_model.eval()
        return ema_model

    def update(self, model):
        """更新EMA参数"""
        self.updates += 1
        d = self.decay(self.updates)

        msd = model.state_dict()
        for k, v in self.ema.state_dict().items():
            if v.dtype.is_floating_point:
                v *= d
                v += (1 - d) * msd[k].detach()

class ModelFactory:
    """模型工厂类"""

    # 支持的模型和权重
    MODELS = {
        'yolov8': {
            'n': 'yolov8n.pt',
            's': 'yolov8s.pt',
            'm': 'yolov8m.pt',
            'l': 'yolov8l.pt',
            'x': 'yolov8x.pt',
        },
        'yolov8-seg': {
            'n': 'yolov8n-seg.pt',
            's': 'yolov8s-seg.pt',
            'm': 'yolov8m-seg.pt',
            'l': 'yolov8l-seg.pt',
            'x': 'yolov8x-seg.pt',
        },
        'yolov11': {
            'n': 'yolo11n.pt',
            's': 'yolo11s.pt',
            'm': 'yolo11m.pt',
            'l': 'yolo11l.pt',
            'x': 'yolo11x.pt',
        },
        'yolov11-seg': {
            'n': 'yolo11n-seg.pt',
            's': 'yolo11s-seg.pt',
            'm': 'yolo11m-seg.pt',
            'l': 'yolo11l-seg.pt',
            'x': 'yolo11x-seg.pt',
        },
    }

    @classmethod
    def create_model(cls, model_type='yolov8', size='n', task='detect', num_classes=1):
        """
        通过工厂加载预训练模型 (不加载具体的权重)

        Args:
            model_type: 模型类型 ('yolov8', 'yolov11')
            size: 模型大小 ('n', 's', 'm', 'l', 'x')
            task: 任务类型 ('detect', 'segment')
            num_classes: 类别数量

        Returns:
             model: YOLO模型实例
        """
        # 构建模型键
        if task == 'segment':
            model_key = f"{model_type}-seg"
        else:
            model_key = model_type
        
        if model_key not in cls.MODELS:
            raise ValueError(f"不支持的模型类型: {model_key}")
        
        if size not in cls.MODELS[model_key]:
            raise ValueError(f"不支持的模型大小: {size}")

        # 获取预训练权重路径
        pretrained_path = cls.MODELS[model_key][size]

        print(f"V 创建模型: {model_key}({size})")
        print(f"  预训练权重: {pretrained_path}")
        print(f"  类别数量: {num_classes}")

        # 加载模型
        model = YOLO(pretrained_path)

        return model

    def get_model_info(cls, model_type, size):
        """获取模型信息"""
        # 这里使用预定义的字典 (仅做演示)
        info = {
            'yolov8n': {'params': '3.2M', 'flops': '8.7G', 'speed': '+++++'},
            'yolov8s': {'params': '11.2M', 'flops': '28.6G', 'speed': '++++'},
            'yolov8m': {'params': '25.9M', 'flops': '78.9G', 'speed': '+++'},
            'yolov8l': {'params': '43.7M', 'flops': '165.2G', 'speed': '++'},
            'yolov8x': {'params': '68.2M', 'flops': '258.5G', 'speed': '+'},
            # ... 其他模型的参数 ...
             'yolo11n': {'params': '2.6M', 'flops': '6.5G', 'speed': '+++++'},
             'yolo11s': {'params': '9.4M', 'flops': '21.5G', 'speed': '++++'},
             'yolo11m': {'params': '20.1M', 'flops': '68.0G', 'speed': '+++'},
             'yolo11l': {'params': '25.3M', 'flops': '86.9G', 'speed': '++'},
             'yolo11x': {'params': '56.9M', 'flops': '194.9G', 'speed': '+'},
        }
        
        key = f"{model_type}{size}"
        return info.get(key, {'params': 'N/A', 'flops': 'N/A', 'speed': 'N/A'})

    @classmethod
    def list_available_models(cls):
        """列出所有可用模型"""
        print(f"-" * 30)
        print(" 可用模型列表:")
        print(f"-" * 30)

        for model_type, sizes in cls.MODELS.items():
            print(f"[{model_type.upper()}]")
            for size, path in sizes.items():
                info = cls.get_model_info(model_type.replace('-seg', ''), size)
                print(f"  - {size.upper()}: {path}")
                print(f"      参数量: {info['params']}, Flops: {info['flops']}, 速度: {info['speed']}")


def create_optimizer(model, optimizer_type='AdamW', lr=0.01, weight_decay=0.0005, momentum=0.937):
    """
    创建优化器

    Args:
        model: 模型
        optimizer_type: 优化器类型 ('SGD', 'Adam', 'AdamW', 'Auto')
        lr: 学习率
        weight_decay: 权重衰减
        momentum: 动量 (仅SGD)
    
    Returns:
        优化器实例
    """
    import numpy as nn
    
    # 参数分组 (不同层使用不同的学习率和权重衰减)
    # 优化器分组配置，将模型参数按类型拆分，实现差异化训练策略
    # 核心目的: 不同层 (如卷积层、归一化层) 对学习率和权重衰减的敏感度不同，分组可提升训练稳定性和效果
    g = [], [], []  # optimizer parameter groups 初始化三个空列表，分别存储不同类型的参数组
    # 筛选PyTorch中所有的归一化层 (BatchNorm, LayerNorm等) 的类对象
    # 原理: nn模块中所有含"Norm"关键字的类均为归一化层，这些层的参数更新策略需特殊处理 (如禁用权重衰减)
    bn = tuple(v for k, v in nn.__dict__.items() if 'Norm' in k) # 归一化层

    # 判断模型是否存在"model"属性 (常见于YOLO等封装好的模型，核心网络结构存在model属性中)
    if hasattr(model, 'model'):
        # 若存在，提取其中的核心网络结构 (避免直接操作外层封装，确保准确遍历内部参数)
        model_param = model.model
    else:
        # 如果非封装式模型 (核心网络结构直接挂载在model上)
        model_param = model

    # 遍历模型中所有模块 (modules) 递归获取所有子模块，包括嵌套层级
    for v in model_param.modules():
        # 遍历当前模块的参数，recurse=False表示不递归遍历子模块的参数 (避免重复收集)
        # p_name 参数名称
        for p_name, p in v.named_parameters(recurse=0):
            # 偏置参数: 通常不施加权重衰减 (减少过拟合风险，且参数量少)
            if p_name == 'bias':
                g[2].append(p)  # 归入第2组: 偏置参数组 (后续配置无权重衰减)
            # 归一化层的权重参数: 特殊处理 (无权重衰减)
            # 原因: 归一化层的权重用于缩放特征分布，权重衰减会破坏标准化的效果
            elif p_name == 'weight' and isinstance(v, bn):
                g[1].append(p)  # 归入第1组: 归一化层权重组 (后续配置无权重衰减)
            else: # 普通权重参数 (如卷积层、全连接层权重): 施加权重衰减 (核心防过拟合手段)
                g[0].append(p)  # 归入第0组，普通权重组 (后续配置有权重衰减)

    # 选择优化器
    if optimizer_type == 'Auto':    # 自动选择策略
        # 自动选择，小模型用AdamW，大模型用SGD
        param_count = sum(p.numel() for p in model_param.parameters())
        optimizer_type = 'AdamW' if param_count < 10e6 else 'SGD'

    if optimizer_type == 'SGD':    # 选择SGD随机梯度下降
        optimizer = torch.optim.SGD(g[2], lr=lr, momentum=momentum, nesterov=True)
    elif optimizer_type == 'Adam': # 选择Adam自适应动量估计，平衡收敛速度和稳定性，适合中等模型
        # g[2]                     # 待优化参数组
        # lr=lr                    # 学习率
        # betas=(momentum, 0.999)  # 一阶矩 (动量) 和二阶矩的指数衰减率，默认 (0.9, 0.999)
        optimizer = torch.optim.Adam(g[2], lr=lr, betas=(momentum, 0.999))
    elif optimizer_type == 'AdamW': # 选择 AdamW(Adam+权重衰减改进): 解决Adam权重衰减消失问题，适合快速收敛
        # g[2]                     # 待优化参数组
        # lr=lr                    # 学习率
        # bests=(momentum, 0.999)  # 一阶矩和二阶矩的衰减率
        # weight_decay=0.0         # 权重衰减的系数 (此处暂设为0，后续可按分组配置: g[0]设为非0, g[1]/g[2]设为0)
        optimizer = torch.optim.AdamW(g[2], lr=lr, betas=(momentum, 0.999), weight_decay=0.0)
    else:
        raise ValueError(f"不支持的优化器类型: {optimizer_type}")

    # 添加参数组
    optimizer.add_param_group({'params': g[0], 'weight_decay': weight_decay})  # 带权重衰减系数
    optimizer.add_param_group({'params': g[1], 'weight_decay': 0.0})           # 不带权重衰减系数

    print(f"V 优化器: {optimizer_type}")
    print(f"  学习率: {lr}")
    print(f"  权重衰减: {weight_decay}")
    print(f"  参数组: {len(g[0])} (with decay), {len(g[1])} (no decay), {len(g[2])} (bias)")

    return optimizer

def create_scheduler(optimizer, scheduler_type="cosine", epoches=100, wamup_epochs=3):
    """
    创建学习率调度器 (余弦退火)

    Args:
        optimizer: 优化器
        scheduler_type: 调度器类型
        epoches: 总训练轮数
        wamup_epochs: 预热轮数

    Retures:
        调度器实例
    """
    if scheduler_type == 'cosine':
        # 余弦退火调度器
        from torch.optim.lr_scheduler import CosineAnnealingLR, LinearLR, SequentialLR

        # 预热阶段
        warmup_scheduler = LinearLR(
            optimizer,
            start_factor=0.1,    # 预热起始学习率因子: 默认学习率 x 0.1
            end_factor=1.0,      # 预热结束学习率因子: 结束时学习率 = 优化器默认学习率 x 1.0 (恢复正常初始学习率)
            total_iters=wamup_epochs # 预热总轮数: 学习率在warmup_epochs轮内完成线性增长
        )

        # 余弦退火阶段
        # 作用: 预热结束后，学习率按余弦函数周期衰减，平衡探索 (高学习率) 和 exploitation (低学习率)
        cosine_scheduler = CosineAnnealingLR(
            optimizer,              # 关联的优化器
            T_max=epoches - wamup_epochs, # 退火周期: 学习率从峰值衰减到最小值的总轮数 (总训练轮数 - 预热轮数)
            eta_min=optimizer.param_groups[0]['lr'] * 0.01 # 最小学习率: 衰减的下限 (为初始学习率的1%，避免学习率过低导致梯度消失)
        )

        # 组合调度器
        # 顺序执行多个调度器 (SequentialLR)
        # 作用: 按顺序执行预热调度器和余弦退火调度器，在指定轮数切换
        scheduler = SequentialLR(
            optimizer=optimizer,        # 关联的优化器
            schedulers=[warmup_scheduler, cosine_scheduler], # 调度器执行顺序: 先执行预热，再执行余弦退火
            milestones=[wamup_epochs]   # 调度器切换里程碑: 第warnum_epochs轮结束后，从预热调度器切换到余弦退火调度器
        )

        print(f"V 学习率调度器: 余弦退火 (Cosine Annealing)")
        print(f"  预热轮数: {wamup_epochs}")
        print(f"  总轮数: {epoches}")

    elif scheduler_type == 'linear':
        from torch.optim.lr_scheduler import LinearLR
        scheduler = LinearLR(optimizer, start_factor=1.0, end_factor=0.01, total_iters=epoches)
        print("V 学习器调度器: 线性衰减")

    elif scheduler_type == 'step':
        from torch.optim.lr_scheduler import StepLR
        scheduler = StepLR(optimizer, step_size=epoches // 3, gamma=0.1)
        print(f"V 学习率调度器: 梯度衰减")

    else:
        raise ValueError(f"不支持的调度器类型: {scheduler_type}")

    return scheduler

if __name__ == "__main__":
    # 测试模拟工厂
    ModelFactory.list_available_models()