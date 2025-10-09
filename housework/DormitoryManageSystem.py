import random

with open("housework/chinaFirstName.txt", "r", encoding="utf-8") as f:
    data = f.read().replace("\n", "")
first_name_lis = []
for i in data:
    first_name = i.strip("，").strip("。").strip("").strip(" ")
    first_name_lis.append(first_name)
first_name_lis = list(set(first_name_lis))
first_name_lis.remove('')

dic = {}
#打印宿舍信息
def print_dic(dic):
    for key, value in dic.items():
        print(f"寝室{key} : {value}", end="\n")
# 删除函数
def delete_student(name):
    for key, value in dic.items():
        for i in range(len(value)- 1):
            if value[i] == name:
                value.remove(name)
                print(f"被删除的学生在{key} :删除后寝室剩余同学为 {value}")
    return dic
# 增添函数
def add_student(room_num, name):
    for key, value in dic.items():
        if key == room_num:
            dic[key].append(name)
            print(f"寝室{room_num}的成员为{value}")
    return dic
# 修改函数
def update_studnt(old_name, new_name):
    tag = False
    for key, value in dic.items():
        for i in range(len(value)):
            if value[i] == old_name:
                value[i] = new_name
                tag = True
                print(f"成功将学生：{old_name}修改为为：{new_name}")
    if tag == False:
        print("修改失败，请确认传入参数！")
    return dic
# 查找函数
def select_student(name):
    tag = False
    for key, value in dic.items():
        for i in range(len(value)):
            if value[i] == name:
                tag = True
                print(f"学生：{name}在寝室：{key}且寝室成员为：{value}")
    if tag == False:
        print("请输入正确学生姓名！")
    return dic
for i in range(1, 7):  # 层数
    
    for j in range(1, 17):  # 每层房间数      
            seed = random.randint(0, len(first_name_lis) - 1)
            room_name = i * 100 +  j
            student_name = "小" + first_name_lis[seed]
            lis_student_name = [student_name + f"{room_name}"+ f"{i}" for i in range(6)]
            for z in range(6):  # 每房间人数
                dic[room_name] = lis_student_name
            
print("=================================毕业前=================================")
print_dic(dic)
print("=================================毕业新生入住============================")
student_lis = list(input("请输入入住学生:").split())

print(f"入住学生:{student_lis}")

def shift_floors(dic, start_floor=1, end_floor=6, rooms_per_floor=16):
    # 1. 先做原始快照（按楼层、按房间）
    snapshot = {}
    for floor in range(start_floor, end_floor + 1):
        floor_dict = {}
        for r in range(1, rooms_per_floor + 1):
            room_no = floor * 100 + r
            if room_no in dic:
                floor_dict[room_no] = list(dic[room_no])  # 拷贝列表
        snapshot[floor] = floor_dict

    # 2. 从高楼层往下回填，避免链式污染
    for floor in range(end_floor, start_floor, -1):  # end_floor, ..., start_floor+1
        src_floor = floor - 1
        if src_floor not in snapshot:
            continue
        for r in range(1, rooms_per_floor + 1):
            src_room = src_floor * 100 + r
            dst_room = floor * 100 + r
            if src_room in snapshot[src_floor]:
                dic[dst_room] = list(snapshot[src_floor][src_room])  # 独立列表
        for key, value in dic.items():  
            if key < 200: 
                dic[key] = [v + f"{key}" for v in student_lis]

    return dic
dic = shift_floors(dic)
print_dic(dic)

tag = True
while(tag == True):
    print()
    print("1.查看当前寝室分布， 2.删除指定学生， 3.增添指定学生, 4.查找学生, 5.修改学生信息, 任意键退出")
    try:
        user_input = int(input("请选择操作操作："))
    except:
        print("成功退出")
        user_input = -1
    

    if user_input == 1:
        print_dic(dic)
    elif user_input == 2:
        print("=================================删除=====================================")
        name = input("请输入你要删除的学生姓名：")
        dic = delete_student(name)
        # print_dic(dic)
    elif user_input == 3:
        print("=================================增加=====================================")
        room_num, name = input("请输入你要添加的寝室号和学生姓名：").split()
        dic = add_student(int(room_num),name)
    elif user_input == 4:
        print("=================================查找=====================================")
        name = input("请输入你要查找的学生姓名：")
        dic = select_student(name)
    elif user_input == 5:
        print("=================================修改=====================================")
        old_name, new_name = input("请输入你要修改的学生姓名和新姓名：").split()
        dic = update_studnt(old_name, new_name)
    
    else:
        tag = False
#张三 李四 王五 刘备 张飞 关羽