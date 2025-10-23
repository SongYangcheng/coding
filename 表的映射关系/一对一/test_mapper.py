from car import Car
from Member import Member
def main():
    #主函数测试
    #定义对象
    member = Member(1,'张三')
    car = Car('宝马','红色')
    #一个人对应一辆车
    member.car = car
    car.member = member
    print(member)
    print(car)
if __name__ == '__main__':
    main()