import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import numpy as np
import cv2
import os
from torchvision import transforms
from torch.optim import SGD
from torch.optim.lr_scheduler import CosineAnnealingWarmRestarts
import matplotlib.pyplot as plt
# 假设 AlexNet 在同级目录的 AlexNet.py 文件中，如果报错请检查文件名
from AlexNet import AlexNet 

# --- 配置部分 ---
# 获取当前脚本所在的绝对路径，避免相对路径报错
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 图片所在的文件夹根目录 (根据你的代码逻辑调整)
# 修改为你的实际下载路径 (注意前面的 r 表示原始字符串，防止转义)
IMAGE_ROOT = r'D:\Users\25711\Downloads\AlexNet猫狗识别数据集data\data\image\train'
# 标签列表文件路径
LIST_FILE_PATH = os.path.join(BASE_DIR, 'photo_list.txt') # 建议放在项目根目录，或者你可以改回你的绝对路径

# 定义训练数据增强策略
train_transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# 定义验证集转换
val_transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

class CustomDataset(Dataset):
    def __init__(self, lines, img_dir, transform=None):
        self.lines = lines
        self.img_dir = img_dir # 接收图片根目录
        self.transform = transform

    def __len__(self):
        return len(self.lines)

    def __getitem__(self, idx):
        line_content = self.lines[idx].strip()
        # 解析文件名和标签
        try:
            parts = line_content.split(';')
            name = parts[0]
            label = int(parts[1])
            
            # 构建绝对路径
            img_path = os.path.join(self.img_dir, name)

            # 【关键修复】使用 imdecode 读取，支持中文路径，且更稳定
            # 先读取为 numpy 数组，再解码
            img_np = np.fromfile(img_path, dtype=np.uint8)
            img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

            # 【关键修复】空值检查
            if img is None:
                raise ValueError(f"Image decoded is None: {img_path}")

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            if self.transform:
                img = self.transform(img)

            return img, label

        except Exception as e:
            # 打印简短的错误日志，避免刷屏
            print(f"[Warn] Error loading sample index {idx}: {e}")
            
            # 返回一个全黑的默认图片，防止程序崩溃
            img = np.zeros((224, 224, 3), dtype=np.uint8)
            if self.transform:
                img = self.transform(img)
            return img, 0 # 返回默认标签 0


def train_model(model, train_loader, val_loader, criterion, optimizer, scheduler, device, num_epochs, log_dir, patience=7):
    history = {
        'train_loss': [], 'train_acc': [],
        'val_loss': [], 'val_acc': [],
        'lr': []
    }
    best_val_acc = 0
    counter = 0

    for epoch in range(num_epochs):
        # --- 训练阶段 ---
        model.train()
        train_loss = 0.0  # 修复初始化错误
        train_correct = 0 # 修复初始化错误
        train_total = 0   # 修复初始化错误

        for batch_idx, (images, labels) in enumerate(train_loader):
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()

            # 梯度裁剪
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()

            train_loss += loss.item()
            _, predicted = outputs.max(1)
            train_total += labels.size(0)
            train_correct += predicted.eq(labels).sum().item()

        # 计算平均值
        train_loss = train_loss / len(train_loader)
        train_acc = 100. * train_correct / train_total

        # --- 验证阶段 ---
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0

        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)

                val_loss += loss.item()
                _, predicted = outputs.max(1)
                val_total += labels.size(0)
                val_correct += predicted.eq(labels).sum().item()

        val_loss = val_loss / len(val_loader)
        val_acc = 100. * val_correct / val_total

        # 更新学习率
        scheduler.step()
        current_lr = scheduler.get_last_lr()[0]

        # 记录历史
        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)
        history['lr'].append(current_lr)

        # 保存最佳模型
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            counter = 0
            torch.save(model.state_dict(), os.path.join(log_dir, 'best_model.pth'))
        else:
            counter += 1

        # 定期保存 Checkpoint
        if (epoch + 1) % 3 == 0:
            torch.save(model.state_dict(), os.path.join(log_dir, f'ep{epoch:03d}-loss{train_loss:.3f}.pth'))

        print(f'Epoch [{epoch + 1}/{num_epochs}] '
              f'Train Loss: {train_loss:.4f} Acc: {train_acc:.2f}% | '
              f'Val Loss: {val_loss:.4f} Acc: {val_acc:.2f}% | LR: {current_lr:.6f}')

        # 早停
        if counter >= patience:
            print(f'Early stopping triggered after {epoch + 1} epochs')
            break
            
    return history

def plot_training_history(history, log_dir):
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 3, 1)
    plt.plot(history['train_loss'], label='Train Loss')
    plt.plot(history['val_loss'], label='Val Loss')
    plt.title('Loss History')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()

    plt.subplot(1, 3, 2)
    plt.plot(history['train_acc'], label='Train Acc')
    plt.plot(history['val_acc'], label='Val Acc')
    plt.title('Accuracy History')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy (%)')
    plt.legend()

    plt.subplot(1, 3, 3)
    plt.plot(history['lr'])
    plt.title('Learning Rate History')
    plt.xlabel('Epoch')
    plt.ylabel('Learning Rate')

    plt.tight_layout()
    plt.savefig(os.path.join(log_dir, 'training_history.png'))
    plt.close()

def main():
    # 设置随机种子
    torch.manual_seed(32)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(42)
    np.random.seed(42)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'Using device: {device}')

    log_dir = os.path.join(BASE_DIR, 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # 读取列表文件
    # 如果你的文件路径确实在 D盘固定位置，请修改回你的绝对路径：
    # list_path = r'D:\python_demo\coding\deepLearning\project_catdog\photo_list.txt'
    list_path = LIST_FILE_PATH 
    
    if not os.path.exists(list_path):
        print(f"Error: 找不到列表文件: {list_path}")
        return

    with open(list_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    np.random.shuffle(lines)
    
    # 划分数据集
    num_val = int(len(lines) * 0.1)
    if num_val == 0: num_val = 1 # 防止数据集过小报错
    
    train_lines = lines[:-num_val]
    val_lines = lines[-num_val:]

    # 实例化 Dataset，传入图片根目录
    train_dataset = CustomDataset(train_lines, img_dir=IMAGE_ROOT, transform=train_transform)
    val_dataset = CustomDataset(val_lines, img_dir=IMAGE_ROOT, transform=val_transform)

    batch_size = 64
    # Windows 下如果 num_workers > 0 经常报错或卡死，如果卡住请改为 0
    num_workers = 4 if os.name != 'nt' else 0 

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True
    )

    print(f'Training on {len(train_lines)} samples, Validating on {len(val_lines)} samples')

    # 初始化模型
    model = AlexNet().to(device) # 假设你需要传递类别数，或者在AlexNet内部修改
    criterion = nn.CrossEntropyLoss()
    
    optimizer = SGD(
        model.parameters(),
        lr=0.01,
        momentum=0.9,
        weight_decay=5e-4,
        nesterov=True,
    )

    scheduler = CosineAnnealingWarmRestarts(
        optimizer,
        T_0=10,
        T_mult=2,
        eta_min=1e-6
    )

    num_epochs = 50
    patience = 7

    history = train_model(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        criterion=criterion,
        optimizer=optimizer,
        scheduler=scheduler,
        device=device,
        num_epochs=num_epochs,
        log_dir=log_dir,
        patience=patience
    )

    plot_training_history(history, log_dir)
    torch.save(model.state_dict(), os.path.join(log_dir, 'final_model.pth'))
    print("Training Finished!")

if __name__ == '__main__':
    main()