#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
字符串工具模块

职责：
    提供字符串处理相关的工具函数，解决常见的格式化问题

功能：
    1. 中英文混排对齐（计算显示宽度、按宽度填充）
    2. 其他字符串格式化工具（可扩展）

使用场景：
    - 日志输出表格对齐
    - 终端输出美化
    - 报告生成格式化

使用示例：
    from string_utils import get_display_width, pad_to_width

    # 计算显示宽度
    width = get_display_width("你好hello")  # 返回 9

    # 按宽度填充
    text = pad_to_width("类别", 10)         # 返回 "类别      "
    text = pad_to_width("123", 8, 'right')  # 返回 "     123"
"""


# ============================================================
# 显示宽度计算
# ============================================================

def get_display_width(text: str) -> int:
    """
    计算字符串的实际显示宽度

    背景：
        在终端或等宽字体环境下，中文字符占 2 个字符宽度，
        英文字符占 1 个字符宽度。Python 的 format 按字符数对齐，
        会导致中英混排时无法对齐。此函数计算实际显示宽度。

    规则：
        - 中日韩统一表意文字（CJK）: 宽度 2
        - 中日韩标点符号: 宽度 2
        - 全角 ASCII、全角标点: 宽度 2
        - 其他字符（英文、数字、半角符号）: 宽度 1

    Args:
        text: 输入字符串

    Returns:
        实际显示宽度（整数）

    Examples:
        >>> get_display_width("hello")
        5
        >>> get_display_width("你好")
        4
        >>> get_display_width("hi你好")
        6
        >>> get_display_width("类别名称")
        8
    """
    width = 0
    for char in text:
        if _is_wide_char(char):
            width += 2
        else:
            width += 1
    return width


def _is_wide_char(char: str) -> bool:
    """
    判断字符是否为宽字符（占 2 个显示宽度）

    Args:
        char: 单个字符

    Returns:
        是否为宽字符
    """
    # 中日韩统一表意文字
    if '\u4e00' <= char <= '\u9fff':
        return True
    # 中日韩标点符号
    if '\u3000' <= char <= '\u303f':
        return True
    # 全角 ASCII、全角标点
    if '\uff00' <= char <= '\uffef':
        return True
    # 中日韩扩展 A
    if '\u3400' <= char <= '\u4dbf':
        return True
    # 中日韩扩展 B (需要代理对，这里简化处理)
    # 日文平假名
    if '\u3040' <= char <= '\u309f':
        return True
    # 日文片假名
    if '\u30a0' <= char <= '\u30ff':
        return True
    # 韩文音节
    if '\uac00' <= char <= '\ud7af':
        return True

    return False


# ============================================================
# 字符串填充对齐
# ============================================================

def pad_to_width(text: str, width: int, align: str = 'left') -> str:
    """
    将字符串填充到指定显示宽度

    基于 get_display_width 计算实际宽度后，用空格填充到目标宽度。
    支持左对齐和右对齐，正确处理中英文混排。

    Args:
        text: 输入字符串
        width: 目标显示宽度
        align: 对齐方式
            - 'left': 左对齐，右边填充空格（默认）
            - 'right': 右对齐，左边填充空格
            - 'center': 居中对齐，两边填充空格

    Returns:
        填充后的字符串

    Examples:
        >>> pad_to_width("hello", 10)
        'hello     '
        >>> pad_to_width("你好", 10)
        '你好      '
        >>> pad_to_width("123", 8, 'right')
        '     123'
        >>> pad_to_width("hi", 10, 'center')
        '    hi    '
    """
    current_width = get_display_width(text)
    padding = width - current_width

    # 已达到或超过目标宽度，直接返回
    if padding <= 0:
        return text

    # 根据对齐方式填充
    if align == 'right':
        return ' ' * padding + text
    elif align == 'center':
        left_pad = padding // 2
        right_pad = padding - left_pad
        return ' ' * left_pad + text + ' ' * right_pad
    else:  # left（默认）
        return text + ' ' * padding


# ============================================================
# 表格格式化工具
# ============================================================

def format_table_row(columns: list, widths: list, aligns: list = None) -> str:
    """
    格式化表格行

    将多列数据按指定宽度和对齐方式格式化为一行字符串。

    Args:
        columns: 列数据列表，如 ["ID", "名称", "数量"]
        widths: 各列宽度列表，如 [4, 12, 8]
        aligns: 各列对齐方式列表，如 ['left', 'left', 'right']
                默认全部左对齐

    Returns:
        格式化后的行字符串

    Example:
        >>> format_table_row(["1", "cat", "100"], [4, 10, 8], ['left', 'left', 'right'])
        '1    cat             100'
    """
    if aligns is None:
        aligns = ['left'] * len(columns)

    # 确保列表长度一致
    assert len(columns) == len(widths) == len(aligns), "列数、宽度数、对齐数必须一致"

    parts = []
    for col, width, align in zip(columns, widths, aligns):
        parts.append(pad_to_width(str(col), width, align))

    return ' '.join(parts)


def format_table_separator(widths: list, char: str = '-') -> str:
    """
    生成表格分隔线

    Args:
        widths: 各列宽度列表
        char: 分隔字符（默认 '-'）

    Returns:
        分隔线字符串

    Example:
        >>> format_table_separator([4, 10, 8])
        '------------------------'
    """
    total_width = sum(widths) + len(widths) - 1  # 加上列间空格
    return char * total_width


# ============================================================
# 模块测试入口
# ============================================================

if __name__ == "__main__":
    """
    模块测试

    用法：
        python string_utils.py
    """
    print("=== string_utils.py 模块测试 ===\n")

    # ----------------------------------------------------------
    # 测试显示宽度计算
    # ----------------------------------------------------------
    print("1. 测试 get_display_width()")
    test_cases = [
        ("hello", 5),
        ("你好", 4),
        ("hi你好", 6),
        ("类别名称", 8),
        ("ordinary_clothes", 16),
        ("反光衣", 6),
    ]

    for text, expected in test_cases:
        actual = get_display_width(text)
        status = "✓" if actual == expected else "✗"
        print(f"  {status} '{text}' -> {actual} (期望: {expected})")

    # ----------------------------------------------------------
    # 测试字符串填充
    # ----------------------------------------------------------
    print("\n2. 测试 pad_to_width()")

    print(f"  左对齐: '{pad_to_width('hello', 10)}'")
    print(f"  左对齐: '{pad_to_width('你好', 10)}'")
    print(f"  右对齐: '{pad_to_width('123', 10, 'right')}'")
    print(f"  居中:   '{pad_to_width('hi', 10, 'center')}'")

    # ----------------------------------------------------------
    # 测试表格格式化
    # ----------------------------------------------------------
    print("\n3. 测试表格格式化")

    # 定义列宽和对齐方式
    widths = [12, 20, 6, 12, 12]
    aligns = ['left', 'left', 'right', 'right', 'right']

    # 表头
    header = format_table_row(['ID', '类别名称', '实例数', '图像数', '均面积'], widths, aligns)
    separator = format_table_separator(widths)

    print(f"  {header}")
    print(f"  {separator}")

    # 数据行
    data = [
        ['0', 'head', '60', '12', '0.0065'],
        ['1', 'ordinary_clothes', '59', '15', '0.0266'],
        ['2', 'person', '116', '27', '0.0851'],
        ['3', 'ordinary', '59', '17', '0.0207'],
        ['4', 'ordinary', '86', '22', '0.0063'],
    ]

    for row in data:
        print(f"  {format_table_row(row, widths, aligns)}")

    print("\n测试完成！")