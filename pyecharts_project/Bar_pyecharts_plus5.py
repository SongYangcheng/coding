# Pyecharts 区域缩放组件使用示例 - 完全修复版
# ================================================
# 功能说明：
#   1. 演示区域缩放组件的使用（滑动条 + 内置缩放）
#   2. 标题和副标题的配置
#   3. 图例、坐标轴的样式设置
#   4. 标记线和标记点的使用
#   5. 数据标签的控制

# ================================================
# """

# ============================================================================
# 导入依赖库
# ============================================================================
from pyecharts.charts import Bar  # 绘制条形图（柱状图）的模块
from pyecharts import options as opts  # 配置项模块（简写为 opts）
from pyecharts.faker import Faker  # 用于生成假数据（测试用）
from pyecharts.globals import ThemeType  # 主题配置项


# ============================================================================
# 创建柱状图
# ============================================================================
bar = (
    # 步骤1：初始化柱状图对象
    Bar(
        init_opts=opts.InitOpts(  # 初始化配置（注意：是 InitOpts 不是 InitialOptions）
            theme=ThemeType.LIGHT  # 使用浅色主题（注意：是 ThemeType.LIGHT）
        )
    )
    
    # 步骤2：添加 X 轴数据
    .add_xaxis(
        Faker.days_attrs  # 使用 Faker 生成日期数据（注意：是 days_attrs）
    )
    
    # 步骤3：添加 Y 轴数据（系列数据）
    .add_yaxis(
        series_name='商家A',  # 系列名称
        y_axis=Faker.days_values,  # Y轴数据（注意：是 days_values）
        category_gap='60%'  # 柱子之间的间距（占类目宽度的百分比）
    )
    
    # 步骤4：设置全局配置项
    .set_global_opts(
        # ===== 区域缩放组件配置 =====
        datazoom_opts=[  # 使用列表，可以配置多个缩放组件
            opts.DataZoomOpts(),  # 滑动条缩放（默认在底部）
            opts.DataZoomOpts(type_="inside")  # 内置缩放（鼠标滚轮）
        ],
        
        # ===== 标题配置 =====
        title_opts=opts.TitleOpts(
            title='区域缩放组件的使用',  # 主标题内容
            pos_left='center',  # 标题位置：居中
            # 主标题字体样式
            title_textstyle_opts=opts.TextStyleOpts(
                color='#fc97af',  # 字体颜色：粉红色
                font_size=26  # 字体大小：26号
            ),
            subtitle='这是副标题',  # 副标题内容
            # 副标题字体样式
            subtitle_textstyle_opts=opts.TextStyleOpts(
                color='cyan',  # 字体颜色：青色
                font_size=14  # 字体大小：14号
            )
        ),
        
        # ===== 图例配置 =====
        legend_opts=opts.LegendOpts(
            pos_top='12%'  # 图例位置：距离顶部12%
        ),
        
        # ===== X轴配置 =====
        xaxis_opts=opts.AxisOpts(
            name='我是x轴',  # X轴名称
            # X轴名称样式
            name_textstyle_opts=opts.TextStyleOpts(
                color='cyan'  # 名称颜色：青色
            )
        ),
        
        # ===== Y轴配置 =====
        yaxis_opts=opts.AxisOpts(
            name='我是y轴',  # Y轴名称
            # Y轴名称样式
            name_textstyle_opts=opts.TextStyleOpts(
                color='cyan'  # 名称颜色：青色
            )
        )
    )
    
    # 步骤5：设置系列配置项
    .set_series_opts(
        # ===== 标记线配置 =====
        markline_opts=opts.MarkLineOpts(
            data=[  # 标记线数据
                opts.MarkLineItem(type_='max', name='最大值'),  # 最大值标记线
                opts.MarkLineItem(type_='min', name='最小值'),  # 最小值标记线
                opts.MarkLineItem(type_='average', name='平均值')  # 平均值标记线
            ]
        ),
        
        # ===== 标记点配置 =====
        markpoint_opts=opts.MarkPointOpts(
            data=[  # 标记点数据
                opts.MarkPointItem(type_='max', name='最大值'),  # 最大值标记点
                opts.MarkPointItem(type_='min', name='最小值')  # 最小值标记点
            ]
        ),
        
        # ===== 数据标签配置 =====
        label_opts=opts.LabelOpts(
            is_show=False  # 不显示数据标签（柱子上的数值）
        )
    )
)


# ============================================================================
# 渲染图表
# ============================================================================
# 将图表渲染为 HTML 文件
# bar.render("区域缩放示例.html")

# # 打印成功信息
# print("✅ 图表生成成功！")
# print("📁 文件名: 区域缩放示例.html")
# print("🌐 请用浏览器打开查看")
# print("\n💡 使用说明:")
# print("  1. 拖动底部滑动条可以缩放查看不同日期范围")
# print("  2. 鼠标滚轮可以在图表区域内缩放")
# print("  3. 图表上的红点表示最大值和最小值")
# print("  4. 图表中的横线表示最大值、最小值和平均值")




