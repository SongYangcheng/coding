from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.globals import ChartType
import pandas as pd
import requests

district_codes = {
"上城区": "330102", "拱墅区": "330105", "西湖区": "330106",
"滨江区": "330108", "萧山区": "330109", "余杭区": "330110",
"临平区": "330113", "钱塘区": "330114", "富阳区": "330111",
"临安区": "330112", "桐庐县": "330122", "淳安县": "330127",
"建德市": "330182"

}
hangzhou_features = []
for district, code in district_codes.items():
    url = f"https://geo.datav.aliyun.com/areas_v3/bound/330100_full.json"
    try:
        res = requests.get(url).json()
        if "features" in res:
            hangzhou_features.extend(res['features'])
    except Exception as e:
        print(f"获取{district}数据失败: {e}")
    #创造完整杭州GeoJSON结构
    hangzhou_geo_json = {
        "type": "FeatureCollection",
        "features": hangzhou_features
    }
    #4. 数据与区县名称匹配
    hangzhou_data = [
    ("上城区",120),("拱墅区",95),("西湖区",150),
    ("滨江区",88),("萧山区",180),("余杭区",130),
    ("临平区",75),("钱塘区",60),("富阳区",105),
    ("临安区",90),("桐庐县",55),("淳安县",40),
    ("建德市",65)
    ]
    #渲染地图
    c = (
        Map(init_opts=opts.InitOpts(width="800px", height="600px"))
        .add_js_funcs(
            f"""echarts.registerMap('hangzhou-district', {hangzhou_geo_json});"""
    )
    .add(
        series_name="杭州各区县数据",
        data_pair=hangzhou_data,
        maptype="hangzhou-district",
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="杭州各区县数据分布图"),
        visualmap_opts=opts.VisualMapOpts(
            min_=30,
            max_=200,
            is_piecewise=True,
            pos_bottom=50,
    
        ),
        tooltip_opts=opts.TooltipOpts(
            trigger="item",
            formatter="{b}: {c}",
        ),
    )
    )
    c.render("html/Map_pyecharts3.html")