class grandfather:
    def __init__(self):
        self.boat = "bigboat"
        self.money = "somuchmonney"
    def action():
        print("你好我使grandfather")
class father:

    def action():
        print(f"你好我是father")

class son(grandfather, father):
    def __init__(self):
        super().__init__()
        
    def action(self):
        super().action()
        print("这是son")
s = son()
s.action()