# 程序2：
import pandas as pd  # 导入pandas库，用于数据处理和读取Excel文件
from pyecharts.charts import Bar  # 从pyecharts图表模块导入柱状图类
from pyecharts import options as opts  # 导入pyecharts的配置选项模块，用于设置图表的各种参数
from pyecharts.globals import ThemeType  # 导入主题类型，用于设置图表主题风格

# 读取Excel数据
data = pd.read_excel('./data/奖牌.xlsx')  # 使用pandas读取Excel文件，将数据存储到data变量中

# 提取最近五届奥运会的数据
dt1 = data.loc[:, ['赛事', '金牌']].values.tolist()[-5:]  # 从data中提取"赛事"和"金牌"两列，转换为列表，取最后5条数据（最近五届）
dt2 = data.loc[:, ['赛事', '银牌']].values.tolist()[-5:]  # 从data中提取"赛事"和"银牌"两列，转换为列表，取最后5条数据
dt3 = data.loc[:, ['赛事', '铜牌']].values.tolist()[-5:]  # 从data中提取"赛事"和"铜牌"两列，转换为列表，取最后5条数据

# 创建柱状图
c = (  # 使用链式调用的方式创建和配置柱状图对象
    Bar(  # 实例化一个柱状图对象
        init_opts=opts.InitOpts(  # 初始化配置选项
            theme=ThemeType.LIGHT,  # 设置图表主题为浅色主题
            bg_color='#FFFFFF'  # 设置图表背景颜色为白色
        )
    )
    .add_xaxis([i[0] for i in dt1])  # 添加X轴数据，从dt1中提取每个子列表的第一个元素（赛事名称），作为X轴的类目

    # 金牌系列
    .add_yaxis(  # 添加Y轴数据系列（金牌）
        "金牌",  # 系列名称，会显示在图例中
        [i[1] for i in dt1],  # Y轴数据，从dt1中提取每个子列表的第二个元素（金牌数量）
        category_gap="30%",  # 设置同一类目中柱子之间的距离，占类目宽度的30%
        itemstyle_opts={  # 使用字典形式配置柱子的样式选项
            "color": '#4e70f0',  # 设置金牌柱子的颜色为蓝色
            "borderRadius": [2, 2, 0, 0],  # 设置柱子的圆角，数组表示[左上, 右上, 右下, 左下]，这里只给顶部设置2px圆角
            "opacity": 1  # 设置柱子的透明度为1（完全不透明）
        },
        emphasis_opts=opts.EmphasisOpts(  # 设置鼠标悬停时的高亮效果
            itemstyle_opts={  # 使用字典形式配置高亮时的样式
                "shadowBlur": 10,  # 设置阴影的模糊程度为10像素
                "shadowOffsetX": 4,  # 设置阴影在X轴方向的偏移量为4像素
                "shadowOffsetY": 4,  # 设置阴影在Y轴方向的偏移量为4像素
                "shadowColor": 'rgba(78, 112, 240, .5)'  # 设置阴影颜色为半透明的蓝色
            }
        )
    )

    # 银牌系列
    .add_yaxis(  # 添加Y轴数据系列（银牌）
        "银牌",  # 系列名称，会显示在图例中
        [i[1] for i in dt2],  # Y轴数据，从dt2中提取每个子列表的第二个元素（银牌数量）
        category_gap="30%",  # 设置同一类目中柱子之间的距离，占类目宽度的30%
        itemstyle_opts={  # 使用字典形式配置柱子的样式选项
            "color": '#00c5d2',  # 设置银牌柱子的颜色为青色
            "borderRadius": [2, 2, 0, 0],  # 设置柱子的圆角，只给顶部设置2px圆角
            "opacity": 1  # 设置柱子的透明度为1（完全不透明）
        },
        emphasis_opts=opts.EmphasisOpts(  # 设置鼠标悬停时的高亮效果
            itemstyle_opts={  # 使用字典形式配置高亮时的样式
                "shadowBlur": 10,  # 设置阴影的模糊程度为10像素
                "shadowOffsetX": 4,  # 设置阴影在X轴方向的偏移量为4像素
                "shadowOffsetY": 4,  # 设置阴影在Y轴方向的偏移量为4像素
                "shadowColor": 'rgba(0, 197, 210, .5)'  # 设置阴影颜色为半透明的青色
            }
        )
    )

    # 铜牌系列
    .add_yaxis(  # 添加Y轴数据系列（铜牌）
        "铜牌",  # 系列名称，会显示在图例中
        [i[1] for i in dt3],  # Y轴数据，从dt3中提取每个子列表的第二个元素（铜牌数量）
        category_gap="30%",  # 设置同一类目中柱子之间的距离，占类目宽度的30%
        itemstyle_opts={  # 使用字典形式配置柱子的样式选项
            "color": '#ffce2b',  # 设置铜牌柱子的颜色为黄色
            "borderRadius": [2, 2, 0, 0],  # 设置柱子的圆角，只给顶部设置2px圆角
            "opacity": 1  # 设置柱子的透明度为1（完全不透明）
        },
        emphasis_opts=opts.EmphasisOpts(  # 设置鼠标悬停时的高亮效果
            itemstyle_opts={  # 使用字典形式配置高亮时的样式
                "shadowBlur": 10,  # 设置阴影的模糊程度为10像素
                "shadowOffsetX": 4,  # 设置阴影在X轴方向的偏移量为4像素
                "shadowOffsetY": 4,  # 设置阴影在Y轴方向的偏移量为4像素
                "shadowColor": 'rgba(255, 206, 43, .5)'  # 设置阴影颜色为半透明的黄色
            }
        )
    )

    .set_series_opts(  # 设置系列的全局配置选项
        label_opts=opts.LabelOpts(position="top")  # 设置数据标签的位置为柱子顶部，显示具体数值
    )

    .set_global_opts(  # 设置图表的全局配置选项
        title_opts=opts.TitleOpts(  # 配置图表标题
            title='历年奥运会中国奖牌数量统计柱形图',  # 设置主标题文字
            pos_left='center',  # 设置标题水平位置为居中
            pos_top='2%'  # 设置标题距离顶部的距离为2%
        ),
        legend_opts=opts.LegendOpts(pos_top='7%'),  # 配置图例，设置图例距离顶部的距离为7%
        xaxis_opts=opts.AxisOpts(name='赛事名称'),  # 配置X轴，设置X轴的名称为"赛事名称"
        tooltip_opts=opts.TooltipOpts(  # 配置提示框组件
            trigger='axis',  # 设置触发类型为坐标轴触发，鼠标悬停在X轴上时显示该列所有数据
            axis_pointer_type='shadow'  # 设置指示器类型为阴影指示器
        ),
        yaxis_opts=opts.AxisOpts(  # 配置Y轴
            splitline_opts=opts.SplitLineOpts(  # 配置Y轴的分隔线
                is_show=True,  # 显示分隔线
                linestyle_opts=opts.LineStyleOpts(type_='dotted')  # 设置分隔线的样式为虚线
            )
        )
    )
)

