import sys # 系统相关参数和函数
import torch # PyTorch,用于深度学习模型的构建和调练
import cv2 # OpenCV,用于图像处理任务
import numpy as np # Numpy,用于数值计算
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget # PyQt5/#
from PyQt5.QtGui import QImage, QPixmap # PyQt5图燥处理类
from PyQt5.QtCore import Qt # PyQt5核心功能,如对齐方式等
from torchvision import transforms # 包含图形预处理功的
from AlexNet import AlexNet
import utils

class ImageClassifierApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setupModel()

    def initUI(self):
        self.setWindowTitle('图像分类器')
        self.setGeometry(100,100,800,600)

        central_weight = QWidget()
        self.setCentralWidget(central_weight)
        layout = QVBoxLayout(central_weight)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(400,400)
        layout.addWidget(self.image_label)

        self.result_label = QLabel('预测结果将在这里显示')
        self.result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_label)

        self.select_button = QPushButton('选择图片')
        self.select_button.clicked.connect(self.selectImage)
        layout.addWidget(self.select_button)

        self.predict_button = QPushButton('开始预测')
        self.predict_button.clicked.connect(self.predict)

        self.predict_button.setEnabled(False)
        layout.addWidget(self.predict_button)

    def setupModel(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        try:
            self.model = AlexNet()
            self.model = self.model.float()
            self.model.load_state_dict(torch.load('./logs/final_model.pth'))
            self.model = self.model.to(self.device)
        except Exception as e:
            print(f'Model setup error:{str(e)}')
            raise

    def selectImage(self):
        file_name,_ = QFileDialog.getOpenFileName(
            self,'选择图片',"","图像文件( *. jpg *. jpeg *. png *. bmp)")

        if file_name:
            try:
                self.current_image = cv2.imread(file_name)
                if self.current_image is not None:
                    display_image = self.resizeImage(self.current_image.copy(),400)
                    height,width,channel = display_image.shape
                    bytes_per_line = 3 * width
                    qt_image = QImage(
                        display_image.data,width,height,bytes_per_line,
                        QImage.Format_RGBA8888).rgbSwapped()
                    self.image_label.setPixmap(QPixmap.fromImage(qt_image))
                    # 启动预测按钮
                    self.predict_button.setEnabled(True)  # 允许点击预测按钮
                    # 清除之前的预测结果
                    self.result_label.setText('图片已加载,点击“开始预测”进行预测')
                    # 更新结果标签文本
                else:
                    self.result_label.setText('图片加载失败')  # 如果图像加载失败,更新结果标签文本
            except Exception as e:
                print(f"Image loading error: {str(e)}")  # 如果发生错误,打印错误信息
                self.result_label.setText('图片加载出错')  # |

    def resizeImage(self, image, target_size):
        h, w = image.shape[:2]
        if h > w:
            new_h = target_size  # 新的高度为目标尺寸
            new_w = int(w * target_size / h)
        else:
            new_w = target_size  # 新的宽度为目标尺寸
            new_h = int(h * target_size / w)  # 新的盖度按比例缩放
        return cv2.resize(image, (new_w, new_h))

    def predict(self):
        if self.current_image is not None:
            try:
                h, w = self.current_image.shape[: 2]
                # 获取图像的高度和宽度
                size = min(h, w)  # 获取较短的一边作为裁剪尺寸
                y_start = (h - size) // 2  # 计算y轴起始位置
                x_start = (w - size) // 2  # 计算x轴起始位置
                cropped_img = self.current_image[y_start:y_start + size, x_start:x_start + size]

                # 2. 转换颜色空间并归一化
                img_RGB = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)  # 将BGR格式转换为RGB格式
                img_resized = cv2.resize(img_RGB,(224, 224))  # 调整图像大小到224x224
                img_float = img_resized.astype(np.float32) / 255.0  # 归一化像素值到[e,1]

                # 3. 转换为 tensor 并调整维度
                img_tensor = torch.from_numpy(img_float).permute(2, 0, 1)  # 将numpy数组转换为torch
                img_tensor = img_tensor.unsqueeze(0)  # 增加一个批次维度

                #4.标准化
                normalize = transforms.Normalize(
                    mean = [0.485,0.456,0.406],
                    std = [0.229,0.224,0.225]
                )
                img_tensor = normalize(img_tensor)

                img_tensor = img_tensor.to(self.device,dtype = torch.float32)

                self.model.eval()
                with torch.no_grad():  # 关闭梯度计算以节省内存
                    outputs = self.model(img_tensor)  # 模型推理,获取输出
                # 注意:模型已经包含了softmax 层,不需要再次应用
                confidence, predicted = torch.max(outputs, 1)

                # 获取预测结果和置信度
                result = utils.print_answer(predicted.item())
                confidence_value = confidence.item() * 100

                # 显示预测结果和置信度
                self.result_label.setText(
                    f'预测结果:{result}\n置信度:{confidence_value :. 2f}%')  # 更新结果标签文本
            except Exception as e:
                print(f'Prediction error:{str(e)}')
                self.result_label.setText(f'预测出错：{str(e)}')

        else:
            self.result_label.setText('请先选择一张图片')

def main():
    app = QApplication(sys.argv)
    window = ImageClassifierApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()