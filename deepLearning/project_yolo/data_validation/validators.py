#验证逻辑
#职责：所有验证相关的函数
"""
本模块专注于数据集的验证"部分，只会打一个问题：“这个数据集合是否符合YOLO规范”"
包括：
1. data.yaml 配置文件的加载与内容的一致性检查
2. 图像文件与对应标签文件的存在性，--对应关系检查
3. 单个标签文件的格式，类别ID，归一化最表范围检查
4. train/val/test 划分之间是否出现重复的图像
所有的韩硕均采用防御性编程风格，确保在任何异常情况下都能给出明确的错误信息，便于用户定位和修复数据集中的问题。
"""
from email.mime import image
from matplotlib.pylab import f
from sympy import comp
import yaml  #用于处理yaml文件
import logging #日志模块
from pathlib import Path #路径处理模块
from typing import List, Dict, Tuple

#从常量模块导入统一的管理配置项，避免魔法值散落
from utils.constants import IMG_EXTENSIONS, YOLO_SPLITS, ValidationMode, TaskType, DETECTION_FIELDS, SEGMENTATION_FIELDS, DEFAULT_SAMPLE_RATIO, DEFULT_MIN_SAMPLE_COUNT, DEFAULT_FILE_ENCODING, SEGMENTATION_MIN_FIELDS

logger = logging.getLogger(__name__)  #配置模块级日志记录器
#===================配置yaml文件验证===================
def load_yaml_config(yaml_path: Path) -> Dict:
    """
    加载并验证data.yaml配置文件的内容
    为什么单独封装:
    - 职责单一：专注于yaml文件的加载与基本验证
    - 便于维护：如果yaml结构变化，只需修改此处
    参数：
        yaml_path (Path): data.yaml文件的路径
    return:
        Dict: 加载并验证后的配置字典
    例外：
        FileNotFoundError: 如果yaml文件不存在
        ValueError: 如果yaml内容不符合预期格式
    """
    if not yaml_path.exists():
        raise FileNotFoundError(f"配置文件未找到: {yaml_path}")
    
    try:
        with open(yaml_path, 'r', encoding=DEFAULT_FILE_ENCODING) as f:
            config = yaml.safe_load(f)
        
        if not isinstance(config, dict):
            raise yaml.YAMLError("配置文件格式错误，预期为字典结构")
        return config
    
    except yaml.YAMLError as e:
        #safe_load 已经捕获大部分错误，这里包装一层便于上层识别
        raise yaml.YAMLError(f"无法解析yaml文件: {e}")
    

def validate_yaml_content(config: Dict) -> Tuple[List[str], int]:
    """
    验证data.yaml中类别识别关键字合法性与一致性
    
    主要检查点：
    - 是否存在'names'关键字，且其值为非空列表
    - 是否存在'path'关键字，且其值为字符串
    参数：
        config (Dict): 通过load_yaml_config加载的配置字典
        return:
            Tuple[List[str], int]: 返回类别名称列表及类别总数
        Raises:
            ValueError: 如果关键字缺失或格式不正确,附带清洗错误描述

    """
    names = config.get("names", []) #类别名称列表, []表示默认值
    nc = config.get("nc", [])
    #isinstance 为类型检查函数，检查前面的names是否为List类型，且不为空，返回True/False
    if not names or not isinstance(names, list) or not all(isinstance(n, str) for n in names):
        raise ValueError("配置文件中'names'关键字缺失或格式不正确，预期为非空字符串列表")
    if not isinstance(nc, int) or nc != len(names):
        raise ValueError(f"配置文件中'nc'关键字缺失或与'names'长度不匹配，预期为{len(names)}")
    logger.info(f"配置文件验证通过，检测到{nc}个类别, 名称列表: {names}")
    return names, nc

