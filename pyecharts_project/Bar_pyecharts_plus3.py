#!/usr/bin/env python3
# 指定使用 Python3 解释器执行此脚本
"""
专门处理 migration_data/migr_imm3ctb.csv 数据并生成增长人数图表
修复版本 - 修复formatter格式化问题
"""

# 导入 pyecharts 的配置选项模块，用于设置图表的各种选项
from pyecharts import options as opts
# 导入柱状图类，用于创建柱状图表
from pyecharts.charts import Bar
# 导入主题类型，用于设置图表主题（如深色主题）
from pyecharts.globals import ThemeType
# 导入 JsCode 工具类，用于在 Python 中嵌入 JavaScript 代码
from pyecharts.commons.utils import JsCode
# 导入 pandas 库，用于数据处理和分析
import pandas as pd
# 导入 os 模块，用于文件和目录操作
import os


def process_migration_data(csv_file='./data/migr_imm3ctb.csv'):
    """
    处理 migr_imm3ctb.csv 数据

    返回:
        (dates, values) - 时间列表和数值列表
    """

    # 检查 CSV 文件是否存在
    if not os.path.exists(csv_file):
        # 如果文件不存在，打印错误信息
        print(f"错误: 找不到数据文件 {csv_file}")
        # 提示用户先运行下载数据的脚本
        print(f"请先运行: python download_migration_data.py")
        # 返回两个 None 值表示处理失败
        return None, None

    # 打印正在读取的文件路径
    print(f"正在读取数据: {csv_file}")

    try:
        # 使用 pandas 读取 CSV 文件
        # low_memory=False 参数防止在读取大文件时出现数据类型混淆的警告
        df = pd.read_csv(csv_file, low_memory=False)
        # 打印数据加载成功的信息，显示行数和列数
        print(f"✓ 数据加载成功: {df.shape[0]} 行 x {df.shape[1]} 列")

        # 显示 DataFrame 的原始列名（在清理之前）
        print(f"\n原始列名: {df.columns.tolist()}")

        # 清理列名 - 去除每个列名首尾的空格
        # 使用 str.strip() 方法去除空白字符
        df.columns = df.columns.str.strip()
        # 打印清理后的列名
        print(f"\n清理后的列名: {df.columns.tolist()}")

        # 创建一个空列表，用于存储识别出的年份列名
        year_columns = []
        # 遍历 DataFrame 的所有列名
        for col in df.columns:
            # 将列名转换为字符串并去除空格
            col_str = str(col).strip()
            # 检查列名是否是纯数字，并且在 2010-2025 年份范围内
            # isdigit() 检查字符串是否全部由数字组成
            if col_str.isdigit() and 2010 <= int(col_str) <= 2025:
                # 如果符合条件，将该列名添加到年份列表中
                year_columns.append(col_str)

        # 对年份列表进行排序，确保年份按时间顺序排列
        year_columns = sorted(year_columns)
        # 打印找到的年份数据列
        print(f"\n找到年份数据: {year_columns}")

        # 如果没有找到任何年份列，报错并返回
        if not year_columns:
            print("错误: 未找到年份数据列")
            return None, None

        # 筛选出 2015-2022 年的数据
        # range(2015, 2023) 生成 2015 到 2022 的数字序列
        # 只保留在 year_columns 中存在的年份
        target_years = [str(y) for y in range(2015, 2023) if str(y) in year_columns]
        # 打印将要使用的年份
        print(f"使用年份: {target_years}")

        # 如果目标年份列表为空，说明数据中没有 2015-2022 的数据
        if not target_years:
            print("错误: 2015-2022年份数据不可用")
            return None, None

        # 创建一个字典，用于存储每年的总数
        yearly_totals = {}
        # 遍历目标年份列表
        for year in target_years:
            # 将该年份列的所有数据转换为数字类型
            # errors='coerce' 参数表示无法转换的值将被设为 NaN
            values = pd.to_numeric(df[year], errors='coerce')
            # 计算该列所有数值的总和（NaN 值会被自动忽略）
            total = values.sum()
            # 将年份和对应的总数存入字典
            yearly_totals[year] = total

        # 打印每年的总数统计
        print(f"\n年度总数:")
        # 遍历字典，打印每年的数据
        for year, total in yearly_totals.items():
            # 使用 :,.0f 格式化数字，添加千分位分隔符
            print(f"  {year}: {total:,.0f}")

        # 计算年度增长（相对于前一年的变化）
        # 对年份进行排序，确保按时间顺序计算
        years = sorted(yearly_totals.keys())
        # 创建字典存储增长数据
        growth_data = {}

        # 使用 enumerate 遍历年份列表，同时获取索引和年份值
        for i, year in enumerate(years):
            # 如果是第一年（索引为0）
            if i == 0:
                # 第一年使用绝对值作为基准
                growth = yearly_totals[year]
            else:
                # 其他年份计算增长 = 当年总数 - 前一年总数
                growth = yearly_totals[year] - yearly_totals[years[i - 1]]
            # 将年份和增长值存入字典
            growth_data[year] = growth

        # 打印每年的增长数据
        print(f"\n年度增长:")
        for year, growth in growth_data.items():
            # 使用 :+,.0f 格式，+ 表示显示正负号，, 表示千分位分隔符
            print(f"  {year}: {growth:+,.0f}")

        # 将字典转换为列表，方便后续图表绘制
        # 提取所有年份作为 X 轴数据
        dates = list(growth_data.keys())
        # 提取所有增长值作为 Y 轴数据
        values = list(growth_data.values())

        # 返回处理好的日期列表和数值列表
        return dates, values

    # 捕获所有异常
    except Exception as e:
        # 打印错误信息
        print(f"错误: {e}")
        # 导入 traceback 模块用于打印详细的错误堆栈信息
        import traceback
        # 打印完整的异常堆栈追踪，帮助调试
        traceback.print_exc()
        # 返回 None 值表示处理失败
        return None, None


