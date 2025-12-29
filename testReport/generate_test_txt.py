import os
import random

# 数据集根目录
DATA_ROOT = r'D:\Users\25711\下载\专业方向强化课程4-实验报告1\flower_photos花卉数据集\flower_photos'
CLASSES = ['daisy', 'dandelion', 'roses', 'sunflowers', 'tulips']

# 收集所有图片路径和标签
img_paths = []
labels = []
for i, cls in enumerate(CLASSES):
    cls_dir = os.path.join(DATA_ROOT, cls)
    if os.path.exists(cls_dir):
        for img_name in os.listdir(cls_dir):
            if img_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                img_paths.append(os.path.join(cls_dir, img_name))
                labels.append(str(i))  # 标签为字符串

# 随机选择 10% 作为测试集（例如 367 张）
random.seed(42)
test_size = int(0.1 * len(img_paths))
test_indices = random.sample(range(len(img_paths)), test_size)

# 写入 test.txt
with open('test.txt', 'w') as f:
    for idx in test_indices:
        f.write(f"{img_paths[idx]} {labels[idx]}\n")

print(f"Generated test.txt with {test_size} images.")