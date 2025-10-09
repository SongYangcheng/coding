import json
with open('./article.txt','r',encoding='utf-8') as f:
    data = f.read().replace("\n", " ")
pure_data = list()
dict_data = dict()
lis_3 = list()
lis_5_10 = list()
lis_10 = list()
# print(data)
for i in data.split(" "):
    
    
    # print(i)
    i = i.strip(",").strip(".").strip("”").strip("“").strip(")").strip("(").lower()
    
    pure_data.extend(i.split("—"))

# print(pure_data)
for i in pure_data:
    if len(i) > 3:
        dict_data[i] = pure_data.count(i)
dict_data_sort = dict(sorted(dict_data.items(), key=lambda x:x[1], reverse=True))

for key, value in dict_data_sort.items():
    # print(len(key))
    if len(key) > 3:
        lis_3.append((key, value))
        if len(key) <= 10 and len(key) >= 5:
            lis_5_10.append((key, value))
        if len(key) > 10:
            lis_10.append((key, value))

# print(lis_10, "\n", lis_3)
print("单词长度大于3的出现频率最高的5个单词： ",lis_3[0:5])
print("单词长度在5到10之间，频率最高的5个单词：", lis_5_10[0:5])
print("单词长度大于10，频率最高的5个单词：", lis_10[0:5])
