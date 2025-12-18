import torch
import torch.nn as nn

class AlexNet(nn.Module):
    def __init__(self, input_shape=(3, 224, 224), num_classes=2):
        super(AlexNet, self).__init__()

        # --- 特征提取层 (Features) ---
        self.features = nn.Sequential(
            # Layer 1
            nn.Conv2d(input_shape[0], 48, kernel_size=11, stride=4, padding=0),
            nn.BatchNorm2d(48),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),

            # Layer 2
            nn.Conv2d(48, 128, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),

            # Layer 3
            nn.Conv2d(128, 192, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),

            # Layer 4
            nn.Conv2d(192, 192, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),

            # Layer 5
            nn.Conv2d(192, 128, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
        )

        # 动态计算 Flatten 后的特征维度
        self.feature_size = self._get_feature_size(input_shape)

        # --- 分类器层 (Classifier) ---
        self.classifier = nn.Sequential(
            nn.Flatten(),
            # FC 1
            nn.Linear(self.feature_size, 1024),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.5),
            
            # FC 2
            nn.Linear(1024, 1024),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.5),
            
            # Output Layer (注意：这里不需要激活函数)
            nn.Linear(1024, num_classes) 
        )

    def _get_feature_size(self, input_shape):
        """辅助函数：自动计算卷积层输出的尺寸"""
        with torch.no_grad():
            x = torch.zeros(1, *input_shape)
            x = self.features(x)
            return x.view(1, -1).size(1)

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        # 【重要】训练时移除 Softmax，直接返回 logits
        # 如果是在预测/推理阶段(inference)，可以在外部手动调用 torch.softmax(x, dim=1)
        return x

# 使用 if __name__ == "__main__": 保护测试代码
# 这样当其他文件 import AlexNet 时，不会自动执行下面的 print
if __name__ == "__main__":
    # 测试代码
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = AlexNet(num_classes=2).to(device)
    
    print(model)

    # 模拟输入：Batch_size=1, Channel=3, Height=224, Width=224
    input_tensor = torch.randn(1, 3, 224, 224).to(device)
    
    output = model(input_tensor)
    print("\n输入尺寸:", input_tensor.shape)
    print("输出尺寸:", output.shape) # 应该是 [1, 2]
    print("输出数值 (Logits):", output)