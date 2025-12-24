
n, m = map(int, input().split(" "))
lis = []
for i in range(n):
    lis.append(list(map(int, input().split(" "))))
#按每列
p_i = []
for j in range(n):
    num = 0
    for i in range(m):
        num += lis[i][j]
    p_i.append(num)

min_i = float("inf")
for i in range(n-1):
    x = p_i[i + 1] - p_i[i]
    if min_i >= x:
        min_i = x
print(p_i)
p_j = []
for i in range(m):
    num = 0
    for j in range(n):
        num += lis[i][j]
    p_j.append(num)

min_j = float("inf")
for i in range(m-1):
    x = p_j[i + 1] - p_j[i]
    if min_j >= x:
        min_j = x
print(min(min_i, min_j))
print(p_j)