c.render('历年奥运会中国奖牌数量统计柱形图.html')  # 将图表渲染并保存为HTML文件
print("图表已生成：历年奥运会中国奖牌数量统计柱形图.html")  # 打印提示信息，告知用户图表已成功生成


# 程序3：
import pandas as pd  # 导入pandas库，用于数据处理和读取Excel文件
from pyecharts.charts import Bar  # 从pyecharts图表模块导入柱状图类
from pyecharts import options as opts  # 导入pyecharts的配置选项模块
from pyecharts.globals import ThemeType  # 导入主题类型，用于设置图表主题风格

# 读取Excel数据
data = pd.read_excel('./data/奖牌.xlsx')  # 使用pandas读取Excel文件，将数据存储到data变量中

# 计算各奖牌占总数的比例
data['gold_p'] = data['金牌'] / data['总计']  # 计算金牌占总奖牌数的比例，创建新列gold_p
data['silver_p'] = data['银牌'] / data['总计']  # 计算银牌占总奖牌数的比例，创建新列silver_p
data['bronze_p'] = data['铜牌'] / data['总计']  # 计算铜牌占总奖牌数的比例，创建新列bronze_p

# 提取数据
dt1 = data.loc[:, ['赛事', '金牌', 'gold_p']].values.tolist()  # 提取赛事、金牌数量和金牌比例三列数据，转换为列表
dt2 = data.loc[:, ['赛事', '银牌', 'silver_p']].values.tolist()  # 提取赛事、银牌数量和银牌比例三列数据，转换为列表
dt3 = data.loc[:, ['赛事', '铜牌', 'bronze_p']].values.tolist()  # 提取赛事、铜牌数量和铜牌比例三列数据，转换为列表

# 定义基础样式字典
base_itemstyle = {  # 创建一个基础样式字典，包含柱子的通用样式配置
    "shadowBlur": 4,  # 设置阴影的模糊程度为4像素
    "shadowOffsetY": 1,  # 设置阴影在Y轴方向的偏移量为1像素（调小以获得更精细的效果）
    "shadowOffsetX": 4,  # 设置阴影在X轴方向的偏移量为4像素
    "borderRadius": [2, 2, 2, 2],  # 设置柱子的圆角，四个角都设置为2px圆角
    "opacity": 1  # 设置柱子的透明度为1（完全不透明）
}

# 为金牌创建样式（复制基础样式并添加金牌特定的颜色和阴影）
itemstyle1 = base_itemstyle.copy()  # 复制基础样式字典，避免修改原始字典
itemstyle1['color'] = '#FFD700'  # 设置金牌柱子的颜色为金黄色
itemstyle1['shadowColor'] = 'rgba(255, 215, 0, .5)'  # 为金牌柱子设置半透明的金黄色阴影

# 为银牌创建样式（复制基础样式并添加银牌特定的颜色和阴影）
itemstyle2 = base_itemstyle.copy()  # 复制基础样式字典
itemstyle2['color'] = '#C0C0C0'  # 设置银牌柱子的颜色为银灰色
itemstyle2['shadowColor'] = 'rgba(192, 192, 192, .5)'  # 为银牌柱子设置半透明的银灰色阴影

