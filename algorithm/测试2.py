# array = [[1,2,3],[8,9,4],[7,6,5]]
# [1,2,3,4,5,6,7,8,9]
# array = [[1,2,3],[8,9,4],[7,6,5]]
# array = [[3],[2]]
array = [
    [1,2,3,4],
    [12,13,14,5],
    [11,16,15,6],
    [10,9,8,7]]
# array = [[2, 3], [2]]

lis = []

if not array or not array[0]:
    print(list())
top, left, bottom, right = 0, 0, len(array) - 1, len(array[0]) - 1
while (left <= right and top <= bottom):
    # if top == left and left == bottom and right == top:
    #     lis.append(array[top][bottom])

    for j in range(left, right + 1):
        lis.append(array[top][j])
    
    for i in range(top + 1, bottom + 1):
        lis.append(array[i][right])

    if left < right and top < bottom:

        for j in range(right - 1, left, -1):
            lis.append(array[bottom][j])
        for i in range(bottom, top, -1):
            lis.append(array[i][top])
    top, left, bottom, right = top+1, left+1, bottom - 1, right - 1

print(lis)
# array = [[3],[2]]
# lis = []
# if not array or not array[0]:
#     print(lis)

# rows, columns = len(array), len(array[0])
# order = list()
# left, right, top, bottom = 0, columns - 1, 0, rows - 1
# while left <= right and top <= bottom:
#     for column in range(left, right + 1):
#         order.append(array[top][column])
#     for row in range(top + 1, bottom + 1):
#         order.append(array[row][right])
#     if left < right and top < bottom:
#         for column in range(right - 1, left, -1):
#             order.append(array[bottom][column])
#         for row in range(bottom, top, -1):
#             order.append(array[row][left])
#     left, right, top, bottom = left + 1, right - 1, top + 1, bottom - 1

# print(order)
