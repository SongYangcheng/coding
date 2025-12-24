import os
import json
import logging
import getpass
import platform
import socket
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

# 从数据验证模块导入分析器
from utils.data_validation.analyzers import SplitStatistics, ClassStatistics
from utils.data_validation.cleaners import InvalidSample

logger = logging.getLogger(__name__)

# 工具版本号，用于报告中显示
__version__ = "1.0.0"

# =============================================================================
# 1. 报告数据结构定义（使用 dataclass 进行序列化）
# =============================================================================

@dataclass
class ReportMeta:
    """
    报告元数据
    """
    run_id: str
    timestamp: str
    operator: str
    machine: str
    platform: str
    python_version: str
    tool_version: str


@dataclass
class ReportConfig:
    """
    数据校验配置参数
    """
    yaml_path: str
    mode: str                     # dataset_SAMPLE or FULL
    task_type: str                # detection / segmentation
    sample_ratio: float           # SAMPLE 模式下采样比例
    min_sample: int               # 最少采样数量
    output_charts: bool           # 是否输出统计图表
    delete_invalid: bool           # 是否删除非法样本


@dataclass
class ReportDatasetInfo:
    """
    数据集基础信息
    """
    nc: int
    classes: List[str]
    splits: Dict[str, Dict]


@dataclass
class ReportValidationResult:
    """
    数据校验结果
    """
    overall_passed: bool
    basic_validation: Dict
    uniqueness_validation: Dict


@dataclass
class ReportStatistics:
    """
    统计分析结果
    """
    splits: Dict[str, Dict]


@dataclass
class ReportActions:
    """
    执行动作记录
    """
    deleted_files: Dict[str, int]
    generated_charts: List[str]


# =============================================================================
# 2. 报告构建器（Builder 模式）
# =============================================================================

class ReportBuilder:
    """
    报告构建器，用于逐步构建完整 JSON 报告
    """

    def __init__(self, yaml_path: Path, mode: str, task_type: str):
        self.yaml_path = str(yaml_path)
        self.mode = mode
        self.task_type = task_type

        self.start_time = datetime.now()

        self.meta: Optional[ReportMeta] = None
        self.config: Optional[ReportConfig] = None
        self.dataset_info: Optional[ReportDatasetInfo] = None
        self.validation_result: Optional[ReportValidationResult] = None
        self.statistics: Dict[str, SplitStatistics] = {}
        self.actions: ReportActions = ReportActions(
            deleted_files={},
            generated_charts=[]
        )

        self._generate_meta_info()

    def _generate_meta_info(self) -> None:
        run_id = self.start_time.strftime("%Y%m%d_%H%M%S")
        timestamp = self.start_time.isoformat()

        try:
            operator = getpass.getuser()
        except Exception:
            operator = "unknown"

        try:
            machine = socket.gethostname()
        except Exception:
            machine = "unknown"

        platform_info = f"{platform.system()} {platform.release()}"
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

        self.meta = ReportMeta(
            run_id=run_id,
            timestamp=timestamp,
            operator=operator,
            machine=machine,
            platform=platform_info,
            python_version=python_version,
            tool_version=__version__
        )

    def set_config(
        self,
        sample_ratio: float = 0.1,
        min_sample: int = 20,
        output_charts: bool = True,
        delete_invalid: bool = False
    ) -> "ReportBuilder":
        self.config = ReportConfig(
            yaml_path=self.yaml_path,
            mode=self.mode,
            task_type=self.task_type,
            sample_ratio=sample_ratio,
            min_sample=min_sample,
            output_charts=output_charts,
            delete_invalid=delete_invalid
        )
        return self

    def set_dataset_info(
        self,
        nc: int,
        classes: List[str],
        splits_info: Dict[str, Dict[str, Any]]
    ) -> "ReportBuilder":
        splits = {}
        for split_name, info in splits_info.items():
            splits[split_name] = {
                "path": info.get("path"),
                "count": info.get("count"),
                "verified_count": info.get("verified_count", info.get("count"))
            }

        self.dataset_info = ReportDatasetInfo(
            nc=nc,
            classes=classes,
            splits=splits
        )
        return self

    def set_validation_result(
        self,
        basic_passed: bool,
        invalid_samples: List[InvalidSample],
        uniqueness_passed: bool,
        duplicates: Dict[str, List[str]]
    ) -> "ReportBuilder":
        invalid_samples_dict = [
            {
                "image_path": s.image_path,
                "label_path": s.label_path,
                "error_type": s.error_type,
                "error_message": s.error_message
            }
            for s in invalid_samples
        ]

        basic_validation = {
            "passed": basic_passed,
            "invalid_count": len(invalid_samples),
            "invalid_samples": invalid_samples_dict
        }

        uniqueness_validation = {
            "passed": uniqueness_passed,
            "duplicates": duplicates
        }

        self.validation_result = ReportValidationResult(
            overall_passed=basic_passed and uniqueness_passed,
            basic_validation=basic_validation,
            uniqueness_validation=uniqueness_validation
        )
        return self

    def set_statistics(
        self,
        statistics: Dict[str, SplitStatistics]
    ) -> "ReportBuilder":
        stats = {}
        for split_name, split_stats in statistics.items():
            class_stats_dict = {}
            for class_id, class_stat in split_stats.class_stats.items():
                class_stats_dict[class_id] = {
                    "class_name": class_stat.class_name,
                    "image_count": class_stat.image_count,
                    "instance_count": class_stat.instance_count,
                    "avg_area": class_stat.avg_area,
                    "std_area": class_stat.std_area,
                    "avg_aspect_ratio": class_stat.avg_aspect_ratio,
                    "std_aspect_ratio": class_stat.std_aspect_ratio,
                }

            stats[split_name] = {
                "total_images": split_stats.total_images,
                "total_instances": split_stats.total_instances,
                "class_stats": class_stats_dict
            }

        self.statistics = stats
        return self

    def set_actions(
        self,
        deleted_files: Optional[Dict[str, int]] = None,
        generated_charts: Optional[List[str]] = None
    ) -> "ReportBuilder":
        if deleted_files:
            self.actions.deleted_files = deleted_files
        if generated_charts:
            self.actions.generated_charts = generated_charts
        return self

    def build(self) -> "ValidationReport":
        if self.config is None:
            raise ValueError("配置未设置，请调用 set_config()")
        if self.dataset_info is None:
            raise ValueError("数据集信息未设置，请调用 set_dataset_info()")
        if self.validation_result is None:
            raise ValueError("校验结果未设置，请调用 set_validation_result()")

        duration = (datetime.now() - self.start_time).total_seconds()

        report = ValidationReport(
            meta=self.meta,
            config=self.config,
            dataset_info=self.dataset_info,
            validation_result=self.validation_result,
            statistics=self.statistics,
            actions=self.actions,
            duration_seconds=duration
        )

        logger.info(f"报告构建完成，耗时 {duration:.2f} 秒")
        return report


