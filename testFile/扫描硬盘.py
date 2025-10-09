import os
import time
import sys

def scan_with_state(path,indent = 0):
    dir_count = 0
    file_count = 0
    total_count = 0

    try:
        entries = os.listdir(path)

    except PermissionError: #权限异常报错捕获
        print(" " * indent + f"[权限不足]无法访问：{path}")
        return 0,0,0 #返回上述三个统计值（全部为零）
    except FileNotFoundError:#文件未找到
        print(" " * indent + f"[路径不存在]：{path}")
        return 0, 0, 0
    except OSError as e:
        print(" " * indent + f"[系统错误]：{path}:{str(e)}")
        return 0, 0, 0
    for entry in entries:
        full_path = os.path.join(path,entry)
        try:
            if os.path.isdir(full_path):
                dir_count += 1
                print(" " * indent + f"|——[目录]{entry}")
                sub_dirs,sub_files,sub_size = scan_with_state(full_path,indent + 4)
                dir_count += sub_dirs
                file_count += sub_files
                total_count += sub_size
            else:
                file_count += 1
                file_size = os.path.getsize(full_path)
                total_count += file_size
                mod_time = time.strftime(
                    "%Y-%m_%d %H:%M:%S",
                    time.localtime(os.path.getmtime(full_path))
                )
                print(" " * indent + f"|——[文件]{entry}({file_size}bytes,修改时间：{mod_time})")
        except PermissionError:
            print(" " * indent + f"|——[无法访问]{entry}(权限不足)")
        except OSError as e:
            print(" " * indent + f"|——[错误]{entry}:{str(e)}")
    print(" " * indent + f"|——[统计]目录：{dir_count},目录:{dir_count},文件：{file_count}，总大小：{total_count}bytes")
    return dir_count, file_count, total_count
def get_available_drives():
    if sys.platform.startswith("win"):
        drives = []
        for drive in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            drive_path = f"{drive}:\\"
            if os.path.exists(drive_path):
                drives.append(drive_path)
        return drives
    else:
        return ["/"]

def main():
    global scan_path
    print("可用的扫描路径：")
    drivers = get_available_drives()
    for i,drive in enumerate(drivers,1):
        print(f"{i},{drive}")
    try:
        choice = input("\n请输入要扫描的盘符编号：")
        if choice.strip():#判断用户是否输入内容
            index = int(choice) - 1
            if 0 <= index < len(drivers):
                scan_path = drivers[index]
            else:
                print("无效的选择，将使用默认路径")
        else:
            scan_path = os.getcwd()
            print(f"将扫描默认路径：{scan_path}")
    except ValueError:
        print("输入无效，将使用默认路径")
        scan_path = os.getcwd()
    if not os.path.exists(scan_path):
        print(f"错误：路径 ‘{scan_path}’不存在")
        sys.exit(1)
    if not os.path.isdir(scan_path):
        print(f"错误'{scan_path}'不是一个目录")
    print(f"\n开始扫描路径：{scan_path}\n")
    start_time = time.time()

    total_dirs,total_files,total_size = scan_with_state(scan_path)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"\n扫描完成！总耗时：{elapsed_time:.2f}秒")
    print(f"总计-目录：{total_dirs}，文件：{total_files}，总大小：{total_size}")
if __name__ == "__main__":
    main()