#===================图像与标签文件验证===================
def get_image_paths(directory: Path):
    """ 
    递归获取指定目标下所有文件格式的图像文件路径

    Args:
    directory(Path):图像所在日录(如 data/train/images)
    Returns:
    List[Path]:匹配到的图像 Path 对象列表(无顺序保证)

    Note:
    若月录不存在则会记录警告并返回空列表,不会抛异常(便于上层继续处理其他划分)
    """

    if not directory.exists():
        logger.warning(f"图像目录不存在:{directory}")
        return []

    images = []
    for ext in IMG_EXTENSIONS: # #7 " *. jpg", " *. jpeg", " *. png"
        images.extend(directory.glob(ext))   #glob 方法用于递归查找匹配的文件路径
    if images:
        logger.info(f"目录 {directory} 下找到{len(images)}张图像")
    else:
        logger.warning(f"目录 {directory} 下未找到任何图像文件")
    return images

def read_label_file(label_path: Path) -> List[str]:
    """
    安全读取YOLO标签文件，返回换行分割的字符串列表
    Args:
        label_path (Path): 标签文件路径
    Returns:
        List[str]: 标签文件的每一行内容列表
    """
    try:
        with open(label_path, "r", encoding=DEFAULT_FILE_ENCODING) as f:
            lines = f.read().splitlines()
    except Exception as e:
        logger.error(f"无法读取标签文件 {label_path}: {e}")
        return []
    
def validate_label_content(
        lines: List[str],
        nc: int,
        task_type: str = TaskType.DETECTION
) -> Tuple[bool, str]:
    """核心标签内容格式验证函数
    检查内容包括：
    1. 子弹是否符合任务类型
    2. 类别ID是否在合法范围[0, nc-1]
    3. 所有坐标是否在[0.0, 1.0]范围内
    4. 所有字段是否正确转化为数据
    Args:
        line (List[str]): 标签文件中的一行，按空格分割后的字段列表
        nc (int): 类别总数
        task_type (str): 任务类型，支持目标检测和实例分割, 默认为目标检测
    Returns:
        Tuple[bool, str]: 验证结果及错误信息，若验证通过则返回(True, "")
    """
    if not lines: #空标签文件直接返回通过
        return True, ""
    for idx, line in enumerate(lines, 1): #从1开始计数
        parts = line.strip().split() #按空格分割字段
        if not parts:
            continue #跳过空行

        if task_type == TaskType.DETECTION:
            expected = DETECTION_FIELDS
            if len(parts) != expected:
                return False, f"第{idx}行字段数错误，预期为{expected}，实际为{len(parts)}"
        elif task_type == TaskType.SEGMENTATION:
            if len(parts) < SEGMENTATION_FIELDS:
                return False, f"第{idx}行字段数错误，实例分割模式下最少应为{SEGMENTATION_FIELDS}，实际为{len(parts)}"
    
    # 2.数值类型与范围检测
        
    try:
        class_id = int(parts[0])
        if not(0 <= class_id < nc):
            return False, f"第{idx}行类别ID {class_id} 超出范围 [0, {nc-1}]"
        coords = [float(p) for p in parts[1:]]
        if not all(0.0 <= c <= 1.0 for c in coords):
            return False, f"第{idx}行坐标值超出范围 [0.0, 1.0]"
    
    except ValueError:
        return False, f"第{idx}行包含无法转换为数字的字段"
    return True, ""

def validate_image_label_pair(
        image_path: Path,
        nc: int,
        task_type: str = TaskType.DETECTION
) -> Tuple[bool, str, List[str]]:
    """
    验证单个图像与其对应标签文件的存在性及标签内容格式
    Args:
        image_path (Path): 图像文件路径
        label_path (Path): 标签文件路径
        nc (int): 类别总数
        task_type (str): 任务类型，支持目标检测和实例分割, 默认为目标检测
    Returns:
        Tuple[bool, str]: 验证结果及错误信息，若验证通过则返回(True, "")
    """
    label_path = image_path.parent.parent / "labels" / image_path.parent.name / (image_path.stem + ".txt") #parent.parent:上两级目录， stem:不带扩展名的文件名

    if not label_path.exists():
        return False, f"标签文件不存在: {label_path}", []
    lines = read_label_file(label_path)
    is_valid, error_msg = validate_label_content(lines, nc, task_type)

    if not is_valid:
        return False, f"标签文件 {label_path} 内容格式错误: {error_msg}", lines
    return True, "", lines