# =============================================================================
# 3. 报告对象
# =============================================================================

@dataclass
class ValidationReport:
    meta: ReportMeta
    config: ReportConfig
    dataset_info: ReportDatasetInfo
    validation_result: ReportValidationResult
    statistics: Dict[str, Dict]
    actions: ReportActions
    duration_seconds: float

    def save(self, output_path: Path):
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(asdict(self), f, ensure_ascii=False, indent=2)


# =============================================================================
# 4. 便捷函数
# =============================================================================

def create_simple_report(
    yaml_path: Path,
    mode: str,
    task_type: str,
    nc: int,
    classes: List[str],
    passed: bool,
    invalid_count: int = 0
) -> ValidationReport:
    builder = ReportBuilder(yaml_path, mode, task_type)
    builder.set_config()
    builder.set_dataset_info(nc, classes, splits_info={})
    builder.set_validation_result(
        basic_passed=passed,
        invalid_samples=[],
        uniqueness_passed=True,
        duplicates={}
    )
    return builder.build()


# =============================================================================
# 5. 示例运行
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("报告生成模块")
    print("=" * 60)

    builder = ReportBuilder(
        yaml_path=Path("data/data.yaml"),
        mode="FULL",
        task_type="detection"
    )

    builder.set_config(
        sample_ratio=0.1,
        min_sample=20,
        output_charts=True,
        delete_invalid=False
    )

    builder.set_dataset_info(
        nc=3,
        classes=["helmet", "head", "person"],
        splits_info={
            "train": {"path": "data/train", "count": 1000, "verified_count": 1000},
            "val": {"path": "data/val", "count": 200, "verified_count": 200}
        }
    )

    builder.set_validation_result(
        basic_passed=True,
        invalid_samples=[],
        uniqueness_passed=True,
        duplicates={}
    )

    report = builder.build()

    print(f"\n运行ID: {report.meta.run_id}")
    print(f"操作者: {report.meta.operator}")
    print(f"机器名: {report.meta.machine}")
    print(f"平台: {report.meta.platform}")
    print(f"Python: {report.meta.python_version}")
    print(f"耗时: {report.duration_seconds:.2f}s")
    print(f"验证结果: {'通过' if report.validation_result.overall_passed else '失败'}")

    output_path = Path("runs/data_validation/test_report.json")
    report.save(output_path)
    print(f"\n报告已保存至: {output_path}")
    print("=" * 60)
