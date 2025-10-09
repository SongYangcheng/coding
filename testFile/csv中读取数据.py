import numpy as np
import pandas as pd
from io import StringIO

# 模拟 CSV 内容(用户基础信息)
csv_content = """
user_id,name,register_date
1,Alice, 2025-01-01
2,Bob, 2025-01-02
3,Charlie, 2025-01-03
4,Dave, 2025-01-04
"""
# 从 CSV 读取数据
user_df = pd.read_csv(StringIO(csv_content), parse_dates=["register_date"])

print(user_df)
# 构造结构数组(用户行为补充数据)
behavior_dtype = [('user_id', 'i4'), 
                  ('daily_visits', 'i4'),
                    ('avg_duration', 'f4')]
# behavior_data = np.zeros(4, dtype=behavior_dtype)
# print(behavior_data)
#[:] 相当于取全部数据
behavior_data = np.array([
(1, 5, 10.5),
(2, 3, 8.2),
(3, 7, 12.1),
(4, 2, 5.3)
], dtype=behavior_dtype)

print(behavior_data)
behavior_df = pd.DataFrame(behavior_data) # /DataFrame
print(behavior_df)
# 合并两个 DataFrame(按user_id 关联)
merged_df = pd.merge(user_df, behavior_df, on="user_id")
print("案例：CSV读取+结构数组整合")
print(merged_df)