# 为铜牌创建样式（复制基础样式并添加铜牌特定的颜色和阴影）
itemstyle3 = base_itemstyle.copy()  # 复制基础样式字典
itemstyle3['color'] = '#CD7F32'  # 设置铜牌柱子的颜色为暖橙色（青铜色）
itemstyle3['shadowColor'] = 'rgba(205, 127, 50, .5)'  # 为铜牌柱子设置半透明的暖橙色阴影

# 创建堆叠柱状图
c = (  # 使用链式调用的方式创建和配置柱状图对象
    Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))  # 初始化柱状图对象，设置主题为浅色主题
    .add_xaxis([i[0] for i in dt1])  # 添加X轴数据，从dt1中提取赛事名称作为X轴的类目

    # 先添加铜牌系列（在最下层）
    .add_yaxis(  # 添加铜牌数据系列
        "铜牌",  # 系列名称，会显示在图例中
        [i[1] for i in dt3],  # Y轴数据，从dt3中提取铜牌数量
        stack="stack1",  # 设置堆叠名称为stack1，相同stack名称的系列会堆叠在一起
        category_gap="50%",  # 设置不同类目之间的间隙，占类目宽度的50%
        itemstyle_opts=itemstyle3  # 应用铜牌的样式配置（暖橙色）
    )

    # 再添加银牌系列（在中间层）
    .add_yaxis(  # 添加银牌数据系列
        "银牌",  # 系列名称，会显示在图例中
        [i[1] for i in dt2],  # Y轴数据，从dt2中提取银牌数量
        stack="stack1",  # 设置相同的堆叠名称，使其堆叠在铜牌之上
        category_gap="50%",  # 设置不同类目之间的间隙
        itemstyle_opts=itemstyle2  # 应用银牌的样式配置（灰色）
    )

    # 最后添加金牌系列（在最上层）
    .add_yaxis(  # 添加金牌数据系列
        "金牌",  # 系列名称，会显示在图例中
        [i[1] for i in dt1],  # Y轴数据，从dt1中提取金牌数量
        stack="stack1",  # 设置相同的堆叠名称，使其堆叠在银牌之上（最上层）
        category_gap="50%",  # 设置不同类目之间的间隙
        itemstyle_opts=itemstyle1  # 应用金牌的样式配置（黄色）
    )

    .set_series_opts(  # 设置系列的全局配置选项
        label_opts=opts.LabelOpts(position="right")  # 设置数据标签的位置为柱子右侧，显示具体数值
    )
    .set_global_opts(  # 设置图表的全局配置选项
        title_opts=opts.TitleOpts(title='历届奥运会奖牌数量堆积柱形图'),  # 设置图表的主标题
        tooltip_opts=opts.TooltipOpts(  # 配置提示框组件
            trigger='axis',  # 设置触发类型为坐标轴触发，鼠标悬停在X轴上时显示该列所有数据
            axis_pointer_type='shadow'  # 设置指示器类型为阴影指示器，显示阴影效果
        ),
        xaxis_opts=opts.AxisOpts(  # 配置X轴选项
            name='赛事名称',  # 设置X轴的名称
            axislabel_opts=opts.LabelOpts(rotate=15)  # 设置X轴标签旋转15度，避免文字重叠
        )
    )
)

c.render('堆叠柱形图.html')  # 将图表渲染并保存为HTML文件，文件名为"堆叠柱形图.html"
print("图表已生成：堆叠柱形图.html")  # 打印提示信息，告知用户图表已成功生成


# 程序4：
# ==================== 导入必要的库 ====================
import pandas as pd  # 导入pandas库，用于数据处理和Excel文件读取
from pyecharts.charts import Bar  # 从pyecharts的charts模块导入Bar类，用于创建柱状图
from pyecharts import options as opts  # 导入配置项模块，用于设置图表的各种选项
from pyecharts.globals import ThemeType  # 导入主题类型模块，用于设置图表主题
from pyecharts.commons.utils import JsCode  # 导入JsCode类，用于在图表中嵌入JavaScript代码

# ==================== 读取和处理数据 ====================
# 读取Excel文件中的奖牌数据，文件路径为'./data/奖牌.xlsx'
data = pd.read_excel('./data/奖牌.xlsx')

# 计算各类奖牌占总奖牌数的比例
# 金牌占比 = 金牌数量 / 总奖牌数量
data['gold_p'] = data['金牌'] / data['总计']

# 银牌占比 = 银牌数量 / 总奖牌数量
data['silver_p'] = data['银牌'] / data['总计']

# 铜牌占比 = 铜牌数量 / 总奖牌数量
data['bronze_p'] = data['铜牌'] / data['总计']

# ==================== 提取所需的数据列 ====================
# 提取金牌相关数据：赛事名称、金牌数量、金牌占比，并转换为列表格式
# .loc[:, ['赛事', '金牌', 'gold_p']] 选择这三列
# .values.tolist() 将DataFrame转换为嵌套列表，每个子列表包含一行数据
dt1 = data.loc[:, ['赛事', '金牌', 'gold_p']].values.tolist()

# 提取银牌相关数据：赛事名称、银牌数量、银牌占比，并转换为列表格式
dt2 = data.loc[:, ['赛事', '银牌', 'silver_p']].values.tolist()

