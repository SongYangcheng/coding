
class Car:
    def __init__(self, title=None, color=None):

        self.title=title
        self.color=color
        self.member=None #关键member=None表示初始化关联字段
    def __str__(self):
        return f'颜色:{self.color}]'
    def __repr__(self): #官方对象表示
        return f'Car({self.title},{self.color})'
        