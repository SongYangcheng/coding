import numpy as np

import csv

import numpy as np
import csv

#从CSV文件读取学生成绩数据
def read_student_grades(filename):
    student_data = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
        #提取学号、姓名和各科成绩
            student = {
            'id':row['学号'],
            'name': row['姓名'],
            'gender': row['性别'],
            'age': int(row['年龄']),
            'class': row['班级'],
            'chinese': float(row['语文成绩']),
            'math':float(row['数学成绩']),
            'english': float(row['英语成绩']),
            'total':float(row['总分'])}

            student_data.append(student)
    return student_data

#读取学生数据(确保CSV文件名为“学生信息.csv",与生成代码一致)
student_data = read_student_grades('d:/python_demo/coding/testFile/学生信息.csv')

#提取各科成绩到NumPy数组
chinese_scores = np.array( [s['chinese'] for s in student_data])
math_scores = np.array([s['math'] for s in student_data])
english_scores = np.array([s['english'] for s in student_data])
total_scores = np.array([s['total'] for s in student_data])
ages = np.array( [s['age' ] for s in student_data])
# 添加一些特殊值用于演示(模拟可能的数据异常)
math_with_anomalies = math_scores.copy()
math_with_anomalies[3] = np.nan
math_with_anomalies [7] = np.inf

print("学生数量:",len(student_data))
print("语文成绩:",chinese_scores)
print("数学成绩(含异常值):",math_with_anomalies)
print("英语成绩:",english_scores)
print("总成绩:",total_scores)
print("年龄:",ages)
print("\n ----绝对值相关函数-----")
chinese_diff = chinese_scores - np.mean(chinese_scores)
print("语文成绩与平均分差值的绝对值(abs):",np.abs(chinese_diff))
print("语文成绩与平均分差值的绝对值(fabs):",np.fabs(chinese_diff))

#2. 幂函数相关
print("\n --- 幂函数相关 --- ")
print("语文成绩的平方根(sqrt):",np.sqrt(chinese_scores))
print("数学成绩的平方根(square):",np.square(math_scores))

# 3. 指数和对数函数
print("\n --- 指数和对数函数 --- ")
print("英语成绩的指数转换(exp)",np.exp(english_scores/ 10)) #除以10防止数值过大
print("总成绩的自然对数(log):",np.log(total_scores))
print("总成绩以10为底的对数(l0g10):",np.log10(total_scores))
print("总成绩以2为底的对数(10g2):",np.log2(total_scores))

# 4. 符号和取整函数(满分为150分)
print("\n --- 符号和取整函数 --- ")
print("与满分(150分)差值的符号(sign):",np.sign(150- math_scores))
print("语文成绩向上取整(ceil):",np.ceil(chinese_scores))
print("数学成绩向下取整(floor):",np.floor(math_scores))
print("英语成绩四舍五入(rint):",np.rint(english_scores))

# 5. 小数和整数部分分离
print("\n --- 小数和整数部分 --- ")
math_frac, math_integ= np.modf(math_scores)
print("数学成绩的小数部分:",math_frac)
print("数学成绩的整数部分:",math_integ)

# 6. 特殊值判断
print("\n --- 特殊值判断 --- ")
print("数学成绩中是否有NaN值(isnan):",np.isnan(math_with_anomalies))
print("数学成绩中是否为有限值(isfinite):", np.isfinite(math_with_anomalies))
print("数学成绩中是否无无限值(isinf):",np.isinf(math_with_anomalies))

# 7. 三角函数
print("\n --- 三角函数 --- ")
normalized = (math_scores - np.min(math_scores)) / (np.max(math_scores) - np.min(math_scores)) * np.pi
print("归一化成绩的正弦值(sin):", np.sin(normalized))
print("归一化成绩的余弦值(cos):", np.cos(normalized))
print("归一化成绩的正切值(tan):", np.tan(normalized))

# 8. 双曲函数
print("\n --- 双曲函数 --- ")
print("归一化成绩的双曲正弦值(sinh):", np.sinh(normalized))

print("归一化成绩的双曲余弦值(cosh):",np.cosh(normalized))
print("归一化成绩的双曲正切值(tanh):",np.tanh(normalized))

# 9. 反三角函数
print("\n --- 反三角函数 --- ")
norm_for_trig = (math_scores - np.mean(math_scores)) / (np.max(math_scores) - np.min(math_scores))
norm_for_trig = np.clip(norm_for_trig, -1, 1)
print("归一化成绩的反正弦值(arcsin):", np.arcsin(norm_for_trig))
print("归一化成绩的反余弦值(arccos):", np.arccos(norm_for_trig))

# 10. 离散值和标准差
print("\n --- 离散值和标准差 --- ")
print("语文成绩的一阶离散差(diff):",np.diff(chinese_scores))
print("数学成绩的标准差(std):",np.std(math_scores))
print("英语成绩的二阶离散差(diff):",np.diff(english_scores, n=2))

# 额外:反双曲余弦函数(缩放分母为150)
print("\n --- 反双曲余弦函数 --- ")
print("总成绩的反双曲余弦值(arccosh):",np.arccosh(total_scores /150))