#定义常量
#职责：定义全局常量，避免魔法数字

"""
常量定义模块
定义数据集验证过程中使用的所有常量，包括
支持的图像格式
YOLO数据集划分名称
文件编码
日志前缀
"""
from requests.utils import DEFAULT_ACCEPT_ENCODING

#支持的图像文件扩展名
IMG_EXTENSIONS = ['*.jpg','*.jpeg','*.png','*.bmp','*.tiff','*.tif','*.webp']
#YOLO数据集划分标准
YOLO_SPLITS = ['train','val','test']

#默认文件编码
DEFAULT_ENCODING = 'UTF-8'

#验证模式
class ValidationMode:
    SAMPLE = 'SAMPLE' #采样验证
    FULL = 'FULL' #完整性验证

#人物类型
class TaskType:
    DETECTION = 'detection'
    SEGMENTATION = 'segmentation'

#YOLO标签格式要求
# YOLO 标签格式要求
# class_id:目标所属类别的索引(整数,从e开始)
# x_center:目标边界框中心点的归一化横坐标(浮点数,范围9~1)
# y_center:目标边界框中心点的归一化纵坐标(浮点数,范围9~1)
# width:目标边界框的归一化库纳杜(浮点数,范围9~1)
# heightL 目标边界框的归一化高度(浮点数,范围e~1)
DETECTION_FIELDS = 5   #单个目标标准信息必须包含的字段总数为5：class_id,x_center,y_center,width,height
# 实例分割标注的核心是用多边形轮廓描述目标,字段构成逻辑是:
# class_id(目标类别索引)(x,y)坐标对,每对坐标占2个字段
# 要形成闭合的多边形轮廓,至少需要3个顶点,对应3x2=6 个坐标字段,加Eclass_id后总数就是7
#（如果目标轮廓更复杂，定点数更多，字段总数会大于7，比如四个顶点对应1 + 4 * 2 = 9个字段）
SEGMENTATION_MIN_FIELDS = 7  #class_id + 至少3对坐标点
DEFAULT_SAMPLE_RATIO = 0.1 #默认采样比例,即10%验证集，90%训练集
DEFAULT_MIN_SAMPLES = 20 #该参数表示采样的最小样本数量阈值，即采样后得到的样本不能少于20个（避免数据集过小）
