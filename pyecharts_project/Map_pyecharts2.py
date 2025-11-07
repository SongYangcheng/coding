# -*- coding: utf-8 -*-
"""
3D中国地图可视化示例
展示全国行政区划的3D地图，包含航线数据和交互效果
"""

from pyecharts import options as opts
from pyecharts.charts import Map3D
from pyecharts.globals import ChartType
from pathlib import Path
import os

# 配置常量
OUTPUT_DIR = 'html'
OUTPUT_FILE = 'map3d_china_enhanced.html'

# 地图配置常量
MAP_CONFIG = {
    'center': [104.114129, 37.550339],  # 中国地理中心
    'zoom': 1.0,
    'map_color': 'rgb(5,101,123)',
    'border_color': 'rgb(62,215,213)',
    'line_color': 'rgb(255, 255, 255)',
}

# 航线数据 - 代表中国主要城市的连接线
FLIGHT_DATA = [
    # 北京-上海航线
    [[116.407396, 39.904200, 1000], [121.473701, 31.230416, 1000]],
    # 上海-广州航线
    [[121.473701, 31.230416], [113.264385, 23.129163]],
    # 北京-深圳航线
    [[116.407396, 39.904200], [114.057868, 22.543099]],
    # 成都-西安航线
    [[104.066801, 30.572815], [108.948024, 34.263161]],
    # 武汉-南京航线
    [[114.305393, 30.593099], [118.796877, 32.060255]],
    # 杭州-青岛航线
    [[120.155070, 30.274085], [120.382640, 36.067082]],
    # 沈阳-哈尔滨航线
    [[123.431472, 41.805698], [126.534967, 45.803775]],
]

def create_enhanced_3d_map():
    """
    创建增强版3D中国地图

    Returns:
        Map3D: 配置完成的3D地图对象
    """
    # 数据验证
    if not FLIGHT_DATA:
        raise ValueError("航线数据不能为空")

    # 创建地图实例
    map_3d = (
        Map3D()
        .add_schema(
            # 地图基础配置
            maptype="china",
            itemstyle_opts=opts.ItemStyleOpts(
                color=MAP_CONFIG['map_color'],
                opacity=0.8,  # 稍微降低不透明度以增强3D效果
                border_width=1.2,
                border_color=MAP_CONFIG['border_color'],
            ),

            # 3D标签配置
            map3d_label=opts.Map3DLabelOpts(
                is_show=True,
                text_style=opts.TextStyleOpts(
                    color="#ffffff",
                    font_size=14,
                    background_color="rgba(0,0,0,0.7)",  # 添加半透明背景
                    border_color="#ffffff",
                    border_width=1,
                ),
            ),

            # 鼠标悬停效果
            emphasis_label_opts=opts.LabelOpts(
                is_show=True,
                color="#ffff00",  # 高亮颜色
                font_size=16,
            ),

            # 光照配置 - 增强视觉效果
            light_opts=opts.Map3DLightOpts(
                main_color="#ffffff",
                main_intensity=1.5,  # 增加光照强度
                is_main_shadow=True,  # 启用阴影
                main_alpha=45,
                main_beta=20,
                ambient_intensity=0.4,  # 增加环境光
                ambient_color="#404040",  # 环境光颜色
            ),

            # 视角控制 - 更好的初始视角
            view_control_opts=opts.Map3DViewControlOpts(
                center=MAP_CONFIG['center'],
                alpha=60,  # 俯视角度
                beta=0,    # 旋转角度
                distance=120,  # 距离
                min_distance=80,
                max_distance=200,
                auto_rotate=True,  # 自动旋转
                auto_rotate_speed=2,  # 旋转速度
            ),

            # 后期特效 - 增强视觉冲击
            post_effect_opts=opts.Map3DPostEffectOpts(
                is_enable=True,
                bloom_intensity=0.3,  # 泛光效果
            ),

            # 实时光线追踪 (如果支持)
            realistic_material_opts=opts.Map3DRealisticMaterialOpts(
                # is_enable=True,
                roughness=0.8,
                metalness=0.2,
            ),

            # 3D线条效果配置
            post_effect_opts=opts.Lines3DEffectOpts(
                is_show=True,
                period=3,  # 动画周期
                trail_length=0.4,  # 尾迹长度
                trail_width=6,  # 尾迹宽度
                trail_opacity=0.8,  # 尾迹透明度
            ),
        )
        .add(
            series_name="主要航线",
            data_pair=FLIGHT_DATA,
            type_=ChartType.LINES3D,
            linestyle_opts=opts.LineStyleOpts(
                is_show=True,
                color=MAP_CONFIG['line_color'],
                opacity=0.9,
                width=3,
            ),
            # 注意：effect_opts 在 Map3D.add() 中不支持，应在 add_schema 中配置
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="中国3D航线地图",
                subtitle="主要城市间航线可视化",
                pos_left="center",
                pos_top="5%",
                title_textstyle_opts=opts.TextStyleOpts(
                    color="#ffffff",
                    font_size=24,
                    font_weight="bold",
                ),
                subtitle_textstyle_opts=opts.TextStyleOpts(
                    color="#cccccc",
                    font_size=14,
                ),
            ),

            # 视觉映射 - 添加高度图例
            visualmap_opts=opts.VisualMapOpts(
                is_show=True,
                type_="continuous",
                min_=0,
                max_=2000,
                range_color=["#00ff00", "#ffff00", "#ff0000"],  # 高度颜色渐变
                pos_right="5%",
                pos_bottom="10%",
                textstyle_opts=opts.TextStyleOpts(color="#ffffff"),
            ),

            # 工具提示增强
            tooltip_opts=opts.TooltipOpts(
                is_show=True,
                background_color="rgba(0,0,0,0.8)",
                border_color="#ffffff",
                border_width=1,
                textstyle_opts=opts.TextStyleOpts(
                    color="#ffffff",
                    font_size=12,
                ),
                formatter="""
                function(params) {
                    if (params.seriesType === 'lines3D') {
                        return '航线: ' + params.name;
                    }
                    return params.name + '<br/>数值: ' + params.value;
                }
                """,
            ),

            # 工具栏配置
            toolbox_opts=opts.ToolboxOpts(
                is_show=True,
                pos_right="5%",
                pos_top="10%",
                feature={
                    "saveAsImage": {
                        "type": "png",
                        "title": "保存为图片",
                        "backgroundColor": "#2c343c"
                    },
                    "restore": {"title": "重置"},
                    "dataZoom": {"title": {"zoom": "缩放", "back": "重置"}},
                },
            ),
        )
    )

    return map_3d

def main():
    """主函数"""
    try:
        print("开始生成增强版3D中国地图...")

        # 创建地图
        map_chart = create_enhanced_3d_map()

        # 确保输出目录存在
        output_dir = Path(OUTPUT_DIR)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / OUTPUT_FILE

        # 渲染并保存
        map_chart.render(str(output_file))

        print(f"✅ 3D地图生成成功！")
        print(f"📁 文件保存位置: {output_file.absolute()}")
        print(f"🌐 在浏览器中打开查看效果")

        # 尝试自动打开浏览器
        try:
            import webbrowser
            webbrowser.open(output_file.as_uri())
            print("🔗 已自动在浏览器中打开")
        except Exception:
            print("ℹ️  请手动在浏览器中打开上述文件路径")

    except Exception as e:
        print(f"❌ 生成地图失败: {e}")
        return False

    return True

if __name__ == "__main__":
    main()