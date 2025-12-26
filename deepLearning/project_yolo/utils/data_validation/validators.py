#验证逻辑
#职责：所有验证相关的函数
"""
本模块专注于数据集的验证部分，验证数据集是否符合模型需求规范要求】、、
包含以下几类验证：
1.data.yaml配置文件的加载与内容一致性检查
2，图像文件与对应标签文件存在性，一一对应关系检查
3，单个标签文件的格式，类别ID，归一化坐标范围检查
4，train/val/test划分之间是否出现重复图像（防止数据泄露）
所有函数均采用防御性编程风格，尽早发现问题
"""
import yaml
import logging
from pathlib import Path
from typing import List,Dict,Tuple
#从常量模块导入统一管理的配置项，避免魔法值散落
from utils.data_validation.constants import (
    IMG_EXTENSIONS,    #支持的图像文件后缀模式列表
    YOLO_SPLITS,       #标准划分名称：['train','val','test']
    DEFAULT_ENCODING,  #文件读取编码
    TaskType,          #任务类型枚举
    DETECTION_FIELDS,#目标检测格式每行所需的字段数(5:class_id,cx,cy,w,h)
    SEGMENTATION_MIN_FIELDS,#实例分割模式最小字段数
)

logger = logging.getLogger(__name__)

#1.YAML配置验证相关函数

def load_yaml_config(yaml_path) -> Dict:
    """
    安全加载并解析data.yaml配置文件
    :param yaml_path:
    :return:
    """

    if not yaml_path.exists():
        raise FileNotFoundError(f'配置文件不存在：{yaml_path}')

    try:
        with open(yaml_path,'r',encoding = DEFAULT_ENCODING) as f:
            config = yaml.safe_load(f)

        if not isinstance(config,dict):
            raise yaml.YAMLError('YAML文件不是有效的字典结构')
        return config

    except yaml.YAMLError as e:
        raise yaml.YAMLError(f'解析data.yaml失败：{e}')

def validate_yaml_content(config:Dict) -> Tuple[List[str],int]:
    """
    验证data.yaml中类别相关字段的合法性与一致性

    主要检查点：
    是否存在‘name’和‘nc’字段
    ‘name’是否为非空字符串列表
    ‘nc’是否为正整数
    Len（names）是否严格等于nc
    :param config: 由load_yaml_config返回的配置字典
    :return: Tuple[List[str],int]
    """
    names = config.get("names",[]) #从配置字典config中获取键为names的值，names对应data.yaml里的类别名称列表
    nc = config.get('nc',[]) #从配置字典config中获取键为nc，nc对应data.yaml里的类别名称列表

    if not names or not isinstance(names,List) or not all(isinstance(n,str) for n in names):
        raise ValueError("缺少'name'字段或格式不正确（应为非空字符串）")

    if not isinstance(nc,int) or nc <= 0:
        raise ValueError("缺少'nc'字段或其值无效（必须为大于零的整数）")

    if len(names) != nc:
        raise ValueError(f"类别数量不一致：names长度为{len(names)}，nc为{nc},两者必须相等")

    logger.info(f'YAML配置验证通过：共{nc}个类别，名称为{names}')
    return names,nc
#2.图像与标签文件验证相关函数
def get_image_paths(directory:Path):
    """
    递归获取指定目标下所有文件格式的图像文件路径
    :param directory:
    :return:
    """
    if not directory.exists():
        logger.warning(f'图像目录不存在：{directory}')
        return []

    images = []
    for ext in IMG_EXTENSIONS:
        images.extend(directory.glob(ext))

    if images:
        logger.info(f'目录{directory}下找到{len(images)}张图像')
    else:
        logger.warning(f"日录 {directory}下木找到任何图像文件")
    return images

def read_label_file(label_path: Path) -> List[str]:
    """    安全读取YOLO标签文件(, txt), 返回换行分割的字符串列表
        Args:
        Label_path(Path): 标签文件路径
        Returns:
        List[str]: 每行内容
    """
    try:
        with open(label_path, "r", encoding=DEFAULT_ENCODING) as f:
            return f.read().splitlines()
    except Exception as e:
        logger.error(f"读取标签文件失败;{label_path},计误:{e}")
        return []

