from pyexpat import model
import warnings
import joblib
import numpy as np
from streamlit import st
from PIL import Image
from streamlit_option_menu import option_menu #导入菜单栏

#忽略警告
warnings.filterwarnings("ignore")

#加载模型
model = joblib.load('./mnist_784.pth') #此处模型先进性计算后才能导入

def  predict_digit(image):
    img = image.convert('L') #转换为灰度图
    img = img.resize((28, 28)) #压缩为 28x28
    img = np.array(img).reshape(1, -1) #转换为数组并展平
    prediction = model.predict(img) #进行预测
    return prediction[0]