def create_chart(dates, values, output_file='html/增长人数图表.html'):
    """
    创建pyecharts柱状图
    """

    # 检查数据是否有效（不为空）
    if not dates or not values:
        # 如果数据无效，打印错误信息
        print("错误: 无有效数据")
        # 返回 None 表示创建失败
        return None

    # 计算 Y 轴的最小值和最大值，用于设置坐标轴范围
    min_val = min(values)  # 找出数值列表中的最小值
    max_val = max(values)  # 找出数值列表中的最大值
    # 计算 Y 轴最小值：如果最小值是负数，乘以1.2留出空间；如果是正数，乘以0.8
    y_min = int(min_val * 1.2) if min_val < 0 else int(min_val * 0.8)
    # 计算 Y 轴最大值：最大值乘以1.2，留出一些显示空间
    y_max = int(max_val * 1.2)

    # 打印图表生成的基本信息
    print(f"\n生成图表:")
    print(f"  数据点数: {len(dates)}")  # 打印数据点的个数
    print(f"  Y轴范围: {y_min:,} 到 {y_max:,}")  # 打印Y轴的范围

    # 创建柱状图对象
    bar = (
        # 初始化柱状图，设置初始配置
        Bar(init_opts=opts.InitOpts(
            width="1400px",  # 设置图表宽度为1400像素
            height="700px",  # 设置图表高度为700像素
            theme=ThemeType.DARK,  # 使用深色主题
            bg_color="#1e2139"  # 设置背景颜色为深蓝色
        ))
        # 添加 X 轴数据（年份列表）
        .add_xaxis(dates)
        # 添加 Y 轴数据系列
        .add_yaxis(
            "增长人数",  # 设置系列名称
            values,  # 传入数值数据
            category_gap="60%",  # 设置柱子之间的间距为60%，使柱子变细
            # 设置柱子的样式
            itemstyle_opts={
                "color": "rgb(255,105,180,0.9)",  # 设置柱子颜色为粉红色，透明度0.9
                "barBorderRadius": [2, 2, 2, 2],  # 设置柱子四个角的圆角半径
                "shadowColor": "rgb(108,80,243,0.9)",  # 设置阴影颜色为紫色
                "shadowBlur": 20,  # 设置阴影模糊程度
                "shadowOffsetX": 0,  # 设置阴影X轴偏移为0
                "shadowOffsetY": 3  # 设置阴影Y轴向下偏移3像素
            },
            # 设置柱子上的标签不显示
            label_opts=opts.LabelOpts(is_show=False),
        )
        # 设置全局配置选项
        .set_global_opts(
            # 设置标题配置
            title_opts=opts.TitleOpts(
                title="增长人数",  # 设置图表标题
                pos_left="center",  # 标题居中显示
                # 设置标题文字样式
                title_textstyle_opts=opts.TextStyleOpts(
                    color="#fff",  # 标题颜色为白色
                    font_size=20  # 标题字体大小为20
                )
            ),
            # 设置 X 轴配置
            xaxis_opts=opts.AxisOpts(
                type_="category",  # X轴类型为类目轴
                # 设置 X 轴标签样式
                axislabel_opts=opts.LabelOpts(
                    rotate=45,  # 标签旋转45度，避免重叠
                    color="#fff",  # 标签颜色为白色
                    font_size=12  # 标签字体大小为12
                ),
                # 设置 X 轴线样式
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#fff")  # 轴线颜色为白色
                ),
            ),
            # 设置 Y 轴配置
            yaxis_opts=opts.AxisOpts(
                name="人数",  # Y轴名称
                # 设置 Y 轴名称的文字样式
                name_textstyle_opts=opts.TextStyleOpts(color="#fff"),  # 名称颜色为白色
                # 设置 Y 轴标签样式
                axislabel_opts=opts.LabelOpts(
                    color="#fff",  # 标签颜色为白色
                    # 使用 JavaScript 代码格式化 Y 轴标签
                    # 这是修复的关键：使用 JsCode 而不是 Python 格式化字符串
                    formatter=JsCode("""
                        function(value) {
                            return value.toLocaleString('en-US');
                        }
                    """)  # toLocaleString 方法会自动添加千分位分隔符
                ),
                # 设置 Y 轴线样式
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#fff")  # 轴线颜色为白色
                ),
                # 设置 Y 轴分割线样式
                splitline_opts=opts.SplitLineOpts(
                    is_show=True,  # 显示分割线
                    # 设置分割线样式
                    linestyle_opts=opts.LineStyleOpts(
                        color="#3a3f5c",  # 分割线颜色为深灰色
                        opacity=0.5  # 分割线透明度为0.5
                    )
                ),
                min_=y_min,  # 设置 Y 轴最小值
                max_=y_max,  # 设置 Y 轴最大值
            ),
            # 设置图例配置
            legend_opts=opts.LegendOpts(
                pos_top="5%",  # 图例距离顶部5%
                pos_right="5%",  # 图例距离右侧5%
                # 设置图例文字样式
                textstyle_opts=opts.TextStyleOpts(color="#ea7ccc", font_size=14)  # 粉红色，字号14
            ),
            # 设置提示框配置
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",  # 触发类型为坐标轴触发
                axis_pointer_type="shadow",  # 指示器类型为阴影
                # 使用 JavaScript 代码自定义提示框格式
                # 这是修复的关键：使用 JsCode 进行格式化
                formatter=JsCode("""
                    function(params) {
                        var data = params[0];
                        return data.name + '<br/>' + 
                               data.seriesName + ': ' + 
                               data.value.toLocaleString('en-US');
                    }
                """)  # 显示：年份 + 换行 + 系列名: 数值（带千分位）
            ),
            # 设置数据区域缩放配置
            datazoom_opts=[
                # 添加滑动条型数据区域缩放组件
                opts.DataZoomOpts(
                    type_="slider",  # 类型为滑动条
                    range_start=0,  # 起始位置为0%
                    range_end=100,  # 结束位置为100%（显示全部数据）
                ),
                # 添加内置型数据区域缩放组件（鼠标滚轮缩放）
                opts.DataZoomOpts(
                    type_="inside",  # 类型为内置
                    range_start=0,  # 起始位置为0%
                    range_end=100,  # 结束位置为100%
                ),
            ],
        )
    )

    # 如果数据中包含2019年，添加高亮标记
    if '2019' in dates:
        # 找到2019年在列表中的索引位置
        idx = dates.index('2019')
        # 获取2019年的数值
        value_2019 = values[idx]

        # 设置系列配置，添加标记点
        bar.set_series_opts(
            # 配置标记点选项
            markpoint_opts=opts.MarkPointOpts(
                # 设置标记点数据
                data=[
                    # 创建一个标记点
                    opts.MarkPointItem(
                        coord=['2019', value_2019],  # 标记点坐标：X轴为'2019'，Y轴为对应的值
                        value=value_2019,  # 标记点的值
                        # 设置标记点样式
                        itemstyle_opts=opts.ItemStyleOpts(color="#ea7ccc")  # 标记点颜色为粉红色
                    )
                ],
                # 设置标记点标签样式
                label_opts=opts.LabelOpts(
                    color="#fff",  # 标签文字颜色为白色
                    font_size=12,  # 标签字体大小为12
                    background_color="#2c3142",  # 标签背景颜色为深灰色
                    border_color="#ea7ccc",  # 标签边框颜色为粉红色
                    border_width=2,  # 标签边框宽度为2像素
                    padding=10,  # 标签内边距为10像素
                    # 使用 JavaScript 代码格式化标签内容
                    # 这是修复的关键：使用 JsCode 格式化标记点标签
                    formatter=JsCode("""
                        function(params) {
                            return '2019\\n增长人数: ' + params.value.toLocaleString('en-US');
                        }
                    """)  # \\n 是换行符，显示为两行：2019 和 增长人数: xxx,xxx
                )
            )
        )

    # 将图表渲染并保存为 HTML 文件
    bar.render(output_file)
    # 打印图表生成成功的消息
    print(f"\n✓ 图表已生成: {output_file}")

    # 返回图表对象
    return bar


