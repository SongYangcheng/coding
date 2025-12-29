import os
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import numpy as np
import cv2
import matplotlib.pyplot as plt
from torchvision import transforms
from torch.optim import SGD
from torch.optim.lr_scheduler import CosineAnnealingWarmRestarts
import json
from model_AlexNet import AlexNet  # 假设model_AlexNet.py在同一目录

# --- 配置部分 ---
# 数据集根目录（根据用户路径调整）
DATA_ROOT = r'D:\Users\25711\下载\专业方向强化课程4-实验报告1\flower_photos花卉数据集\flower_photos'
# 类别列表（flower_photos的5个类别）
CLASSES = ['daisy', 'dandelion', 'roses', 'sunflowers', 'tulips']
NUM_CLASSES = len(CLASSES)

# 保存类别映射
class_dict = {str(i): cls for i, cls in enumerate(CLASSES)}
with open('classes.json', 'w') as f:
    json.dump(class_dict, f)

# 定义训练数据增强策略
train_transform = transforms.Compose([
    transforms.RandomResizedCrop(227),  # AlexNet输入227x227
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])  # 归一化到[-1,1]
])

# 定义验证集转换
val_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(227),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

class FlowerDataset(Dataset):
    def __init__(self, img_paths, labels, transform=None):
        self.img_paths = img_paths
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.img_paths)

    def __getitem__(self, idx):
        img_path = self.img_paths[idx]
        label = self.labels[idx]
        # 使用 PIL.Image.open 代替 cv2.imread，以更好地处理中文路径
        from PIL import Image
        img = Image.open(img_path).convert('RGB')
        if self.transform:
            img = self.transform(img)
        return img, label

def get_dataset_paths(root_dir):
    img_paths = []
    labels = []
    for i, cls in enumerate(CLASSES):
        cls_dir = os.path.join(root_dir, cls)
        if os.path.exists(cls_dir):
            for img_name in os.listdir(cls_dir):
                if img_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                    img_paths.append(os.path.join(cls_dir, img_name))
                    labels.append(i)
    return img_paths, labels

def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'Using device: {device}')

    # 获取数据集路径
    img_paths, labels = get_dataset_paths(DATA_ROOT)
    print(f'Total images: {len(img_paths)}')

    # 划分训练集和验证集 (9:1)
    np.random.seed(42)
    indices = np.random.permutation(len(img_paths))
    split = int(0.9 * len(img_paths))
    train_indices = indices[:split]
    val_indices = indices[split:]

    train_paths = [img_paths[i] for i in train_indices]
    train_labels = [labels[i] for i in train_indices]
    val_paths = [img_paths[i] for i in val_indices]
    val_labels = [labels[i] for i in val_indices]

    # 创建数据集
    train_dataset = FlowerDataset(train_paths, train_labels, transform=train_transform)
    val_dataset = FlowerDataset(val_paths, val_labels, transform=val_transform)

    batch_size = 32
    num_workers = 0  # Windows下设为0避免多进程问题

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers, pin_memory=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers, pin_memory=True)

    # 初始化模型
    model = AlexNet(num_classes=NUM_CLASSES).to(device)

    # 损失函数和优化器
    criterion = nn.CrossEntropyLoss()
    optimizer = SGD(model.parameters(), lr=0.01, momentum=0.9, weight_decay=5e-4)
    scheduler = CosineAnnealingWarmRestarts(optimizer, T_0=10, T_mult=2)

    # 训练参数
    epochs = 50
    best_acc = 0.0
    train_losses = []
    val_losses = []
    val_accs = []

    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        for inputs, targets in train_loader:
            inputs, targets = inputs.to(device), targets.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

        train_loss = running_loss / len(train_loader)
        train_losses.append(train_loss)

        # 验证
        model.eval()
        val_loss = 0.0
        correct = 0
        total = 0
        with torch.no_grad():
            for inputs, targets in val_loader:
                inputs, targets = inputs.to(device), targets.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, targets)
                val_loss += loss.item()
                _, predicted = outputs.max(1)
                total += targets.size(0)
                correct += predicted.eq(targets).sum().item()

        val_loss /= len(val_loader)
        val_acc = 100. * correct / total
        val_losses.append(val_loss)
        val_accs.append(val_acc)

        scheduler.step()

        print(f'Epoch {epoch+1}/{epochs}, Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%')

        # 保存最佳模型
        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(), 'AlexNet_best.pth')

    # 保存最终模型
    torch.save(model.state_dict(), 'AlexNet.pth')

    # 绘制训练曲线
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 3, 1)
    plt.plot(train_losses, label='Train Loss')
    plt.plot(val_losses, label='Val Loss')
    plt.legend()
    plt.title('Loss')

    plt.subplot(1, 3, 2)
    plt.plot(val_accs, label='Val Acc')
    plt.legend()
    plt.title('Accuracy')

    plt.tight_layout()
    plt.savefig('training_history.png')
    plt.show()

    print(f'Best validation accuracy: {best_acc:.2f}%')

if __name__ == '__main__':
    main()