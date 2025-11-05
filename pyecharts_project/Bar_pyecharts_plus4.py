#coding:utf-8
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.globals import ThemeType, JsCode #导入主题和样式操作
import pandas as pd
import numpy as np
import sys
import os

#函数一：创建kaggle竞赛热度柱状图
def create_kaggle_trend_chart(csv_file='data/subject.csv', output_html='html/kaggle_trend_chart.html'):
    #读取数据
    try:
        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"文件不存在: {csv_file}")
        data = pd.read_csv(csv_file, encoding='utf-8')
        print("数据读取成功")
        if len(data) == 0:
            raise ValueError("数据文件为空")
    except FileNotFoundError:
        print('文件不存在')
    #提取主题和热度
    except Exception as e:
        print(f'读取数据失败: {e}')
        return False

    data_top = data.head(15).copy()
    #竞赛名称太长进行截断
    data_x = [str(name)[:40] + '...' if len(str(name)) > 40 else str(name) for name in data_top['Name'].tolist()]

    data_y = []
    for value in data_top['Gain'].tolist():
        try:
            data_y.append(float(value) if pd.notna(value) else 0.0)
        except:
            data_y.append(0.0)
            print(f'警告：增益值 {value}格式错误，已设置为0.0')
    #new echarts.graphic.LinearGradient(0, 0, 0, 1, [...], false): 创建ECharts线性渐变对象，核心用于图表元素，颜色渐变填充
    #0， 0 ， 0， 1：表示渐变起始坐标x0，y0和结束坐标x1，y1，范围均为0到1
    style_positive = JsCode(
        """
        new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {offset: 0, color: '#83bff6'},
            {offset: 0.5, color: '#188df0'},
            {offset: 1, color: '#188df0'}
        ], false)
        """
    )
    #负值渐变色
    style_negative = JsCode(
        """
        new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {offset: 0, color: '#ff9999'},
            {offset: 0.5, color: '#ff4d4d'},
            {offset: 1, color: '#cc0000'}
        ], false)
        """
    )
    #格式化数据
    formatted_data_y = []
    for x, y in zip(data_x, data_y):
        y = float(y)
        color_style = style_positive if y >= 0 else style_negative
        formatted_data_y.append(
            opts.BarItem(
                name=x,
                value=y,
                itemstyle_opts=opts.ItemStyleOpts(color=color_style)
            )
        )
    #创建图表
    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT,
                                     width='900px', 
                                     height='600px', 
                                     bg_color='#FFFFFF',
                                     renderer='canvas' #使用canvas渲染器
                                     ))
        .add_xaxis(data_x)
        .add_yaxis("每月在线人数增益名称", formatted_data_y,
                   label_opts=opts.LabelOpts(is_show=True,
                                             position='top',
                                             formatter="{c}",
                                             color="#ffffff",
                                             font_weight="bold" #字体为粗体
                                             ))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Kaggle竞赛主题热度分布", #主标题
                                       subtitle="每月在线人数增益", #副标题
                                       pos_left='center',
                                       pos_top='20px', #距离顶部20px
                                       title_textstyle_opts=opts.TextStyleOpts(
                                           color="#ffffff",
                                           font_size=20,
                                           font_weight="bold"
                                       ),
                                        subtitle_textstyle_opts=opts.TextStyleOpts(
                                             color="#aaaaaa",
                                             font_size=14
                                        )
                                        ),
            #x轴配置
            xaxis_opts=opts.AxisOpts(
                name="竞赛主题",
                axislabel_opts=opts.LabelOpts(
                    rotate=45,
                    interval=0,
                    color="#ffffff",
                    font_size=10
                ),
                name_location='middle',
                name_gap=50,
                name_textstyle_opts=opts.TextStyleOpts(
                    color='#ffffff',
                    font_size=14,
                ),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(
                        color="#444444"
                    )
                )
            ),
            #y轴配置
            yaxis_opts=opts.AxisOpts(
                name="热度",
                name_location='middle', #名称位置
                name_gap=40, #名称与轴线距离
                name_textstyle_opts=opts.TextStyleOpts(
                    color='#ffffff',
                    font_size=14,
                ),
                #Y轴标签样式
                axislabel_opts=opts.LabelOpts(
                    color="#ffffff",
                    font_size=12
                ),
                #Y轴线样式
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(
                        color="#444444",
                        width=1
                    )
                ),
                #Y轴分割线配置
                splitline_opts=opts.SplitLineOpts(
                    is_show=True,
                    linestyle_opts=opts.LineStyleOpts(
                        opacity=1,
                        color="#444444",
                    )
                )
            ),
            #提示框配置
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",  #触发类型为坐标轴触发
                axis_pointer_type="shadow", #指示器类型为阴影
                formatter="{b}<br/>在线人数增益：{c}",#提示框内容格式
                background_color="rgba(0, 0, 0, 0.8)", #背景颜色
                border_color="#333333", #边框颜色
                border_width=1, #边框宽度
                textstyle_opts=opts.TextStyleOpts(
                    color="#ffffff",
                    font_size=12
                )
            ),
            #数据缩放配置
            datazoom_opts=[
                opts.DataZoomOpts(
                    type_='slider',
                    range_start=0,
                    range_end=100,
                    pos_bottom='5%', #距离底部：5%
                ),
                opts.DataZoomOpts(
                    type_='inside',
                    range_start=0, #范围起始
                    range_end=100 #结束位置
                )
            ],
            #工具配置
            toolbox_opts=opts.ToolboxOpts(
                is_show=True, #显示工具栏
                pos_right='20px', #距离右侧20px
                pos_top='20px', #距离顶部20px
                feature={
                    "saveAsImage": {
                        "type": "png",
                        "title": "保存为图片",
                        "backgroundColor": "#ffffff"
                    },
                    "restore": {
                        "title": "还原"
                    },
                    "dataZoom": {
                        "title": {"zoom": "区域缩放", "back": "区域还原"}
                    }
                }
            )
        )
    )
    try:
        bar.render(output_html)
        print(f"柱状图已保存为 {output_html}")
        return True
    except Exception as e:
        print(f"保存柱状图失败: {e}")
        return False

#主函数
def main():
    print('1.竞赛热度分析图')
    print('2.竞赛增长率分析图')
    print('3. 交互缩放和工具提示')
    print('4. 可导入为图片')
    #初始计数器
    success_count = 0
    if create_kaggle_trend_chart():
        success_count += 1
    print(f"成功生成图表数量: {success_count}")
if __name__ == "__main__":
    main()