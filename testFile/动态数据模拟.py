# 带条件的嵌套列表生成(模拟“动态数据过滤”)</b>
import numpy as np
import pandas as pd
# 模拟“学生成绩数据”,通过条件判断生成嵌套列表,再转换为DataFrame,演示“数据预处理+动态构造”场景。

student_raw = [
{"id": 1, "name":"Alice","scores": [85, 90, 92]},
{"id": 2, "name": "Lisa","scores":[100, 90, 92]},
{"id": 3, "name":"luxi","scores": [85, 89, 92]},
{"id": 4, "name": "xiaoming","scores": [85, 90, 78]}
]

#求某一科目的平均分
#需要嵌套列表完成
#指定列，学号，姓名，数学，语文，英语
#动态构造嵌套列表，只保留数学成绩不小于80且无缺失值的学生
filtered_student = []
for student in student_raw:
    math_score = student['scores'][0]
    if not pd.isna(math_score) and math_score >= 80:
        filtered_student.append(
            [
                student['id'],
                student['name'],
                student['scores'][0],
                student['scores'][1],
                student['scores'][2],
            ]
        )

#生成DataFrame并指定列名
scores_df = pd.DataFrame(
    filtered_student,
    columns=["学号", "姓名", "数学", "语文", "英语"]
)

print(scores_df)