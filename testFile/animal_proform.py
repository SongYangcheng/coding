class Animal:
    """动物基类"""
    def __init__(self, name, age,gender, keeper):
        self.name = name
        self.gender = gender
        self.age = age
        self.keeper = keeper
        self.energy = 100 #能量值
    def rest(self):
        self.energy = min(100, self.energy + 20)
        print(f"{self.name}重在休息恢复能量到{self.energy}")

    def perform(self):
        """动物表演的基方法，要在子类重写"""
        if self.energy < 30:
            print(f"{self.name}累了")
            return False
        
        self.energy -= 30
        print(f"{self.name}的能量剩余{self.energy}")
        return True
class Keeper:
    """饲养员负责管理动物"""
    def __init__(self, name):
        self.name = name
        self.animals = []
    def add_animal(self, animal):
         """添加饲养员动物"""
         self.animals.append(animal)
         print(f"饲养员{self.name}照顾{animal.name}")
    def ask_perform(self):
        print(f"饲养员{self.name}开始让动物表演")
        for animal in self.animals:
            animal.perform()
            print("+++++++++即将表演+++++++++++++++")
class Tiger(Animal):
    """老虎类"""
    def __init__(self, name, age, gender, keeper, stripe_count):
        super().__init__(name, age, gender, keeper)
        self.strip_count = stripe_count
        self.speed = 50

    def perform(self):
        if not super().perform(): #检查能能量
            return 
        
        print(f"{self.name} ShowTime展示捕猎突击速度{self.speed}")
        print(f"条纹数{self.strip_count}")
        
class Penguin(Animal):
    """企鹅类"""
    def __init__(self, name, age, gender, keeper, swimming_speed):
        super().__init__(name, age, gender, keeper)
        self.swimming_speed = swimming_speed
        self.flipper_length = 30

    def perform(self):
        if not super().perform(): #检查能能量
            return 
        
        print(f"{self.name} ShowTime展示游泳{self.swimming_speed}")
        print(f"鸡翅长度{self.flipper_length}")
        
class Elephant(Animal):
    """大象类"""
    def __init__(self, name, age, gender, keeper, trunk_length):
        super().__init__(name, age, gender, keeper)
        self.trunk_length = trunk_length
        self.tusk_length = 2

    def perform(self):
        if not super().perform(): #检查能能量
            return 
        
        print(f"{self.name} ShowTime展示喷水{self.trunk_length}")
        print(f"象牙个数{self.tusk_length}")

if __name__ == "__main__":
    zookeeper = Keeper("宋洋城")

    tiger = Tiger("威武", 5, "雄性", zookeeper, 100)
    penguin = Penguin("冰冰", 3, "雄性", zookeeper, 25)
    elephant = Elephant("但鹏飞", 6, "雄性", zookeeper, 2)

    zookeeper.add_animal(tiger)
    zookeeper.add_animal(penguin)
    zookeeper.add_animal(elephant)

    #饲养员要求动物表演
    print("\n--------------")
    zookeeper.ask_perform()

    #动物休息恢复能量
    print("\n -------------动物们休息一下-----------")
    tiger.rest()
    penguin.rest()
    #再次表演
    print("\n-------------去表演--------------")
    zookeeper.ask_perform()
    

