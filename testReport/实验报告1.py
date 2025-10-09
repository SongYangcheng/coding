#coding:utf-8
import json
with open("./datas.txt", "r", encoding="utf-8") as f:
    data = json.load(f)

mydict = {}
#将省名和空列表写入字典
for i in data:
    if i[1][2:3] == "省" or i[1][2:3] == "市" or i[1][2:3] == "古" or i[1][2:3] == "江":
        mydict.update({i[1][:3]:[ ]})
    else:
        mydict.update({i[1][:2]:[ ]})
#遍历个元素判断是那个省，并将其写入value
for key in mydict.keys():
    for i in data:
        if key == i[1][:3] or key == i[1][:2]:
            mydict[key].append(i)
#输出
print("{")
for key, value in mydict.items():
    print("  \"%s\":[" %(key))
    for i in value:
        print("      %s,"%(i))
    
    if(key == "海南省"):
        print("]")
    else:
        print("],")
print("}")