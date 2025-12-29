import os

def get_dataset_list(test_file_path):
    """
    从 test.txt 文件中读取图片路径和标签列表。
    假设 test.txt 格式为每行: image_path label
    """
    img_list = []
    labels = []
    with open(test_file_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                img_path, label = parts
                img_list.append(img_path)
                labels.append(label)
    return img_list, labels

def get_train_and_val(train_file_path, val_file_path):
    """
    从 train.txt 和 val.txt 文件中读取训练和验证数据。
    假设格式类似 get_dataset_list。
    返回训练和验证的图片路径和标签列表。
    """
    train_img_list, train_labels = get_dataset_list(train_file_path)
    val_img_list, val_labels = get_dataset_list(val_file_path)
    return train_img_list, train_labels, val_img_list, val_labels