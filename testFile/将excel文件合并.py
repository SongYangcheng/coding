import pandas as pd

# 1. 读取两个Excel文件,保留原始列结构(不提前处理索引等,先获取完整数据)
df_new = pd. read_excel('phones_new. xlsx' )
df_old = pd. read_excel('phone_old.xlsx' )

# 2. 打印查看两个文件原始的列名,目的是发现列名中可能存在的空格等差异问题
print("新文件原始列名(含空格):",df_new.columns.tolist())
print("旧文件原始列名(无空格):",df_old.columns.tolist())

# 3. 核心步骤:处理列名中的空格(包括列前后的空格以及中问可能存在的空格)
# 对新文件的列名,先去除前后空格,再替换掉中间的空格
df_new.columns = df_new.columns.str.strip().str.replace(' ', '')
# 对旧文件的列名也进行同样的处理
df_old.columns = df_old.columns.str.strip().str.replace(' ', '')

#打印处理后文件列名
print("处理后新文件列名：", df_new.columns.tolist())
print("处理后旧文件列名：", df_old.columns.tolist())

standard_columns = df_old.columns.tolist()

for col in df_new.columns:
    if col not in standard_columns:
        df_new = df_new.drop(columns=col)
        print(f"已删除新文件的冗余列：{col}") #会存在unnamed：0冗余列

#合并两个DataFrame数据
df_combined = pd.concat([df_new, df_old], ignore_index=True)

#将合并的数据写入新的excel文件， index=True表示保留索引列

df_combined.to_excel('phones_conbined_final.xlsx', index=True)

#打印最终合并的数据验证合并结果是否正确
print(df_combined)
print("合成最终文件")