
# [
#     [1, 2, 3, 4,]
#     [12, 13, 14, 5,]
#     [11, 16, 15, 6,]
#     [10, 9, 8, 7,]

# ]


n = 3
lis = [[0] * n for _ in range(n)]
circle = n // 2  # 修正拼写错误
start_i = 0      # 修正拼写错误
start_j = 0      # 修正拼写错误
count = 1

# 特殊情况：当n=1时，直接设置中心点
if n == 1:
    lis[0][0] = 1
    print(lis)
else:
    for layer in range(circle):
        # 当前层的起始位置
        i = start_i + layer
        j = start_j + layer
        
        # 当前层的边长
        length = n - 2 * layer
            

        # 向右移动（顶边）
        for _ in range(length - 1):
            lis[i][j] = count
            count += 1
            j += 1
        
        # 向下移动（右边）
        for _ in range(length - 1):
            lis[i][j] = count
            count += 1
            i += 1
        
        # 向左移动（底边）
        for _ in range(length - 1):
            lis[i][j] = count
            count += 1 
            j -= 1

        # 向上移动（左边）
        for _ in range(length - 1):
            lis[i][j] = count
            count += 1
            i -= 1
    
    # 处理奇数情况的中心点（如果还没有被处理）
    if n % 2 == 1:
        lis[n//2][n//2] = count

# 打印结果
print(lis)
