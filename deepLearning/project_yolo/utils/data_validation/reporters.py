#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :reporters.py
# @Project   :yolo_server
# @Function  :
# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
报告生成模块

职责：
    生成数据集验证的 JSON 报告，记录验证过程的完整信息

报告内容：
    1. 元信息（时间、执行者、机器、版本）
    2. 配置信息（yaml路径、验证模式、任务类型）
    3. 数据集信息（类别数、类别名、各划分统计）
    4. 验证结果（通过/失败、无效样本、重复图像）
    5. 统计数据（类别分布、bbox面积、宽高比）
    6. 执行操作（删除的文件）
    7. 生成的图表
    8. 耗时信息

输出格式：
    JSON 文件，保存到 runs/data_validation/YYYYMMDD_HHMMSS/report.json

使用示例：
    from reporters import ReportBuilder, save_json_report

    builder = ReportBuilder()
    report = builder.build(result, config, deleted_info, chart_files)
    save_json_report(report, output_dir / "report.json")
"""

import os
import json
import logging
import getpass
import platform
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

from utils.data_validation.analyzers import SplitStatistics, ClassStatistics
from utils.data_validation.cleaners import InvalidSample

logger = logging.getLogger(__name__)

# 版本号
__version__ = "1.0.0"


# ============================================================
# 数据类：报告结构
# ============================================================

@dataclass
class ReportMeta:
    """
    报告元信息

    记录报告生成的基本信息，用于追溯和审计
    """
    run_id: str  # 运行ID（时间戳）
    timestamp: str  # 生成时间（ISO格式）
    operator: str  # 执行者（用户名）
    machine: str  # 机器名
    platform: str  # 操作系统
    python_version: str  # Python 版本
    tool_version: str  # 工具版本


@dataclass
class ReportConfig:
    """
    报告配置信息

    记录本次验证使用的配置参数
    """
    yaml_path: str  # 配置文件路径
    mode: str  # 验证模式 (SAMPLE/FULL)
    task_type: str  # 任务类型 (detection/segmentation)
    sample_ratio: float  # 采样比例
    min_samples: int  # 最小采样数
    output_charts: bool  # 是否生成图表
    delete_invalid: bool  # 是否删除无效文件


@dataclass
class ReportDatasetInfo:
    """
    数据集信息

    记录数据集的基本结构
    """
    nc: int  # 类别数量
    classes: List[str]  # 类别名称列表
    splits: Dict[str, Dict]  # 各划分信息 {"train": {"path": "...", "count": 100}}


@dataclass
class ReportValidationResult:
    """
    验证结果

    记录验证的通过/失败情况
    """
    overall_passed: bool  # 总体是否通过
    basic_validation: Dict  # 基础验证结果
    uniqueness_validation: Dict  # 唯一性验证结果


@dataclass
class ReportStatistics:
    """
    统计数据

    记录各划分的详细统计信息
    """
    splits: Dict[str, Dict]  # 各划分统计 {"train": {...}, "val": {...}}


@dataclass
class ReportActions:
    """
    执行的操作

    记录验证过程中执行的操作（如删除文件）
    """
    deleted_files: Dict[str, int]  # 删除的文件数 {"images": n, "labels": m}
    generated_charts: List[str]  # 生成的图表文件名


# ============================================================
# 报告构建器
# ============================================================

class ReportBuilder:
    """
    报告构建器

    负责收集验证过程的各类信息，构建完整的 JSON 报告

    Example:
        builder = ReportBuilder()
        report = builder.build(result, config, deleted_info, chart_files)
    """

    def __init__(self, logger_instance: logging.Logger = None):
        """
        初始化报告构建器

        Args:
            logger_instance: 日志实例
        """
        self.logger = logger_instance or logger

    def build(
            self,
            result: Any,  # ValidationResult
            config: Any,  # ValidationConfig
            deleted_info: Dict[str, int] = None,
            chart_files: Dict[str, Path] = None
    ) -> Dict:
        """
        构建完整报告

        Args:
            result: 验证结果对象 (ValidationResult)
            config: 验证配置对象 (ValidationConfig)
            deleted_info: 删除文件统计 {"images": n, "labels": m}
            chart_files: 生成的图表 {"name": Path}

        Returns:
            完整的报告字典，可直接序列化为 JSON
        """
        self.logger.info("开始构建验证报告...")

        deleted_info = deleted_info or {}
        chart_files = chart_files or {}

        report = {
            "meta": self._build_meta(),
            "config": self._build_config(config),
            "dataset_info": self._build_dataset_info(result),
            "validation_result": self._build_validation_result(result),
            "statistics": self._build_statistics(result),
            "actions": self._build_actions(deleted_info, chart_files),
            "duration_seconds": result.duration_seconds
        }

        self.logger.info("报告构建完成")
        return report

    def _build_meta(self) -> Dict:
        """构建元信息"""
        now = datetime.now()

        return {
            "run_id": now.strftime("%Y%m%d_%H%M%S"),
            "timestamp": now.isoformat(),
            "operator": self._get_operator(),
            "machine": platform.node(),
            "platform": f"{platform.system()} {platform.release()}",
            "python_version": platform.python_version(),
            "tool_version": __version__
        }

    def _get_operator(self) -> str:
        """获取执行者用户名"""
        try:
            return getpass.getuser()
        except Exception:
            return os.environ.get("USER", os.environ.get("USERNAME", "unknown"))

    def _build_config(self, config: Any) -> Dict:
        """构建配置信息"""
        return {
            "yaml_path": str(config.yaml_path),
            "mode": config.mode,
            "task_type": config.task_type,
            "sample_ratio": config.sample_ratio,
            "min_samples": config.min_samples,
            "output_charts": config.output_charts,
            "delete_invalid": config.delete_invalid
        }

    def _build_dataset_info(self, result: Any) -> Dict:
        """构建数据集信息"""
        return {
            "nc": result.nc,
            "classes": result.class_names,
            "splits": result.splits_info
        }

    def _build_validation_result(self, result: Any) -> Dict:
        """构建验证结果"""
        # 基础验证结果
        basic_validation = {
            "passed": result.passed,
            "invalid_count": len(result.invalid_samples),
            "invalid_samples": [
                {
                    "image": str(sample.image_path),
                    "label": str(sample.label_path),
                    "error": sample.error_message
                }
                for sample in result.invalid_samples[:50]  # 最多记录50个
            ]
        }

        if len(result.invalid_samples) > 50:
            basic_validation["truncated"] = True
            basic_validation["total_invalid"] = len(result.invalid_samples)

        # 唯一性验证结果
        uniqueness_validation = {
            "passed": result.uniqueness_passed,
            "duplicates": {
                key: samples[:20]  # 每组最多记录20个
                for key, samples in result.duplicates.items()
            } if result.duplicates else {}
        }

        return {
            "overall_passed": result.passed and result.uniqueness_passed,
            "basic_validation": basic_validation,
            "uniqueness_validation": uniqueness_validation
        }

    def _build_statistics(self, result: Any) -> Dict:
        """构建统计数据"""
        statistics = {}

        for split_name, stats in result.split_stats.items():
            split_stat = {
                "total_images": stats.total_images,
                "total_instances": stats.total_instances,
                "class_distribution": {}
            }

            # 各类别统计
            for class_id, cs in stats.class_stats.items():
                split_stat["class_distribution"][cs.class_name] = {
                    "class_id": class_id,
                    "instance_count": cs.instance_count,
                    "image_count": cs.image_count,
                    "avg_bbox_area": round(cs.avg_area, 6),
                    "avg_aspect_ratio": round(cs.avg_aspect_ratio, 4),
                    "min_bbox_area": round(min(cs.bbox_areas), 6) if cs.bbox_areas else 0,
                    "max_bbox_area": round(max(cs.bbox_areas), 6) if cs.bbox_areas else 0,
                    "min_aspect_ratio": round(min(cs.bbox_aspect_ratios), 4) if cs.bbox_aspect_ratios else 0,
                    "max_aspect_ratio": round(max(cs.bbox_aspect_ratios), 4) if cs.bbox_aspect_ratios else 0,
                }

            statistics[split_name] = split_stat

        return statistics

    def _build_actions(
            self,
            deleted_info: Dict[str, int],
            chart_files: Dict[str, Path]
    ) -> Dict:
        """构建执行的操作"""
        return {
            "deleted_files": {
                "images": deleted_info.get("images", 0),
                "labels": deleted_info.get("labels", 0)
            },
            "generated_charts": [
                str(path.name) for path in chart_files.values()
            ] if chart_files else []
        }


# ============================================================
# 报告保存函数
# ============================================================

def save_json_report(
        report: Dict,
        output_path: Path,
        indent: int = 2,
        ensure_ascii: bool = False,
        logger_instance: logging.Logger = None
) -> Path:
    """
    保存 JSON 报告到文件

    Args:
        report: 报告字典
        output_path: 输出文件路径（如 runs/.../report.json）
        indent: JSON 缩进空格数
        ensure_ascii: 是否转义非 ASCII 字符（False 保留中文）
        logger_instance: 日志实例

    Returns:
        保存的文件路径

    Example:
        save_json_report(report, Path("runs/report.json"))
    """
    log = logger_instance or logger

    # 确保父目录存在
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 写入 JSON 文件
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=indent, ensure_ascii=ensure_ascii)

    log.info(f"报告已保存: {output_path}")
    return output_path


def load_json_report(
        report_path: Path,
        logger_instance: logging.Logger = None
) -> Optional[Dict]:
    """
    加载 JSON 报告

    Args:
        report_path: 报告文件路径
        logger_instance: 日志实例

    Returns:
        报告字典，加载失败返回 None
    """
    log = logger_instance or logger

    try:
        with open(report_path, 'r', encoding='utf-8') as f:
            report = json.load(f)
        log.info(f"报告已加载: {report_path}")
        return report
    except Exception as e:
        log.error(f"加载报告失败: {e}")
        return None


# ============================================================
# 便捷函数
# ============================================================

def generate_report(
        result: Any,
        config: Any,
        output_dir: Path,
        deleted_info: Dict[str, int] = None,
        chart_files: Dict[str, Path] = None,
        logger_instance: logging.Logger = None
) -> Path:
    """
    一键生成并保存报告

    便捷函数，封装 ReportBuilder + save_json_report

    Args:
        result: 验证结果对象
        config: 验证配置对象
        output_dir: 输出目录（report.json 将保存在此目录下）
        deleted_info: 删除文件统计
        chart_files: 生成的图表文件
        logger_instance: 日志实例

    Returns:
        报告文件路径

    Example:
        report_path = generate_report(result, config, Path("runs/20251221"))
    """
    log = logger_instance or logger

    # 构建报告
    builder = ReportBuilder(logger_instance=log)
    report = builder.build(result, config, deleted_info, chart_files)

    # 保存报告
    report_path = Path(output_dir) / "report.json"
    save_json_report(report, report_path, logger_instance=log)

    return report_path


# ============================================================
# 模块测试入口
# ============================================================

if __name__ == "__main__":
    """
    模块测试

    使用模拟数据测试报告生成功能
    """
    from pathlib import Path
    from dataclasses import dataclass, field
    from typing import List, Dict

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    print("=== reporters.py 模块测试 ===\n")


    # ----------------------------------------------------------
    # 模拟数据
    # ----------------------------------------------------------

    @dataclass
    class MockClassStats:
        class_id: int
        class_name: str
        instance_count: int
        image_count: int
        bbox_areas: List[float]
        bbox_aspect_ratios: List[float]

        @property
        def avg_area(self):
            return sum(self.bbox_areas) / len(self.bbox_areas) if self.bbox_areas else 0

        @property
        def avg_aspect_ratio(self):
            return sum(self.bbox_aspect_ratios) / len(self.bbox_aspect_ratios) if self.bbox_aspect_ratios else 0


    @dataclass
    class MockSplitStats:
        split_name: str
        total_images: int
        total_instances: int
        class_stats: Dict = field(default_factory=dict)


    @dataclass
    class MockInvalidSample:
        image_path: Path
        label_path: Path
        error_message: str


    @dataclass
    class MockResult:
        passed: bool
        invalid_samples: List
        uniqueness_passed: bool
        duplicates: Dict
        split_stats: Dict
        splits_info: Dict
        nc: int
        class_names: List[str]
        duration_seconds: float


    @dataclass
    class MockConfig:
        yaml_path: Path
        mode: str
        task_type: str
        sample_ratio: float
        min_samples: int
        output_charts: bool
        delete_invalid: bool


    # 创建模拟统计数据
    train_stats = MockSplitStats("train", 100, 500)
    train_stats.class_stats = {
        0: MockClassStats(0, "cat", 200, 80, [0.05, 0.08, 0.03] * 50, [1.2, 0.8, 1.0] * 50),
        1: MockClassStats(1, "dog", 180, 70, [0.06, 0.10, 0.04] * 50, [1.1, 0.9, 1.2] * 50),
        2: MockClassStats(2, "bird", 120, 50, [0.02, 0.03, 0.01] * 30, [0.7, 0.6, 0.8] * 30),
    }

    val_stats = MockSplitStats("val", 20, 100)
    val_stats.class_stats = {
        0: MockClassStats(0, "cat", 40, 16, [0.05, 0.07] * 15, [1.1, 0.9] * 15),
        1: MockClassStats(1, "dog", 35, 14, [0.06, 0.09] * 12, [1.0, 1.1] * 12),
        2: MockClassStats(2, "bird", 25, 10, [0.02, 0.03] * 10, [0.7, 0.8] * 10),
    }

    # 创建模拟结果
    result = MockResult(
        passed=False,
        invalid_samples=[
            MockInvalidSample(Path("/data/train/images/bad1.jpg"), Path("/data/train/labels/bad1.txt"),
                              "标签文件不存在"),
            MockInvalidSample(Path("/data/train/images/bad2.jpg"), Path("/data/train/labels/bad2.txt"),
                              "类别ID超出范围"),
        ],
        uniqueness_passed=True,
        duplicates={},
        split_stats={"train": train_stats, "val": val_stats},
        splits_info={
            "train": {"path": "/data/train", "count": 100},
            "val": {"path": "/data/val", "count": 20}
        },
        nc=3,
        class_names=["cat", "dog", "bird"],
        duration_seconds=12.5
    )

    config = MockConfig(
        yaml_path=Path("/configs/data.yaml"),
        mode="FULL",
        task_type="detection",
        sample_ratio=0.1,
        min_samples=20,
        output_charts=True,
        delete_invalid=False
    )

    deleted_info = {"images": 0, "labels": 0}
    chart_files = {
        "class_distribution": Path("figures/class_distribution.png"),
        "bbox_area_histogram": Path("figures/bbox_area_histogram.png"),
    }

    # ----------------------------------------------------------
    # 生成报告
    # ----------------------------------------------------------

    OUTPUT_DIR = Path(r"C:\Users\Matri\Desktop\yolo_server\tests\test_figure")  # 当前目录

    builder = ReportBuilder()
    report = builder.build(result, config, deleted_info, chart_files)

    # 保存报告
    report_path = save_json_report(report, OUTPUT_DIR / "report.json")

    # ----------------------------------------------------------
    # 输出结果
    # ----------------------------------------------------------

    print(f"\n{'=' * 50}")
    print("报告已生成")
    print('=' * 50)
    print(f"文件路径: {report_path}")
    print(f"\n报告内容预览:")
    print(json.dumps(report, indent=2, ensure_ascii=False)[:2000])
    print("...")

    print("\n测试完成！")