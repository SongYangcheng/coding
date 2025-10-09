# coding: UTF-8

import time

from pynput import mouse,keyboard

m_mouse = mouse.Controller()

print(m_mouse.position) #鼠标定位

time.sleep(0.1)
m_mouse = mouse.Controller()
m_keyboard = keyboard.Controller() #获取键盘控制
m_mouse.position = (850, 670)
m_mouse.click(mouse.Button.left) #控制鼠标右键点击

while(True):
    m_keyboard.type("叫爸爸")
    m_keyboard.press(keyboard.Key.enter) #按压回车键
    m_keyboard.release(keyboard.Key.enter) #反复
    time.sleep(0.1)