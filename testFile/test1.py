import os, sys
import time
#time.localtime()显示当前时间类型为 <class 'time.struct_time'> 
time_now = time.localtime()

#格式化时间输出tme.strftime()可自定义，类型为<class 'str'>
time_mod = time.strftime("%Y-%m-%d %H:%M:%S", time_now)

print(time_now, type(time_now))
print(time_mod, type(time_mod))
print(sys.platform.startswith("win"))

#处理盘符根目录

def get_available_drives():
    """获取当前系统中可用盼复根路径，适配windows"""
    if sys.platform.startswith('win'): # sys.platform 获取系统信息win32
        drives = []
        #遍历A-Z所有可能的盘符字母
        for drive in 'DE':
            drive_path = f'{drive}:\\' #拼接盘符路径 D:\\
            #检查该盘符是否存在（是否有对应分区）
            #os.path.exists()判断文件路径是否存在
            if os.path.exists(drive_path):
                drives.append(drive_path)
        return drives #返回windows心痛可用盘符
    else:
        return ['/']
    
def main(): #定义主函数
    """用户互动, 路径验证， 启动扫描及其显示最终结果"""
    print("可用的扫描路径：")
    drivers = get_available_drives()

    #遍历可用路径，用编号标识每个路径
    for i, drive in enumerate(drivers, 1):
        print(f"{i}:{drive}")

    try:
        #提示用户编号，直接回车使用默认路径
        choice = input("\n请输入要扫描盘符(直接回车为默认路径)")
        if choice.strip():
            #将用户字符串转换为整数减一后列表从0开始
            index = int(choice) - 1
            if 0 <= index <= len(drivers):
                scan_path = drivers[index]
            else:
                print("输入无效将使用默认路径")

                scan_path = os.getcwd() #获取当前路径
        else:
            scan_path = os.getcwd()

            print(f"将扫描当前路径{scan_path}")
    except ValueError:

        print("输入异常将使用默认路径")
        scan_path = os.getcwd()
        

    if not os.path.exists(scan_path):
        print(f"{scan_path}路径不存在")
        sys.exit(1) #调用sys退出程序 ， 1为异常退出

    if not os.path.isdir(scan_path):
        print(f"{scan_path}不是路径")
        sys.exit(1)
    
    print(f"\n开始扫描路径:{scan_path}")
    start_time = time.time() #记录扫描开始时间

    #调用扫描函数执行扫描，接受返货总统数据
    # total_dirs, total_files, total_size = scan_with_stats(scan_path)

    end_time = time.time() #结束时间
    elapsed_time = end_time - start_time

    print(f"扫描耗时{elapsed_time:.2f}")
    # print(f"目录：{total_dirs}, 文件：{total_files}, 总大小: {total_size}")

if __name__ == "__main__":
    main()