def validate_label_content(
        lines:list[str],
        nc:int,
        task_type:str = TaskType.DETECTION
) -> Tuple[bool,str]:
    if not lines:
        return True,""
    for idx,line in enumerate(lines,1):
        parts = line.strip().split()
        if not parts:
            continue

        if task_type == TaskType.DETECTION:
            expected = DETECTION_FIELDS
            if len(parts) != expected:
                return False,f'第{idx}行：检测任务需要{expected}个字段（class x_center y_center w h）,实际{len(parts)}个'
        elif task_type == TaskType.SEGMENTATION:
            if len(parts) < SEGMENTATION_MIN_FIELDS or (len(parts) - 1) % 2 != 0:
                return False,f'第{idx}行：分割任务格式错误（class_id）后必须为偶数个坐标轴且至少三对坐标'

        try:
            class_id = int(parts[0])
            if not (0 <= class_id < nc):
                return False, f"第{idx}行:类别ID {class_id}超出合法他围 [8,{nc - 1}]"

            # 将坐标部分转为 float 并检查归一化商国
            coords = [float(x) for x in parts[1:]]
            if not all(0.0 <= x <= 1.0 for x in coords):
                return False, f"第{idx}行:存在坐标值超出归一化范围 [e.e,1.0]"
        except ValueError:
            return False, f"第{idx}行:包含无法转换为数值的字段(要求class_id 为整数,其会为浮点数)"

def validate_image_label_pair(
        img_path:Path,
        nc:int,
        task_type:str = TaskType.DETECTION
) -> Tuple[bool,str,List[str]]:
    """
    对单张图像及其对应标签文件进行完整性与格式验证
    :param img_path: 图像文件路径
    :param nc: 类别总数
    :param task_type: 任务类型
    :return: 是否合法
             错误信息
             标签文件内容行列表
    """
    label_path = img_path.parent.parent / 'labels' / (img_path.stem + '.txt')
    if not label_path.exists():
        return False,f'对应标签文件不存在：{label_path}',[]
    lines = read_label_file(label_path)
    is_valid,error_msg = validate_label_content(lines,nc,task_type)

    if not is_valid:
        return False,f'标签内容错误（{label_path}）：{error_msg}',lines


#3.数据集划分唯一性验证
def validate_split_uniqueness(config:Dict) -> Tuple[bool,Dict[str,List[str]]]:
    """
    # 检查train/val/test 三个划分之间是否出现图像文件名重复
    :param config: 已加载的data.yaml配置字典
    :return:Tuple[bool,Dict[str,List[str]]]
            整体是否通过验证
            重复详情字典，key为‘train-val’等，value为示例从夫文件名列表（最多前10个）
    """
    split_stems:Dict[str,set] = {} #等同于split_stems = {},中间部分是对这个变量内容的注释
    duplicates:Dict[str,List[str]] = {}

    #step1
    for split in YOLO_SPLITS:
        if split not in config or config[split] is None:
            logger.info(f'data.yaml中未定义{split}路径，跳过该划分检测')
            continue
        split_path = Path(config[split]).resolve()
        if not split_path.exists():
            logger.warning(f'{split}划分路径不存在：{split_path}')
            continue
        stems = {img.stem for ext in IMG_EXTENSIONS for img in split_path.glob(ext)}
        split_stems[split] = stems
        logger.info(f'{split.upper()}划分共收集到{len(stems)}张唯一图像')

    #step2：两两比较常见的三组划分
    comparison_pairs = [('train','val'),('train','test'),('val','test')]
    all_passed = True
    for s1,s2 in comparison_pairs:
        if s1 not in split_stems or s2 not in split_stems:
            continue

        common_stems = split_stems[s1].intersection(split_stems[s2])
        if common_stems:
            all_passed = False
            example_list = sorted(list(common_stems))[:10]
            duplicates[f'{s1}-{s2}'] = example_list
            logger.error(f'在{s1.upper()}和{s2.upper()}划分间发现{len(common_stems)}张从夫图片，示例：{example_list}')
    if all_passed:
        logger.info('数据集划分唯一性验证通过：train/val/test之间无重复图像')
    else:
        logger.error('数据集划分唯一性验证失败，存在跨划分重复图像，请立即处理！')

    return all_passed,duplicates

if __name__ == '__main__':
    import sys
    from pathlib import Path
    default_data_path = Path(f'实际路径，例如D:PythonProject3/Yoloserver_platform_project/data/train')
    data_path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_data_path
    images_dir = data_path / 'images'
    images_ = get_image_paths(images_dir)
    print(f'在{images_dir}下找到{len(images_)}张图片\n')

    if not images_:
        print('未找到任何图像文件，请检查路径是否正确')
        sys.exit(1)

    nc_assumed = 5
    invalid_count = 0
    print('正在逐张检查图片-标签对合法性...\n')
    for img_path in images_:
        is_valid,error_msg,_ = validate_image_label_pair(img_path,nc_assumed,TaskType)
        if not is_valid:
            print(f"x 不合法-{img_path.name}→{error_msg}")
            invalid_count += 1
        # else:
        # print(f"v Mit - {img_poth.nome}")

        print(f"\n验证完成")
        print(f"总图像数:{len(images_)}")
        print(f"验证通过:{len(images_) - invalid_count}")
        print(f"验证失败:{invalid_count}")

        if invalid_count == 0:
            print("\n恭喜!当前划分所有图像-标签对均合法!")
        else:
            print(f"\n发现{invalid_count}个问遇,请根据上方信息修复后重新训练。")