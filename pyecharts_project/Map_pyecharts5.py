import pyecharts.options as opts
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode
# 确保导入 Line
from pyecharts.charts import Timeline, Grid, Bar, Map, Pie, Line
import os

# 确保html文件夹存在
if not os.path.exists("html"):
    os.makedirs("html")

# 原始数据
data = [
    {
        "time": 1980,
        "data": [
            {"name": "台湾省", "value": [633.76, 12.28, "台湾省"]},
            {"name": "香港特别行政区", "value": [432.47, 8.38, "香港特别行政区"]},
            {"name": "江苏省", "value": [319.8, 6.2, "江苏省"]},
            {"name": "上海市", "value": [311.89, 6.05, "上海市"]},
            {"name": "山东省", "value": [292.13, 5.66, "山东省"]},
            {"name": "辽宁省", "value": [281, 5.45, "辽宁省"]},
            {"name": "广东省", "value": [249.65, 4.84, "广东省"]},
            {"name": "四川省", "value": [229.31, 4.44, "四川省"]},
            {"name": "河南省", "value": [229.16, 4.44, "河南省"]},
            {"name": "黑龙江省", "value": [221, 4.28, "黑龙江省"]},
        ],
    },
    {
        "time": 2000,
        "data": [
            {"name": "台湾省", "value": [27435.15, 19.47, "台湾省"]},
            {"name": "香港特别行政区", "value": [14201.59, 10.08, "香港特别行政区"]},
            {"name": "广东省", "value": [10741.25, 7.62, "广东省"]},
            {"name": "江苏省", "value": [8553.69, 6.07, "江苏省"]},
            {"name": "山东省", "value": [8337.47, 5.92, "山东省"]},
            {"name": "浙江省", "value": [6141.03, 4.36, "浙江省"]},
            {"name": "河南省", "value": [5052.99, 3.59, "河南省"]},
            {"name": "河北省", "value": [5043.96, 3.58, "河北省"]},
            {"name": "上海市", "value": [4771.17, 3.39, "上海市"]},
            {"name": "辽宁省", "value": [4669.1, 3.31, "辽宁省"]},
        ],
    },
    {
        "time": 2005,
        "data": [
            {"name": "台湾省", "value": [30792.89, 12.52, "台湾省"]},
            {"name": "广东省", "value": [22527.37, 9.16, "广东省"]},
            {"name": "江苏省", "value": [18598.69, 7.56, "江苏省"]},
            {"name": "山东省", "value": [18366.87, 7.47, "山东省"]},
            {"name": "香港特别行政区", "value": [14869.68, 6.05, "香港特别行政区"]},
            {"name": "浙江省", "value": [13417.68, 5.46, "浙江省"]},
            {"name": "河南省", "value": [10587.42, 4.3, "河南省"]},
            {"name": "河北省", "value": [10043.42, 4.08, "河北省"]},
            {"name": "上海市", "value": [9247.66, 3.76, "上海市"]},
            {"name": "辽宁省", "value": [8047.3, 3.27, "辽宁省"]},
        ],
    },
    {
        "time": 2010,
        "data": [
            {"name": "广东省", "value": [46036.25, 9.49, "广东省"]},
            {"name": "江苏省", "value": [41425.48, 8.54, "江苏省"]},
            {"name": "山东省", "value": [39169.92, 8.08, "山东省"]},
            {"name": "台湾省", "value": [30205.64, 6.23, "台湾省"]},
            {"name": "浙江省", "value": [27747.65, 5.72, "浙江省"]},
            {"name": "河南省", "value": [23092.36, 4.76, "河南省"]},
            {"name": "河北省", "value": [20394.26, 4.21, "河北省"]},
            {"name": "辽宁省", "value": [18457.3, 3.81, "辽宁省"]},
            {"name": "四川省", "value": [17185.48, 3.54, "四川省"]},
            {"name": "上海市", "value": [17165.98, 3.54, "上海市"]},
        ],
    },
    {
        "time": 2015,
        "data": [
            {"name": "广东省", "value": [72812.55, 9.35, "广东省"]},
            {"name": "江苏省", "value": [70116.38, 9, "江苏省"]},
            {"name": "山东省", "value": [63002.3, 8.09, "山东省"]},
            {"name": "浙江省", "value": [42886, 5.51, "浙江省"]},
            {"name": "河南省", "value": [37010.25, 4.75, "河南省"]},
            {"name": "台湾省", "value": [32604.52, 4.19, "台湾省"]},
            {"name": "四川省", "value": [30103.1, 3.87, "四川省"]},
            {"name": "河北省", "value": [29806.1, 3.83, "河北省"]},
            {"name": "湖北省", "value": [29550.19, 3.8, "湖北省"]},
            {"name": "湖南省", "value": [29047.2, 3.73, "湖南省"]},
        ],
    },
]

