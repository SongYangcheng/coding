import os
import torch
from PIL import Image
from torchvision import transforms
import matplotlib.pyplot as plt
import json
import numpy as np

from split_data import get_dataset_list, get_train_and_val
from model_AlexNet import AlexNet

def predict_visualization():
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    num_classes = 5

    # 数据组织方式
    data_transform = transforms.Compose([
        transforms.Resize((227, 227)),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    # 读取类别标签
    json_path = 'classes.json'
    with open(json_path, "r") as f:
        class_json = json.load(f)

    # 载入训练模型
    model = AlexNet(num_classes=num_classes).to(device)
    weights_path = r'AlexNet.pth'
    model.load_state_dict(torch.load(weights_path))
    model.eval()  # 转为评估模式，将处理所有神经元

    # 获取测试图片列表
    test_list = get_dataset_list(r'test.txt')
    img_list, true_labels = test_list

    # 随机选择15张图片进行可视化
    np.random.seed(42)
    selected_indices = np.random.choice(len(img_list), 15, replace=False)

    # 创建大图
    plt.figure(figsize=(20, 15))
    plt.suptitle('Flower Classification Prediction Results', fontsize=16)

    for i, idx in enumerate(selected_indices, 1):
        image_path = img_list[idx]
        true_label = true_labels[idx]

        # 加载和预处理图片
        img = Image.open(image_path)
        img_tensor = data_transform(img)
        img_tensor = torch.unsqueeze(img_tensor, dim=0)

        # 预测
        with torch.no_grad():
            output = torch.squeeze(model(img_tensor.to(device))).cpu()
            predict = torch.softmax(output, dim=0)
            predict_index = torch.argmax(predict).numpy()

        # 创建子图
        plt.subplot(3, 5, i)
        plt.imshow(img)
        plt.axis('off')   # 关闭x轴y轴

        # 预测结果
        pred_class = class_json[str(predict_index)]
        true_class = true_label

        # 设置标题和颜色
        color = 'green' if pred_class == true_class else 'red'
        plt.title(f'Pred: {pred_class}\nTrue: {true_class}\nProb: {predict[predict_index].numpy():.2%}', color=color, fontsize=10)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('flower_prediction_results.png', dpi=300, bbox_inches='tight')
    plt.show()

def predict_single_image():
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    num_classes = 5

    # 数据组织方式
    data_transform = transforms.Compose([
        transforms.Resize((227, 227)),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    # 读取类别标签
    json_path = 'classes.json'
    with open(json_path, "r") as f:
        class_json = json.load(f)

    # 载入训练模型
    model = AlexNet(num_classes=num_classes).to(device)
    weights_path = r'AlexNet.pth'
    model.load_state_dict(torch.load(weights_path))
    model.eval()  # 转为评估模式

    # 从test.txt中获取测试图片
    test_list = get_dataset_list(r'test.txt')
    img_list, labels = test_list

    # 为每个类别选择一张图片
    selected_images = []
    selected_labels = []
    used_classes = set()

    for img_path, label in zip(img_list, labels):
        if label not in used_classes:
            selected_images.append(img_path)
            selected_labels.append(label)
            used_classes.add(label)  # 图片上面添加标签
            if len(used_classes) == num_classes:  # 当我们有了所有类别的图片就停止
                break

    # 创建大图
    plt.figure(figsize=(20, 6))
    plt.suptitle('Single Flower Image Classification', fontsize=16)

    for i, (image_path, true_label) in enumerate(zip(selected_images, selected_labels), 1):
        # 加载图片和预处理图片
        img = Image.open(image_path)
        img_tensor = data_transform(img)
        img_tensor = torch.unsqueeze(img_tensor, dim=0)

        # 预测
        with torch.no_grad():
            output = torch.squeeze(model(img_tensor.to(device))).cpu()
            predict = torch.softmax(output, dim=0)
            predict_index = torch.argmax(predict).numpy()

        # 创建子图
        plt.subplot(1, 5, i)
        plt.imshow(img)
        plt.axis('off')  # 隐藏x轴和y轴

        # 预测结果
        pred_class = class_json[str(predict_index)]

        # 设置标题颜色
        color = 'green' if pred_class == true_label else 'red'
        plt.title(f'Pred: {pred_class}\nTrue: {true_label}\nProb: {predict[predict_index].numpy():.2%}', color=color, fontsize=10)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('sigle_flower_predictions.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == '__main__':
    predict_visualization()
    predict_single_image()

