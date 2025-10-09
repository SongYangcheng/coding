class Food:
    def __init__(self):
        self.time = 0
        self.state = "生的"
        self.flavour = []
    
    def barbeque(self):
        # self.time = int(input("请输入要烧烤的时间:"))
        if self.time < 3:
            self.state = "生的"
        elif 3 <=  self.time  <= 5:
            self.state = "半生不熟"
        elif 15 <= self.time <= 25:
            self.state = "熟的"
        elif self.time > 30:
            self.state = "烤糊了"
        
    def addFlavour(self):
        self.flavour = input("请添加调料:").split()
        
    def print_out(self):
        print(f"你的食物状态：{self.state}")
        print(f"你添加了：{",".join(self.flavour)}")

def main():
    f = Food()
    tag = True
    while tag == True:
        print("1.开始烧烤, 2.继续烧烤, 3.添加调料, 4.查看当前状态, 5.结束烧烤")
        choice = int(input("请输入你的选择:"))
        if choice == 1:
            f.time = int(input("请输入要烧烤时间："))
        elif choice == 2:
            f.time += int(input("请输入继续烧烤时间"))
        elif choice == 3:
            f.flavour = input("请输入你要添加的调料：").split()
        elif choice == 4:
            f.print_out()
        elif choice == 5:
            tag = False

if __name__ == "__main__":
    main()
        