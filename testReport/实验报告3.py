import pandas as pd

df = pd.read_csv(r"data/orders.csv")
print("=============================1.前五行数据打印===============================")
#前五行数据打印
print(df.head())
print("=============================2.总价的求解===============================")
#总价的求解
df["总价"] = df["单价"] * df["数量"] ** (1 - df["折扣比例"])
print(df.head())
print("============================#3.统计每列缺失值数量=====================================")
#统计每列缺失值数量
Nan_number = df.isnull().sum()
print(Nan_number)
print("============================4.将城市列的缺失值填充为未知，将折扣比列和运费的缺失值改为各自的平均值=====================================")

df = df.fillna(value={"城市":"未知"})
mean_discount = df["折扣比例"].mean()
mean_freight = df["运费"].mean()
df = df.fillna(value={"折扣比例":mean_discount})
df = df.fillna(value={"运费":mean_freight})
print(df.head())
print("============================5.删除重复订单只保留最后一次=====================================")
print(df.drop_duplicates(subset=["订单编号"], keep="last"))
print("=============================6.按照品类进行分组===============================")
df_group = df.groupby("品类").agg(
    订单数量 = ("数量","sum"),
    平均单价 = ("单价","mean"),
    总订单金额 = ("总价","sum")
)
print(df_group)
print("===========7.输出总订单金额最大的====================")
#找出已支付订单
paid = df[(df["订单状态"] == "paid")]
#对已支付订单进行品类分组
paid_group = paid.groupby("品类")["总价"].sum()
print(paid_group.idxmax())