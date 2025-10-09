class Things():
    def __init__(self, name, area):
        self.name = name
        self.area = area

class LineseHouse:
    def __init__(self, thing, area):
        self.postion = "中俄边界"
        self.square = 150
        self.leaveSquare = 50 - area
        self.contextThing = []
        self.thing = thing
    def context(self):
        self.contextThing.append(self.thing)

    def message(self):
        if self.leaveSquare >= 0:
            print(f"岗哨位置:{self.postion}, 剩余面积:{self.leaveSquare}, 当前物资为:{self.contextThing}")
        else:
            print("物资不够容纳")

T = Things("香蕉", 20)
L = LineseHouse(T.name, T.area)
L.context()
L.message()