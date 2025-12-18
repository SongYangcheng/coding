import matplotlib.image as mpimg
import numpy as np
import torch
from torchvision import transforms
from PIL import Image
import os

def load_image(path):
    """
    读取图片并进行中心裁剪（正方形）
    """
    # mpimg.imread 读取的图片可能是 float(0-1) 也可能是 int(0-255)
    img = mpimg.imread(path)
    
    # 处理通道问题：如果是灰度图 (H, W)，转换为 RGB (H, W, 3)
    if len(img.shape) == 2:
        img = np.stack([img]*3, axis=-1)
    # 处理 RGBA (H, W, 4)，只取前三个通道
    if img.shape[2] > 3:
        img = img[:, :, :3]

    short_edge = min(img.shape[:2])
    yy = int((img.shape[0] - short_edge) / 2)
    xx = int((img.shape[1] - short_edge) / 2)
    
    # 中心裁剪
    crop_img = img[yy: yy + short_edge, xx: xx + short_edge]
    return crop_img

def resize_image(image, size):
    """
    调整图片大小并转换为 Tensor
    """
    images = []
    
    # 增加 Batch 维度: (H, W, C) -> (1, H, W, C)
    if len(image.shape) == 3:
        image = np.expand_dims(image, axis=0)

    # 定义转换流程：Resize -> ToTensor (会自动将 0-255 转为 0-1 并归一化)
    transform = transforms.Compose([
        transforms.Resize(size),
        transforms.ToTensor(),
        # 建议加上与训练时一致的 Normalize，否则预测准确率会下降
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    for i in image:
        if isinstance(i, np.ndarray):
            # ---【关键修复】---
            # 判断当前数据类型，防止重复乘以 255
            if i.dtype == np.float32 or i.dtype == np.float64:
                # 只有当数据是小数且最大值 <= 1.0 时，才 * 255
                if i.max() <= 1.0:
                    i = (i * 255).astype(np.uint8)
                else:
                    i = i.astype(np.uint8)
            else:
                # 如果已经是整数（如 jpg），直接转
                i = i.astype(np.uint8)
            
            # 转为 PIL Image 以便进行 Resize
            i = Image.fromarray(i)
        
        # 执行转换
        i = transform(i)
        images.append(i)

    # 堆叠: (Batch, C, H, W)
    images = torch.stack(images)
    return images

def print_answer(argmax):
    """
    读取标签文件并将索引转换为类别名称
    """
    # 建议将路径提取为常量或参数
    file_path = './photo_list.txt' # 假设你的标签文件长这样：cat.0.jpg;0 或 cat;0
    
    # 这里的逻辑需要根据你实际的标签映射文件来修改
    # 通常训练时我们只保存类别名称列表，例如 classes.txt:
    # cat
    # dog
    
    # 这里假设是一个简单的列表：0是猫，1是狗
    classes = ['cat', 'dog'] 
    
    if torch.is_tensor(argmax):
        argmax = argmax.item()
    
    pred_name = classes[argmax]
    print(f"预测结果: {pred_name} (Index: {argmax})")
    return pred_name

# 如果你有具体的 index_word.txt 文件，请使用下面的版本：
def print_answer_from_file(argmax, file_path='./data/model/index_word.txt'):
    if not os.path.exists(file_path):
        print(f"错误: 找不到标签映射文件 {file_path}")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # 假设文件每一行格式为: index;class_name
            # 例如:
            # 0;cat
            # 1;dog
            synest = {}
            for l in f.readlines():
                parts = l.strip().split(';')
                if len(parts) >= 2:
                    synest[int(parts[0])] = parts[1]
        
        if torch.is_tensor(argmax):
            argmax = argmax.item()
            
        print(f"预测类别: {synest.get(argmax, '未知类别')}")
        
    except Exception as e:
        print(f"解析标签文件出错: {e}")