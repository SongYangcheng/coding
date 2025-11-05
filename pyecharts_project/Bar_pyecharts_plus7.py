from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.globals import ThemeType
import pandas as pd
import numpy as np
from pyecharts.commons.utils import JsCode

# 假设 data/age.xlsx 存在，并且列是 ['年龄组', '男性', '女性']
# 为了使示例可运行，我们创建一个模拟的DataFrame
# 在您的实际使用中，请保留 pd.read_excel('data/age.xlsx')
try:
    data = pd.read_excel('data/age.xlsx')
    data.columns = ['年龄组', '男性', '女性']
except FileNotFoundError:
    print("未找到 'data/age.xlsx'，使用模拟数据代替。")
    data_dict = {
        '年龄组': ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80+'],
        '男性': [150, 200, 250, 300, 280, 220, 180, 100, 50],
        '女性': [140, 190, 260, 310, 290, 230, 190, 110, 60]
    }
    data = pd.DataFrame(data_dict)


data_sorted = data.sort_values(by='年龄组', ascending=False)
age_group = data_sorted['年龄组'].tolist()
male_data = data_sorted['男性'].tolist()
female_data = data_sorted['女性'].tolist()

#创建柱状图
c = (
    Bar(init_opts=opts.InitOpts(width='1200px',
                                 height='800px',
                                 bg_color='#333333',
                                 theme=ThemeType.DARK))
    .add_xaxis(xaxis_data=age_group)
    .add_yaxis(series_name='男性', #添加第一个系列数据
               y_axis=male_data,
               itemstyle_opts=opts.ItemStyleOpts(
                   color='#49a9dc',
                   border_radius=3, #圆角
                   opacity=1 #透明度
               ),
               #设置数据标签选项
               label_opts=opts.LabelOpts(
                   is_show=True,
                   position='top',
                   color='#FFFFFF',
                   font_size=12,
                   formatter="{c}人"
               )
)
#添加第二个系列数据
    .add_yaxis(series_name='女性',
               y_axis=[-x for x in female_data],
               itemstyle_opts=opts.ItemStyleOpts(
                   color='#eab8d1',
                   border_radius=3, # 圆角
                   opacity=1
               ),
               #设置数据标签选项
               label_opts=opts.LabelOpts(
                   is_show=True, #显示标签  
                   position='bottom', # <--- 修正建议 (2): 'bottom' -> 'left'
                   color='#FFFFFF',
                   font_size=12,
                   formatter=JsCode("function(params) { return Math.abs(params.value) + '人'; }") #使用JS代码格式化标签
               )
)
#全局设置
.set_global_opts(
    title_opts=opts.TitleOpts( #主标题
        title='某地区人口金字塔图',
        is_show=True,
        pos_left='center',
        # 补充：使标题在暗色背景下可见
        title_textstyle_opts=opts.TextStyleOpts(color='#FFFFFF',font_size=20)  #标题文字颜色
    ),
    legend_opts=opts.LegendOpts(
        pos_right='10%',
        pos_top='5%',
        textstyle_opts=opts.TextStyleOpts(
            color='#FFFFFF',
            font_size=14
        ),

    ),
    xaxis_opts=opts.AxisOpts( #X轴配置 (反转后变为Y轴)
        type_='category', #类目轴
        axislabel_opts=opts.LabelOpts(
            color='white' #设置标签为白色
        ),
        axisline_opts=opts.AxisLineOpts(
            linestyle_opts=opts.LineStyleOpts(
                color='gray' #设置轴线颜色为灰色
            )
        )
    ),
    yaxis_opts=opts.AxisOpts( #Y轴配置 (反转后变为X轴)
        type_='value', #数值轴
        axislabel_opts=opts.LabelOpts(
            formatter=JsCode(
                "function(value){return Math.abs(value)}" #使用JS代码格式化标签为绝对值
            ),
            color='white' # <--- 补充：使Y轴标签可见
        ),
        max_=max(male_data) * 1.1 if male_data else 10,
        min_=-max(female_data) * 1.1 if female_data else -10,
        splitline_opts=opts.SplitLineOpts( #分割线配置
            is_show=True,
            linestyle_opts=opts.LineStyleOpts(
                color="#555555",
                type_='dashed'
            )
        )
    ),
    tooltip_opts=opts.TooltipOpts( #提示框配置
        trigger='axis',
        axis_pointer_type='shadow',
        # <--- 修正 (3): 修复 JsCode 的语法错误
        # formatter=JsCode(
        #     # """function(params){
        #     #     // params 是一个数组，params[0] 是男性，params[1] 是女性
        #     #     var male = params[0] ? params[0].value : 0;
        #     #     var female = params[1] ? Math.abs(params[1].value) : 0;
                
        #     #     // 返回格式化的HTML字符串
        #     #     return params[0].name + '<br/>' + 
        #     #            params[0].seriesName + ': ' + male + '人<br/>' +
        #     #            params[1].seriesName + ': ' + female + '人';
        #     # }"""
        # ),
    )
)
#旋转坐标轴
.reversal_axis()
)

# 生成HTML文件
c.render('html/人口金字塔图.html')
print("代码检查完毕，已生成 'html/人口金字塔图.html'")