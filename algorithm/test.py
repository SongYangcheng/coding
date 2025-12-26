import heapq
n, k = list(map(int, input().split(" ")))
arr = list(map(int, input().split(" ")))
n = len(arr)
if n == 0 or k <= 0:
    print([])

prefix = [0] * (n + 1)
for i in range(n):
    prefix[i+1] = prefix[i] + arr[i]
# print(prefix) 
prefix.sort()
min_heap = []
for i in range(n):
    diff = prefix[i+1] - prefix[i]
    heapq.heappush(min_heap, (diff, i, i+1))
print(min_heap)
result = []
for _ in range(k):
    if not min_heap:
        break
    val, i, j = heapq.heappop(min_heap)
    result.append(str(val))
    if j + 1 < n + 1:
        new_diff = prefix[j+1] - prefix[i]
        heapq.heappush(min_heap, (new_diff, i, j+1))
print(" ".join(result))