# --- 步骤 1: 数据预处理 ---
# 提取所有年份
time_list = [d["time"] for d in data]

# 构建一个 {省份: {年份: GDP}} 的字典
all_province_data = {}
for d in data:
    year = d["time"]
    for province_data in d["data"]:
        name = province_data["name"]
        gdp = province_data["value"][0]
        if name not in all_province_data:
            all_province_data[name] = {}
        all_province_data[name][year] = gdp
# --- 预处理结束 ---

# (确保您在文件顶部导入了所有图表)
# from pyecharts.charts import Timeline, Grid, Bar, Map, Pie, Line
def get_year_chart(year: int, all_data: dict, all_years: list):
    # 提取当年的数据
    map_data = [
        [[x["name"], x["value"]] for x in d["data"]] for d in data if d["time"] == year
    ][0]
    
    min_data, max_data = (
        min([d[1][0] for d in map_data]),
        max([d[1][0] for d in map_data]),
    )
    
    # 1. 定义地图 (使用 layout_center 和 layout_size 定位)
    map_chart = (
        Map()
        .add(
            series_name="",
            data_pair=map_data,
            label_opts=opts.LabelOpts(is_show=False),
            is_map_symbol_show=False,
            itemstyle_opts={
                "normal": {"areaColor": "#323c48", "borderColor": "#404a59"},
                "emphasis": {
                    "label": {"show": Timeline},
                    "areaColor": "rgba(255,255,255, 0.5)",
                },
            },
            # 地图位置 (左上)
            layout_center=["27.5%", "35%"],
            layout_size="50%"
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="1980年以来中国各省GDP排名变化情况",
                subtitle="GDP单位:亿元",
                pos_left="center",
                pos_top="top",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=25, color="rgba(255,255,255, 0.9)"
                ),
            ),
            tooltip_opts=opts.TooltipOpts(
                is_show=True,
                formatter=JsCode(
                    """function(params) {
                    if ('value' in params.data) {
                        return params.data.value[2] + ': ' + params.data.value[0];
                    }
                }"""
                ),
            ),
            visualmap_opts=opts.VisualMapOpts(
                is_calculable=True,
                dimension=0,
                pos_left="10",
                pos_top="center",
                range_text=["High", "Low"],
                range_color=["lightskyblue", "yellow", "orangered"],
                textstyle_opts=opts.TextStyleOpts(color="#ddd"),
                min_=min_data,
                max_=max_data,
            ),
        )
    )

    # 2. 定义柱状图 (使用 grid_opts, 放在左下角)
    bar_x_data = [x[0] for x in map_data]
    bar_y_data = [{"name": x[0], "value": x[1][0]} for x in map_data]
    bar = (
        Bar()
        .add_xaxis(xaxis_data=bar_x_data)
        .add_yaxis(
            series_name="",
            y_axis=bar_y_data,
            label_opts=opts.LabelOpts(
                is_show=True, position="right", formatter="{b}: {c}"
            ),
        )
        .reversal_axis()
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(is_show=False)),
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(is_show=False)),
            tooltip_opts=opts.TooltipOpts(is_show=False),
            visualmap_opts=opts.VisualMapOpts(
                is_calculable=True,
                dimension=0,
                pos_left="10",
                pos_top="center",
                range_text=["High", "Low"],
                range_color=["lightskyblue", "yellow", "orangered"],
                textstyle_opts=opts.TextStyleOpts(color="#ddd"),
                min_=min_data,
                max_=max_data,
            ),
        )
    )

    # 3. 定义饼图 (使用 center 定位, 放在右下角)
    pie_data = [[x[0], x[1][0]] for x in map_data]
    rest_value = 0
    if map_data:
        first_province_gdp = map_data[0][1][0]
        first_province_percent = map_data[0][1][1]
        if first_province_percent > 0:
            total_gdp = (first_province_gdp / first_province_percent) * 100
            top_10_gdp_sum = sum(item[1][0] for item in map_data)
            rest_value = total_gdp - top_10_gdp_sum
            rest_value = max(rest_value, 0)
    pie_data.append(["其他省份", round(rest_value, 2)])
    
    pie = (
        Pie()
        .add(
            series_name="",
            data_pair=pie_data,
            radius=["12%", "20%"],
            # 饼图位置 (右下)
            center=["77.5%", "75%"], 
            itemstyle_opts=opts.ItemStyleOpts(
                border_width=1, border_color="rgba(0,0,0,0.3)"
            ),
            # --- 额外优化：修复饼图标签重叠 ---
            label_opts=opts.LabelOpts(
                position="outside",
                formatter="{b}\n{d}%", # 显示省份和百分比
                color="#fff" # 标签文字颜色
            ),
        )
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=True, formatter="{b} {d}%"),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )

    # 4. 定义折线图 (使用 grid_opts, 放在右上角)
    line_chart = (
        Line()
        .add_xaxis(xaxis_data=[str(y) for y in all_years])
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title=f"{year}年 Top 10 省份GDP趋势",
                pos_left="77.5%", # 对应右上角的中心
                pos_top="10%", 
                title_textstyle_opts=opts.TextStyleOpts(color="#fff", font_size=16)
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            legend_opts=opts.LegendOpts(
                pos_left="center", 
                pos_bottom="bottom", 
                textstyle_opts=opts.TextStyleOpts(color="#fff")
            ),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(color="#fff")),
            
            # --- !!! 核心修复在这里 !!! ---
            yaxis_opts=opts.AxisOpts(
                # type_="log", # <-- 移除对数轴, 否则包含None的数据会渲染失败
                axislabel_opts=opts.LabelOpts(color="#fff")
            ),
        )
    )
    
    current_top_provinces = [d[0] for d in map_data]
    for province_name in current_top_provinces:
        history_data = all_data.get(province_name, {})
        # .get(y) 默认返回 None, 这对于线性轴是OK的
        trend = [history_data.get(y) for y in all_years] 
        
        line_chart.add_yaxis(
            series_name=province_name,
            y_axis=trend,
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(name="当前年份", coord=[str(year), history_data.get(year)])
                ]
            )
        )

    # --- 步骤 5: 最终组合 ---
    final_chart = (
        Grid(init_opts=opts.InitOpts(width="1600px", height="900px", theme=ThemeType.DARK))
        # (左下) 柱状图
        .add(
            bar,
            grid_opts=opts.GridOpts(
                pos_left="5%", pos_right="55%", pos_top="55%", pos_bottom="5%"
            ),
        )
        # (右上) 折线图
        .add(
            line_chart,
            grid_opts=opts.GridOpts(
                pos_left="60%", pos_right="5%", pos_top="15%", pos_bottom="50%"
            ),
        )
        # (左上) 地图 (传入空 grid_opts)
        .add(map_chart, grid_opts=opts.GridOpts()) 
        # (右下) 饼图 (传入空 grid_opts)
        .add(pie, grid_opts=opts.GridOpts())
    )
    
    return final_chart

# --- (您文件中的 Timeline 和 render 部分保持不变) ---
# (确保您的 Timeline 初始化尺寸和 Grid 一致)

time_list = [d["time"] for d in data]

timeline = Timeline(
    init_opts=opts.InitOpts(width="1600px", height="900px", theme=ThemeType.DARK)
)
for y in time_list:
    g = get_year_chart(
        year=y, 
        all_data=all_province_data, 
        all_years=time_list
    )
    timeline.add(g, time_point=str(y))

timeline.add_schema(
    orient="vertical",
    is_auto_play=True,
    is_inverse=True,
    play_interval=5000,
    pos_left="null",
    pos_right="5",
    pos_top="20",
    pos_bottom="20",
    width="50",
    label_opts=opts.LabelOpts(is_show=True, color="#fff"),
)

# 渲染图表
timeline.render("html/Map_pyecharts5_with_line.html")

print("图表已生成，请查看 html/Map_pyecharts5_with_line.html 文件")