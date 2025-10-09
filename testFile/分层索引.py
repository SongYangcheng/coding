import numpy as np
import pandas as pd

sales_data = {
'华东':{"2025-01":5000,"2025-02":5200,"2025-03":5500},
'华北':{"2025-01":4800,"2025-02":4900,"2025-03":5100},
'华南':{"2025-01":6000,"2025-02":6100,"2025-03":6300}
}

#生成多层索引

regions = list(sales_data.keys())
months = list(sales_data["华东"].keys())

#创建分层索引

multi_index = pd.MultiIndex.from_product([regions, months], names=["区域","月份"])

#展平嵌套字典为单层字典
flattened_data = {
}

for regions, month_data in  sales_data.items():
    for month, sales in month_data.items():
        flattened_data[(regions, month)] = sales
print(flattened_data)
#生成带分层的索引DataFrame
sales_df = pd.DataFrame(
    data={"销售额":flattened_data},
    index=multi_index
)

print("======分层索引+嵌套字典生成======")
print(sales_df)
print("按照区域分组求和")
print(sales_df.groupby("区域").sum())