# 提取铜牌相关数据：赛事名称、铜牌数量、铜牌占比，并转换为列表格式
dt3 = data.loc[:, ['赛事', '铜牌', 'bronze_p']].values.tolist()

# ==================== 定义柱状图的样式配置 ====================
# 创建基础样式字典，包含所有奖牌柱子的通用样式属性
base_itemstyle = {
    "shadowBlur": 4,  # 阴影的模糊半径为4像素，数值越大阴影越模糊
    "shadowOffsetY": 1,  # 阴影在Y轴（垂直方向）的偏移量为1像素，正值向下偏移
    "shadowOffsetX": 4,  # 阴影在X轴（水平方向）的偏移量为4像素，正值向右偏移
    "borderRadius": [2, 2, 2, 2],  # 柱子四个角的圆角半径，顺序为[左上, 右上, 右下, 左下]
    "opacity": 1  # 柱子的不透明度，1表示完全不透明，0表示完全透明
}

# ==================== 为不同奖牌创建专属样式 ====================
# 复制基础样式并为金牌添加特定的颜色和阴影效果
itemstyle1 = base_itemstyle.copy()  # 使用.copy()创建独立副本，避免修改原字典
itemstyle1['color'] = '#FFD700'  # 设置金牌柱子的填充颜色为金黄色（Gold色值）
itemstyle1['shadowColor'] = 'rgba(255, 215, 0, .5)'  # 设置阴影颜色为半透明的金黄色

# 复制基础样式并为银牌添加特定的颜色和阴影效果
itemstyle2 = base_itemstyle.copy()  # 创建独立的样式副本
itemstyle2['color'] = '#aca5c7'  # 设置银牌柱子的填充颜色为紫灰色（修改后的银色）
itemstyle2['shadowColor'] = 'rgba(172, 165, 199, .5)'  # 设置阴影颜色为半透明的紫灰色（与柱子颜色匹配）

# 复制基础样式并为铜牌添加特定的颜色和阴影效果
itemstyle3 = base_itemstyle.copy()  # 创建独立的样式副本
itemstyle3['color'] = '#f8c167'  # 设置铜牌柱子的填充颜色为金橙色（修改后的铜色）
itemstyle3['shadowColor'] = 'rgba(248, 193, 103, .5)'  # 设置阴影颜色为半透明的金橙色（与柱子颜色匹配）

# ==================== 定义JavaScript格式化函数 ====================
# 定义用于格式化柱子标签的JavaScript函数字符串
# 功能：将小数形式的比例转换为百分比格式显示
# 例如：0.456 -> "45.6%"
jscode = "function(x){return Number(x.data * 100).toFixed(1) + '%';}"

# 定义用于格式化Y轴刻度标签的JavaScript函数字符串
# 功能：将Y轴上的小数值转换为百分比格式显示
# 例如：0.5 -> "50.0%"
jscode2 = "function(x){return Number(x * 100).toFixed(1) + '%';}"

