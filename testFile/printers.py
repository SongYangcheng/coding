#多态
class Printer:
    """打印机基类，定义基本属性和接口"""
    def __init__(self, brand, model, is_connected=False):
        self.brand = brand
        self.model = model
        self.is_connected = is_connected
        self.paper_count = 100          # 纸张数量（对 3D 打印机可忽略）
        self.status = "待机中"

    def connect(self):
        """连接到电脑"""
        self.is_connected = True
        self.status = "待机中"
        print(f"{self.brand} {self.model} 已成功连接")

    def add_paper(self, count):
        """添加纸张"""
        self.paper_count += count
        print(f"已添加纸张，当前纸张数 {self.paper_count}")

    def print(self, document):
        """基类打印，子类可扩展"""
        if not self.is_connected:
            print(f"{self.brand} {self.model} 未连接电脑")
            return False
        if self.paper_count <= 0:
            print(f"{self.brand} {self.model} 纸张不足，请添加纸张")
            return False
        self.status = "打印中"
        return True


class Computer:
    """电脑类用于发送打印指令"""
    def __init__(self, name):
        self.name = name
        self.connected_printers = []  # 保存已连接打印机

    def connect_printer(self, printer: Printer):
        """连接打印机"""
        if printer not in self.connected_printers:
            self.connected_printers.append(printer)
            printer.connect()
            print(f"{self.name} 已连接打印机: {printer.brand} {printer.model}")
        else:
            print(f"{printer.brand} {printer.model} 已在列表中")

    def send_print_job(self, document):
        """向所有连接的打印机发送打印任务"""
        if not self.connected_printers:
            print(f"{self.name} 尚未连接任何打印机")
            return
        print(f"{self.name} 发送打印任务: {document}")
        for p in self.connected_printers:
            ok = p.print(document)
            if ok:
                print(f"{p.brand} {p.model} 完成任务: {document}")
            print("------")


class InkjetPrinter(Printer):
    """喷墨打印机"""
    def __init__(self, brand, model):
        super().__init__(brand, model)
        self.ink_levels = {
            "black": 80,
            "cyan": 60,
            "magenta": 60,
            "yellow": 50
        }

    def print(self, document):
        if not super().print(document):
            return False
        # 检查墨水
        low_colors = [c for c, lvl in self.ink_levels.items() if lvl < 10]
        if low_colors:
            print(f"{self.brand} {self.model} 墨水不足: {','.join(low_colors)}")
        print(f"{self.brand} {self.model} 正在喷墨打印: {document}")
        print("彩色喷头工作，成像中...")
        print(f"墨水状态：黑 {self.ink_levels['black']}%")
        # 消耗
        self.paper_count -= 1
        for k in self.ink_levels:
            self.ink_levels[k] = max(0, self.ink_levels[k] - 1)
        self.status = "待机中"
        return True


class LaserPrinter(Printer):
    """激光打印机"""
    def __init__(self, brand, model):
        super().__init__(brand, model)
        self.toner_level = 70    # 碳粉
        self.drum_health = 90    # 鼓组件健康

    def print(self, document):
        if not super().print(document):
            return False
        if self.toner_level < 15:
            print(f"{self.brand} {self.model} 碳粉不足，请尽快更换")
        print(f"{self.brand} {self.model} 激光打印: {document}")
        print(f"碳粉剩余 {self.toner_level}%，鼓组件健康 {self.drum_health}%")
        self.paper_count -= 1
        self.toner_level = max(0, self.toner_level - 1)
        self.status = "待机中"
        return True


class Printer3D(Printer):
    """3D 打印机（不使用纸张逻辑）"""
    def __init__(self, brand, model):
        super().__init__(brand, model)
        self.filament_type = "PLA"
        self.filament_remaining = 50  # 耗材百分比

    def print(self, document):
        # 3D 打印忽略纸张检测，可只检查连接
        if not self.is_connected:
            print(f"{self.brand} {self.model} 未连接电脑")
            return False
        self.status = "打印中"
        if self.filament_remaining < 10:
            print(f"{self.brand} {self.model} 耗材不足，请补充")
        print(f"{self.brand} {self.model} 3D 打印: {document}")
        print(f"喷头挤出 {self.filament_type} 材料分层构建")
        print(f"剩余耗材 {self.filament_remaining}%")
        self.filament_remaining = max(0, self.filament_remaining - 2)
        self.status = "待机中"
        return True


if __name__ == "__main__":
    office_pc = Computer("办公室电脑")

    inkjet = InkjetPrinter("惠普", "DeskJet 3755")
    laser = LaserPrinter("佳能", "LBP6030w")
    printer3d = Printer3D("爱普生", "ET-7000")

    office_pc.connect_printer(inkjet)
    office_pc.connect_printer(laser)
    office_pc.connect_printer(printer3d)

    office_pc.send_print_job("季度报告.pdf")
    office_pc.send_print_job("产品设计.stl")
