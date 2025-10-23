#一对一映射：你中有我我中有你
class Member:
    def __init__(self, mid=None, name=None):
        self.mid=mid
        self.name=name
        self.car=None #关键car=None表示初始化
    def __str__(self): #该用法不要和car中的参数一样否则会死循环
        return f"姓名:{self.name},车辆信息:[{self.car}]"
    def __repr__(self): 
        #对象表示
        return f"Member({self.mid},{self.name})"

