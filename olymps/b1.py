data = open('b1.txt').readlines()
n = int(data[0])
arr = [list(map(int, data[i + 1].split())) for i in range(n)]
ans = [[0] * n for _ in range(n)]
sums = [[0] * (2 * n - 1) for _ in range(2 * n - 1)]
gor = [[0] * n for _ in range(n)]
ver = [[0] * n for _ in range(n)]
for i in range(n // 3):
    for j in range(n):
        gor[3 * i + 2][j] = arr[3 * i + 1][j] - arr[3 * i][j] - (gor[3 * i - 1][j] if i > 1 else 0)
        gor[- 3 * i - 3][j] = arr[- 3 * i - 2][j] - arr[- 3 * i - 1][j] - (gor[- 3 * i][j] if i > 1 else 0)
    for j in range(n):
        ver[j][3 * i + 2] = arr[j][3 * i + 1] - arr[j][3 * i] - (ver[3 * i - 1][j] if i > 1 else 0)
        ver[j][- 3 * i - 3] = arr[j][- 3 * i - 2] - arr[j][- 3 * i - 1] - (ver[- 3 * i][j] if i > 1 else 0)
for i in range(2, n - 2):
    for j in range(2, n - 2):
        ans[i][j] = gor[i][j - 1] - gor[i][j - 2] - ans[i][j - 2]  # from gor
        ans[i][j] = ver[i - 1][j] - ver[i - 2][j] - ans[i-2][j]  # from ver
print(*gor, sep='\n')
print()
print(*ver, sep='\n')
print()
print(*ans, sep='\n')
