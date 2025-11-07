from pyecharts import options as opts
from pyecharts.charts import Liquid
from pyecharts.globals import SymbolType, ThemeType
from pyecharts.commons.utils import JsCode

# 这是一个标准的心形 SVG 路径
heart_path = (
    "path://M10,30 A20,20 0,0,1 50,30 A20,20 0,0,1 90,30 Q90,60 50,90 Q10,60 10,30 z"
)#SVG路径
c = (
    Liquid(
        init_opts=opts.InitOpts(
            # theme=opts.ThemeType.DARK,
            width="600px",
            height="800px",
            bg_color="#3b2c3c",
        )
    )

    .add("Liquid",#添加液体图
          [0.3, 0.7], # 液体图数据
         is_outline_show=False, #是否显示外轮廓
        #shape=SymbolType.DIAMOND #默认情况为圆形
        shape=heart_path,# 设置图形为心形
        # shape=SymbolType.ARROW, # 设置图形为箭头
        # shape=SymbolType.RECT # 设置图形为矩形
        color=['#ff0000', '#ff8080'], # 设置液体颜色
        outline_border_distance=10, #轮廓与水滴间距
        label_opts=opts.LabelOpts(
            font_size=50,
            formatter=JsCode(
                """function(params){
                return (Math.floor(params.value * 100) + '%');
                }"""
            ),
            position="inside", #标签位置
            color="#fff", #标签颜色
        ),
    )
    
    .set_global_opts(title_opts=opts.TitleOpts(title="Liquid-Shape-Heart"),

                     legend_opts=opts.LegendOpts(is_show=False), #不显示图例
                     )
    .set_series_opts( #设置系列选项
        label_opts=opts.LabelOpts( #设置标签选项
            is_show=True,
            position="inside", #标签位置
            font_size=20,
            color="#fff",
        )
    )
    .render("html/liquid_pyecharts1.html")
)