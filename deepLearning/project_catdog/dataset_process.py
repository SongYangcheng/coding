import os

# 使用 r'' 原始字符串防止路径中的转义字符问题
data_dir = r'D:\Users\25711\Downloads\AlexNet猫狗识别数据集data\data\image\train'

# 检查路径是否存在，防止报错
if not os.path.exists(data_dir):
    print(f"错误: 找不到路径 {data_dir}")
else:
    photos = os.listdir(data_dir)
    print(f"找到 {len(photos)} 个文件")

    # 指定 encoding='utf-8' 是个好习惯
    with open('photo_list.txt', 'w', encoding='utf-8') as f:
        count_cat = 0
        count_dog = 0
        
        for photo in photos:
            # 过滤掉非图片文件（比如系统生成的 Thumbs.db 等）
            if not photo.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                continue

            # 使用 startswith 判断更稳健，防止文件名中包含多个点导致 split 出错
            # 这里的 photo 是文件名，例如 "cat.123.jpg"
            if photo.startswith('cat'):
                # 【关键修改】使用 ';' 作为分隔符，与 Dataset 代码保持一致
                f.write(f'{photo};0\n') 
                count_cat += 1
            elif photo.startswith('dog'):
                f.write(f'{photo};1\n')
                count_dog += 1
    
    print("生成完成！")
    print(f"猫: {count_cat} 张, 狗: {count_dog} 张")
    # with 语句块结束后文件会自动关闭，不需要写 f.close()