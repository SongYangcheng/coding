import numpy as np
import matplotlib.pyplot as plt

# 生成参数 t 的范围
t = np.linspace(0, 20 * np.pi, 1000) # 通常蝴蝶曲线需要较长的 t 范围才能完整展现

# 计算蝴蝶函数的 x 和 y 坐标
x_b = np.sin(t) * (np.exp(np.cos(t)) - 2*np.cos(4*t) - np.sin(t/12) ** 5)
y_b = np.cos(t) * (np.exp(np.cos(t)) - 2*np.cos(4*t) - np.sin(t/12) ** 5)

# 绘制蝴蝶曲线
plt.figure(figsize=(8, 8)) # 设置图表大小，让蝴蝶看起来更舒展
plt.plot(x_b, y_b, color='purple', linewidth=1)
plt.title('Butterfly Curve')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.grid(True, linestyle='--', alpha=0.6)
plt.axis('equal') # 保持X轴和Y轴的比例一致，避免变形
plt.show()