# ==================== 创建百分比堆叠柱状图 ====================
# 使用链式调用方式创建和配置柱状图对象
c = (
    # 初始化Bar图表对象，设置初始化选项
    Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))  # 使用LIGHT主题（浅色背景主题）

    # 添加X轴数据（横轴：赛事名称）
    # [i[0] for i in dt1] 是列表推导式，提取dt1中每个子列表的第一个元素（赛事名称）
    .add_xaxis([i[0] for i in dt1])

    # ==================== 添加铜牌数据系列（堆叠图的底层） ====================
    .add_yaxis(
        "铜牌",  # 系列名称，将显示在图例（legend）中
        # 提取铜牌占比数据并四舍五入到小数点后2位
        # [round(i[2], 2) for i in dt3] 提取dt3中每个子列表的第三个元素（铜牌占比）
        [round(i[2], 2) for i in dt3],
        stack="stack1",  # 堆叠组名称，相同stack值的系列会堆叠显示
        category_gap="55%",  # 不同类别（赛事）之间的柱子间隔，占类别宽度的55%
        itemstyle_opts=itemstyle3,  # 应用铜牌的样式配置（金橙色及阴影）
        label_opts=opts.LabelOpts(  # 配置数据标签的显示选项
            position="right",  # 标签显示在柱子的右侧
            formatter=JsCode(jscode),  # 使用JavaScript函数格式化标签为百分比格式
            color="#f8c167"  # 标签文字颜色设置为金橙色，与柱子颜色一致（已修改）
        )
    )

    # ==================== 添加银牌数据系列（堆叠图的中间层） ====================
    .add_yaxis(
        "银牌",  # 系列名称，将显示在图例中
        # 提取银牌占比数据并四舍五入到小数点后2位
        [round(i[2], 2) for i in dt2],
        stack="stack1",  # 使用相同的堆叠组名称，使其堆叠在铜牌之上
        category_gap="55%",  # 柱子间隔，与铜牌系列保持一致
        itemstyle_opts=itemstyle2,  # 应用银牌的样式配置（紫灰色及阴影）
        label_opts=opts.LabelOpts(  # 配置数据标签的显示选项
            position="right",  # 标签显示在柱子的右侧
            formatter=JsCode(jscode),  # 使用JavaScript函数格式化标签为百分比格式
            color="#aca5c7"  # 标签文字颜色设置为紫灰色，与柱子颜色一致（已修改）
        )
    )

    # ==================== 添加金牌数据系列（堆叠图的顶层） ====================
    .add_yaxis(
        "金牌",  # 系列名称，将显示在图例中
        # 提取金牌占比数据并四舍五入到小数点后2位
        [round(i[2], 2) for i in dt1],
        stack="stack1",  # 使用相同的堆叠组名称，使其堆叠在银牌之上（最顶层）
        category_gap="55%",  # 柱子间隔，与其他系列保持一致
        itemstyle_opts=itemstyle1,  # 应用金牌的样式配置（金黄色及阴影）
        label_opts=opts.LabelOpts(  # 配置数据标签的显示选项
            position="right",  # 标签显示在柱子的右侧
            formatter=JsCode(jscode),  # 使用JavaScript函数格式化标签为百分比格式
            color="#FFD700"  # 标签文字颜色设置为金黄色，与柱子颜色一致
        )
    )

    # ==================== 设置图表的全局配置选项 ====================
    .set_global_opts(
        # 配置图表标题
        title_opts=opts.TitleOpts(
            title='历年奥运会中国奖牌数量百分比堆积柱形图',  # 图表主标题文字
            pos_left='center',  # 标题水平位置居中显示
            pos_top='2%'  # 标题距离容器顶部的距离为2%
        ),

        # 配置图例（显示各系列名称的说明）
        legend_opts=opts.LegendOpts(
            pos_top='7%'  # 图例距离容器顶部的距离为7%，放在标题下方
        ),

        # 配置提示框组件（鼠标悬停时显示的信息框）
        tooltip_opts=opts.TooltipOpts(
            trigger='axis',  # 触发类型为坐标轴触发，鼠标悬停在某个类别上时显示该类别的所有系列数据
            axis_pointer_type='shadow'  # 指示器类型为阴影，会在柱子位置显示阴影指示器
        ),

        # 配置X轴选项（横轴：赛事名称）
        xaxis_opts=opts.AxisOpts(
            name='赛事名称',  # X轴的名称标签
            axislabel_opts=opts.LabelOpts(
                rotate=15  # X轴标签文字旋转15度，防止文字过长时重叠
            )
        ),

        # 配置Y轴选项（纵轴：奖牌占比）
        yaxis_opts=opts.AxisOpts(
            max_=1,  # 设置Y轴的最大值为1（代表100%），因为数据是占比形式
            axislabel_opts=opts.LabelOpts(  # 配置Y轴刻度标签的显示格式
                formatter=JsCode(jscode2)  # 使用JavaScript函数将Y轴刻度格式化为百分比显示
            )
        )
    )
)

# ==================== 渲染并保存图表 ====================
# 将配置好的图表渲染为HTML文件，可在浏览器中打开查看
c.render('百分比堆叠柱形图1.html')

# 打印提示信息，告知用户图表已成功生成
print("图表已生成：百分比堆叠柱形图1.html")


# 程序5：百分比堆叠
# ==================== 导入必要的库 ====================
import pandas as pd  # 导入pandas库，用于读取和处理Excel数据
from pyecharts.charts import Bar  # 从pyecharts图表库中导入Bar类，用于创建柱状图
from pyecharts import options as opts  # 导入options模块并重命名为opts，用于配置图表的各种选项
from pyecharts.globals import ThemeType  # 从globals模块导入ThemeType，用于设置图表主题样式
from pyecharts.commons.utils import JsCode  # 导入JsCode类，用于在Python中嵌入JavaScript代码

# ==================== 读取Excel数据 ====================
# 使用pandas的read_excel函数读取Excel文件
# './data/奖牌.xlsx'是文件的相对路径，data变量存储读取的DataFrame对象
data = pd.read_excel('./data/奖牌.xlsx')

# ==================== 计算各奖牌占总数的比例 ====================
# 创建新列'gold_p'，计算金牌数量占总奖牌数的比例（小数形式）
# 例如：如果金牌15枚，总计50枚，则gold_p = 15/50 = 0.3
data['gold_p'] = data['金牌'] / data['总计']

# 创建新列'silver_p'，计算银牌数量占总奖牌数的比例（小数形式）
data['silver_p'] = data['银牌'] / data['总计']

# 创建新列'bronze_p'，计算铜牌数量占总奖牌数的比例（小数形式）
data['bronze_p'] = data['铜牌'] / data['总计']

# ==================== 提取所需的数据列并转换为列表 ====================
# 使用.loc选择器提取指定的三列：['赛事', '金牌', 'gold_p']
# .values将DataFrame转换为numpy数组，.tolist()再转换为Python列表
# 最终dt1的格式：[['北京2008', 51, 0.48], ['伦敦2012', 38, 0.43], ...]
dt1 = data.loc[:, ['赛事', '金牌', 'gold_p']].values.tolist()

# 提取银牌相关的三列数据并转换为列表格式
# 格式：[['北京2008', 21, 0.20], ['伦敦2012', 27, 0.31], ...]
dt2 = data.loc[:, ['赛事', '银牌', 'silver_p']].values.tolist()

