import warnings
import joblib
import numpy as np
import streamlit as st
from PIL import Image
from repo_cli.commands.upload import upload_file
from streamlit_option_menu import option_menu

# 忽略警告
warnings.filterwarnings("ignore")

# 加载模型
model = joblib.load('./mnist_784.pth')

def predict_digit(image):
    img = image.convert('L') # 转换为灰度图
    img = img.resize((28, 28)) # 压缩为 28x28
    img = np.array(img).reshape(1, -1) # 转换为数组并展平
    prediction = model.predict(img) # 进行预测
    return prediction[0]

def main():
    st.title('手写数字识别')

    # 添加侧边栏菜单
    selected = option_menu(
        menu_title=None,  # 无标题
        options=["首页", "上传图片", "关于"], # 菜单选项
        icons=["house", "cloud-upload", "info-circle"], # 图表
        menu_icon="cast",   # 菜单图标 (注意：代码中似乎写的是 menu_icons="case"，但这通常是 menu_icon="cast" 的笔误)
        default_index=0,    # 默认选中项
        orientation="horizontal" # 横向布局
    )

    if selected == "首页":
        st.subheader("欢迎使用手写数字识别系统")
        st.write("请通过上传图片来识别手写数字。")

    elif selected == "上传图片":
        st.subheader("上传图片进行识别")
        uploaded_file = st.file_uploader("请选择图片", type=["png", "jpg", "jpeg"])

        if uploaded_file is not None:
            # 显示上传图片
            image = Image.open(uploaded_file)
            st.image(image, caption="上传的图片", use_column_width=True)

            # 进行预测
            prediction = predict_digit(image)
            st.write(f'预测结果为: {prediction}')

    elif selected == "关于":
        st.subheader("关于本项目")
        st.write("这是一个基于 K-最近邻 (KNN) 算法的手写识别系统。")
        st.write("数据来自 MNIST，模型使用 scikit-learn 训练。")
        st.write("开发工具：Streamlit, Python, scikit-learn, PIL.")

if __name__ == '__main__':
    main()