def main():
    """主函数"""
    # 打印分隔线
    print("=" * 70)
    # 打印程序标题
    print("移民数据增长图表生成器")
    # 打印数据来源说明
    print("专门处理: data/migr_imm3ctb.csv")
    # 打印分隔线
    print("=" * 70)

    # 处理数据
    # 打印提示信息
    print("\n正在处理数据...")
    # 调用数据处理函数，获取年份列表和数值列表
    dates, values = process_migration_data('./data/migr_imm3ctb.csv')

    # 检查数据是否处理成功
    if dates and values:
        # 生成图表
        # 打印提示信息
        print("\n正在生成图表...")
        # 调用图表创建函数
        create_chart(dates, values, '增长人数图表.html')

        # 显示统计信息
        # 打印统计信息标题
        print("\n" + "=" * 70)
        print("数据统计")
        print("=" * 70)
        # 打印时间范围：第一年到最后一年
        print(f"时间范围: {dates[0]} - {dates[-1]}")
        # 打印数据点的数量
        print(f"数据点数: {len(dates)}")
        # 打印增长统计信息
        print(f"\n增长统计:")
        # 打印最大增长值，+ 号表示显示正负号
        print(f"  最大增长: {max(values):+,.0f}")
        # 打印最小增长值
        print(f"  最小增长: {min(values):+,.0f}")
        # 打印平均增长值
        print(f"  平均增长: {sum(values) / len(values):+,.0f}")
        # 打印增长总和（所有年份增长值的总和）
        print(f"  增长总和: {sum(values):+,.0f}")

        # 计算更多统计量
        # 导入统计模块
        import statistics
        # 检查数据点是否超过1个（标准差需要至少2个数据点）
        if len(values) > 1:
            # 打印标准差，衡量数据的离散程度
            print(f"  标准差: {statistics.stdev(values):,.2f}")
            # 打印中位数，中间位置的值
            print(f"  中位数: {statistics.median(values):+,.0f}")

        # 找出最大和最小增长年份
        # 找到最大值在列表中的索引
        max_idx = values.index(max(values))
        # 找到最小值在列表中的索引
        min_idx = values.index(min(values))
        # 打印极值年份信息
        print(f"\n极值年份:")
        # 根据索引打印最大增长的年份和数值
        print(f"  最大增长年份: {dates[max_idx]} ({values[max_idx]:+,.0f})")
        # 根据索引打印最小增长的年份和数值
        print(f"  最小增长年份: {dates[min_idx]} ({values[min_idx]:+,.0f})")

        # 计算正负增长年份
        # 使用列表推导式筛选出所有正增长的年份
        positive_years = [d for d, v in zip(dates, values) if v > 0]
        # 使用列表推导式筛选出所有负增长的年份
        negative_years = [d for d, v in zip(dates, values) if v < 0]
        # 打印增长趋势信息
        print(f"\n增长趋势:")
        # 打印正增长年份的数量和列表
        print(f"  正增长年份: {len(positive_years)} 个 {positive_years if positive_years else '无'}")
        # 打印负增长年份的数量和列表
        print(f"  负增长年份: {len(negative_years)} 个 {negative_years if negative_years else '无'}")

        # 打印年度变化详情
        print(f"\n年度变化:")
        # 遍历所有年份
        for i in range(len(dates)):
            # 如果是第一年（基准年）
            if i == 0:
                # 打印基准年的信息
                print(f"  {dates[i]}: {values[i]:+15,.0f} (基准年)")
            else:
                # 计算相对于上一年的变化率（百分比）
                # 如果上一年的值为0，则变化率为0
                change_rate = ((values[i] - values[i - 1]) / abs(values[i - 1]) * 100) if values[i - 1] != 0 else 0
                # 打印该年份的数值和相对上年的变化率
                print(f"  {dates[i]}: {values[i]:+15,.0f} (较上年 {change_rate:+.1f}%)")

        # 显示所有年份的详细数据
        print(f"\n详细数据:")
        # 同时遍历年份和数值
        for date, value in zip(dates, values):
            # 计算该年份数值占总和的百分比
            percentage = (value / sum(values) * 100) if sum(values) != 0 else 0
            # 打印年份、数值和占比
            print(f"  {date}: {value:+15,.0f}  ({percentage:+.1f}% 占比)")

        # 打印完成信息
        print("\n" + "=" * 70)
        print(" 完成!")
        print("=" * 70)
        # 提示用户如何查看生成的图表
        print("请在浏览器中打开 '增长人数图表.html' 查看图表")
        # 打印使用提示
        print("\n提示:")
        print("  - 可以使用鼠标滚轮缩放")  # 提示可以用鼠标滚轮缩放图表
        print("  - 可以拖动下方滑块选择时间范围")  # 提示可以用滑块选择显示的时间范围
        print("  - 鼠标悬停查看详细数据")  # 提示鼠标悬停可以查看tooltip

    else:
        # 如果数据处理失败，打印错误信息
        print("\n" + "=" * 70)
        print(" 处理失败")
        print("=" * 70)
        # 打印可能的失败原因
        print("\n可能的原因:")
        print("  1. 数据文件不存在")
        print("  2. 数据格式不正确")
        print("  3. 缺少必要的年份列")
        # 打印解决方案建议
        print("\n解决方案:")
        print("  1. 运行: python download_migration_data.py")
        print("  2. 确保 migration_data/migr_imm3ctb.csv 存在")
        print("  3. 检查CSV文件是否损坏")


# Python 程序的入口点
# 当脚本被直接运行时（而不是被导入），执行 main 函数
if __name__ == "__main__":
    # 调用主函数
    main()