# 提取铜牌相关的三列数据并转换为列表格式
# 格式：[['北京2008', 28, 0.26], ['伦敦2012', 23, 0.26], ...]
dt3 = data.loc[:, ['赛事', '铜牌', 'bronze_p']].values.tolist()

# ==================== 定义柱状图的基础样式 ====================
# 创建基础样式字典，包含所有奖牌柱子的通用样式属性
# 这个字典定义了阴影效果、圆角、透明度等通用样式
base_itemstyle = {
    "shadowBlur": 4,  # 阴影的模糊半径为4像素，数值越大阴影越模糊，产生柔和的阴影效果
    "shadowOffsetY": 1,  # 阴影在Y轴（垂直方向）的偏移量为1像素，正值表示阴影向下偏移
    "shadowOffsetX": 4,  # 阴影在X轴（水平方向）的偏移量为4像素，正值表示阴影向右偏移
    "borderRadius": [2, 2, 2, 2],  # 柱子四个角的圆角半径，顺序为[左上, 右上, 右下, 左下]，单位为像素
    "opacity": 1  # 柱子的不透明度，范围0-1，1表示完全不透明，0表示完全透明
}

# ==================== 为不同奖牌创建专属样式 ====================
# 为金牌创建样式配置
# 使用.copy()方法复制基础样式字典，创建一个独立的副本，避免修改原始字典
itemstyle1 = base_itemstyle.copy()
itemstyle1['color'] = '#FFD700'  # 设置金牌柱子的填充颜色为金黄色（Gold的标准色值）
itemstyle1['shadowColor'] = 'rgba(255, 215, 0, .5)'  # 设置阴影颜色为半透明的金黄色，rgba中最后的.5表示50%透明度

# 为银牌创建样式配置
# 同样先复制基础样式，然后设置银牌特有的颜色
itemstyle2 = base_itemstyle.copy()
itemstyle2['color'] = '#aca5c7'  # 设置银牌柱子的填充颜色为紫灰色，营造类似银色的金属质感
itemstyle2['shadowColor'] = 'rgba(172, 165, 199, .5)'  # 设置阴影颜色为半透明的紫灰色，与柱子颜色相呼应

# 为铜牌创建样式配置
# 同样的流程，复制基础样式后设置铜牌的颜色
itemstyle3 = base_itemstyle.copy()
itemstyle3['color'] = '#f8c167'  # 设置铜牌柱子的填充颜色为金橙色，模拟铜的颜色
itemstyle3['shadowColor'] = 'rgba(248, 193, 103, .5)'  # 设置阴影颜色为半透明的金橙色

# ==================== 定义提示框格式化函数 ====================
# 使用JsCode包装JavaScript函数，用于自定义鼠标悬停时提示框的显示内容
# 这个函数将在浏览器端执行，当用户鼠标悬停在图表上时被调用
tooltip_formatter = JsCode(
    """
    function (params) {
        // params参数是一个数组，包含当前鼠标位置下所有堆叠系列的数据
        // params[0]是第一个系列的数据对象
        // params[0].name 是当前X轴的类别名称（例如"北京2008"）
        var result = params[0].name + '<br/>';  // 首先显示赛事名称，<br/>是HTML换行符

        // 使用for循环遍历params数组中的每个系列数据
        // params.length表示数组的长度（即有多少个系列：金牌、银牌、铜牌）
        for (var i = 0; i < params.length; i++) {
            // params[i].seriesName 是当前系列的名称（"金牌"/"银牌"/"铜牌"）
            // params[i].value 是当前系列在这个位置的数值（百分比）
            // 将系列名称、数值和百分号拼接成一行，并添加换行符
            result += params[i].seriesName + ': ' + params[i].value + '%<br/>';
        }

        // 返回格式化后的HTML字符串
        // 例如返回："北京2008<br/>铜牌: 26.4%<br/>银牌: 19.8%<br/>金牌: 48.1%<br/>"
        return result;
    }
    """
)