#===================数据划分重复性验证===================
    
def validate_data_splits(config: Dict) -> Tuple[bool, Dict[str, List[str]]]:
    """
    检查train/val/test 三个划分之间是否出现图像文件名重复
    重复图会导致严重的数据泄露，使验证集/测试集的评估结果失去意义
    函数通过文件名stem比较， 即可高效检测大多数重复的情况
    Args:
        config (Dict): 通过load_yaml_config加载的配置字典
    Returns:
        Tuple[bool, Dict[str, List[str]]]: 验证结果及重复文件名详情，若无重复则返回(True, {})
        - 整体是否通过验证
        - 冲否详情字典，key为'train-val'等， value为示例重复文件名列表"""
    
    split_stems: Dict[str, set] = {} #存储每个划分的文件名stem集合
    duplicates: Dict[str, List[str]] = {} #存储重复文件名详情

    #step1: 收集每个有效的划分图像文件名
    for split in YOLO_SPLITS:
        if split not in config or config[split] is None:
            logger.info(f"配置文件中未定义划分 '{split}'，跳过该划分的重复性检查")
            continue

        split_path = Path(config[split].resovle()) #获取划分路径
        if not split_path.exists():
            #路径不存在测记录的警告日志并跳过
            logger.warning(f"划分路径不存在: {split_path}，跳过该划分的重复性检查")
            continue
        #遍历所有文件的图像拓展名，获取路径下所有图像文件，提取其stem并去重
        stems = {img.stem for ext in IMG_EXTENSIONS for img in split_path.glob(ext)} 
        #将当前划分的图像stem集合存入字典，便于后续的匹配标签未见
        split_stems[split] = stems
        logger.info(f"划分 '{split}' 下找到{len(stems)}张图像用于重复性检查")
    #step2: 检查划分之间的重复文件名
    comparisons = [("train", "val"), ("train", "test"), ("val", "test")]
    all_passed = True

    for s1, s2 in comparisons:
        if s1 not in split_stems and s2 not in split_stems:
            continue
        common_stems = split_stems[s1].intersection(split_stems[s2]) #求交集
        if common_stems:
            all_passed = False
            example_list = sorted(list(common_stems))[:10] #取前10个示例
            duplicates[f"{s1}-{s2}"] = example_list #存储重复详情
            logger.error(f"划分 '{s1}' 和 '{s2}' 之间存在重复图像文件名，共{len(common_stems)}个示例: {example_list}")
    if all_passed:
        logger.info("数据划分之间未发现重复的图像文件名")
    else:
        logger.error("数据划分之间存在重复的图像文件名，请修复后重新验证")
    return all_passed, duplicates


#===================直接运行时的检点测试入口(便于本地快速验证)===================

if __name__ == "__main__":
    """本地快速测试入口
    用于执行模块级的简单验证测试
    不建议在生产环境中使用"""
    import sys
    from pathlib import Path

    #默认数据据集路径
    default_data_path = Path(r"")
    #sys.argv 用于获取命令行参数,第一个参数为脚本名称，第二个参数为数据集路径
    #sys.argv[1]表示用户传入的数据集路径， argv表示参数列表
    data_path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_data_path
    print(f"使用数据集路径: {data_path}")

    images_dir = data_path / "images"
    images_ = get_image_paths(images_dir)
    print(f"在目录 {images_dir} 下找到 {len(images_)} 张图像")

    if not images_:
        print("未找到任何图像文件，退出测试")
        sys.exit(1)  #退出代码1表示异常终止
    
    #这里假设类别总数为5
    nc_assumed = 5
    invalid_count = 0
    print("重在逐张检测图像-标签的合法性...")
    for img_path in images_:
        is_valid, error_msg, _ = validate_image_label_pair(img_path, nc_assumed, TaskType.DETECTION)
        if not is_valid:
            invalid_count += 1
            print(f"图像 {img_path} 验证失败: {error_msg}")

    
    print(f"验证完成，共发现 {invalid_count} 个无效的图像-标签对")


    