# ==================== 创建百分比堆叠柱状图 ====================
# 使用链式调用（方法链）的方式构建图表对象
# 每个方法调用后都会返回self（图表对象本身），因此可以继续调用下一个方法
c = (
    # 第一步：初始化Bar图表对象
    # init_opts用于设置图表的初始化选项
    # ThemeType.LIGHT指定使用浅色主题（白色背景、深色文字）
    Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))

    # 第二步：添加X轴数据（横轴，显示赛事名称）
    # [i[0] for i in dt1] 是列表推导式
    # 从dt1列表中提取每个子列表的第一个元素（索引0），即赛事名称
    # 结果类似：['北京2008', '伦敦2012', '里约2016', '东京2020', '巴黎2024']
    .add_xaxis([i[0] for i in dt1])

    # ==================== 第一层（底层）：添加铜牌数据系列 ====================
    # 堆叠柱状图必须按照从下到上的顺序添加系列
    # 先添加的系列会显示在底部，后添加的系列堆叠在上面
    .add_yaxis(
        "铜牌",  # 第一个参数：系列的名称，会显示在图例和提示框中

        # 第二个参数：Y轴数据，使用列表推导式处理数据
        # i[2]表示每个子列表的第三个元素，即铜牌占比（小数形式，如0.264）
        # i[2] * 100 将小数转换为百分比（如0.264 * 100 = 26.4）
        # round(..., 1) 四舍五入保留1位小数（如26.4）
        # 最终生成类似 [26.4, 26.2, 24.1, ...] 的列表
        [round(i[2] * 100, 1) for i in dt3],

        stack="stack1",  # stack参数指定堆叠组的名称，相同名称的系列会堆叠显示
        category_gap="55%",  # 设置不同类别（赛事）之间的柱子间隔，占类别宽度的55%
        itemstyle_opts=itemstyle3,  # 应用铜牌的样式配置字典（金橙色及阴影效果）

        # 配置数据标签（显示在柱子上的文字）
        label_opts=opts.LabelOpts(
            position="right",  # 标签位置：显示在柱子的右侧
            formatter="{c}%",  # 标签格式：{c}是占位符，会被实际数值替换，后面加上%符号
            color="#f8c167"  # 标签文字颜色：设置为金橙色，与柱子颜色保持一致
        )
    )

    # ==================== 第二层（中间层）：添加银牌数据系列 ====================
    .add_yaxis(
        "银牌",  # 系列名称

        # 提取银牌数据并转换为百分比
        # dt2是银牌数据列表，处理方式与铜牌相同
        [round(i[2] * 100, 1) for i in dt2],

        stack="stack1",  # 使用相同的堆叠组名称，使其堆叠在铜牌系列之上
        category_gap="55%",  # 保持相同的类别间隔
        itemstyle_opts=itemstyle2,  # 应用银牌的样式配置（紫灰色及阴影）

        label_opts=opts.LabelOpts(
            position="right",  # 标签显示在右侧
            formatter="{c}%",  # 百分比格式
            color="#aca5c7"  # 紫灰色标签
        )
    )

    # ==================== 第三层（顶层）：添加金牌数据系列 ====================
    .add_yaxis(
        "金牌",  # 系列名称

        # 提取金牌数据并转换为百分比
        # dt1是金牌数据列表
        [round(i[2] * 100, 1) for i in dt1],

        stack="stack1",  # 使用相同的堆叠组名称，使其堆叠在最顶层
        category_gap="55%",  # 保持相同的类别间隔
        itemstyle_opts=itemstyle1,  # 应用金牌的样式配置（金黄色及阴影）

        label_opts=opts.LabelOpts(
            position="right",  # 标签显示在右侧
            formatter="{c}%",  # 百分比格式
            color="#FFD700"  # 金黄色标签
        )
    )

    # ==================== 设置图表的全局配置选项 ====================
    .set_global_opts(
        # 配置图表标题
        title_opts=opts.TitleOpts(
            title='历年奥运会中国奖牌数量百分比堆积柱形图',  # 设置主标题文字
            pos_left='center',  # 标题水平位置：居中对齐（也可以设置为'left'、'right'或具体像素值）
            pos_top='2%'  # 标题垂直位置：距离容器顶部2%的高度
        ),

        # 配置图例（显示各系列名称的说明区域）
        legend_opts=opts.LegendOpts(
            pos_top='7%'  # 图例位置：距离容器顶部7%，放在标题下方
        ),

        # 配置提示框组件（鼠标悬停时显示的信息框）
        tooltip_opts=opts.TooltipOpts(
            trigger='axis',  # 触发类型：'axis'表示坐标轴触发，鼠标在X轴任意位置悬停时显示该位置所有系列的数据
            axis_pointer_type='shadow',  # 指示器类型：'shadow'表示阴影指示器，会在柱子位置显示阴影背景高亮效果
            formatter=tooltip_formatter  # 使用自定义的JavaScript格式化函数来格式化提示框的内容
        ),

        # 配置X轴（横轴）选项
        xaxis_opts=opts.AxisOpts(
            name='赛事名称',  # X轴的名称标签，会显示在X轴的末端
            axislabel_opts=opts.LabelOpts(  # 配置X轴刻度标签的选项
                rotate=15  # 标签文字旋转角度：顺时针旋转15度，用于避免赛事名称过长时文字重叠
            )
        ),

        # 配置Y轴（纵轴）选项
        yaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(  # 配置Y轴刻度标签的选项
                formatter="{value}%"  # Y轴标签的格式化字符串，{value}占位符会被替换为实际的刻度值，后面加上%符号
            ),
            max_=100  # 设置Y轴的最大值为100，因为我们的数据已经转换为0-100的百分比形式
        )
    )
)

# ==================== 渲染并保存图表到HTML文件 ====================
# render方法将图表对象转换为HTML文件
# 生成的HTML文件包含完整的图表代码（包括ECharts库和数据），可以在任何浏览器中直接打开查看
# 文件会保存在脚本运行的当前工作目录下
c.render('堆叠图提示框修复.html')

# 在控制台打印成功提示信息
# 让用户知道图表已经成功生成，并告知文件名
print("图表已生成：堆叠图提示框.html")
