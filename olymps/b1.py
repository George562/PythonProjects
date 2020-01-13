from random import randint

n = 5
wasArr = [[randint(1, 9) for _ in range(n)] for _ in range(n)]
arr = [[0] * n for _ in range(n)]
for y in range(n):
    for x in range(n):
        start_y, end_y = 0 if y == 0 else y - 1, y + 2 if y < n - 1 else y + 1
        start_x, end_x = 0 if x == 0 else x - 1, x + 2 if x < n - 1 else x + 1
        arr[y][x] = sum(wasArr[i][j] for i in range(start_y, end_y) for j in range(start_x, end_x))
for i in wasArr:
    print(*i)
print()
for i in arr:
    print(*i)
print()
ans = [[0] * n for _ in range(n)]
gor = [[0] * n for _ in range(n)]
ver = [[0] * n for _ in range(n)]
for i in range(n // 3):
    for j in range(n):
        gor[3 * i + 2][j] = arr[3 * i + 1][j] - arr[3 * i][j] + (gor[3 * i - 1][j] if i > 0 else 0)
        gor[- 3 * i - 3][j] = arr[- 3 * i - 2][j] - arr[- 3 * i - 1][j] + (gor[- 3 * i][j] if i > 0 else 0)
    for j in range(n):
        ver[j][3 * i + 2] = arr[j][3 * i + 1] - arr[j][3 * i] + (ver[j][3 * i - 1] if i > 0 else 0)
        ver[j][- 3 * i - 3] = arr[j][- 3 * i - 2] - arr[j][- 3 * i - 1] + (ver[j][- 3 * i] if i > 0 else 0)
for i in range(1, n // 3 + 1):
    for j in range(1, n // 3 + 1):
        ans[i * 3 - 1][j * 3 - 1] = ver[i * 3 - 2][j * 3 - 1] - ver[i * 3 - 3][j * 3 - 1] + ans[i * 3 - 4][j * 3 - 1]  # from ver
        ans[- i * 3][- j * 3] = ver[- i * 3 + 1][- j * 3] - ver[- i * 3 + 2][- j * 3] + ans[- i * 3 + 3][- j * 3]  # from ver
        if n % 3 != 2:
            ans[i * 3 - 1][- j * 3] = ver[i * 3 - 2][- j * 3] - ver[i * 3 - 3][- j * 3] + ans[i * 3 - 4][- j * 3]  # from ver
            ans[- i * 3][j * 3 - 1] = ver[- i * 3 + 1][j * 3 - 1] - ver[- i * 3 + 2][j * 3 - 1] + ans[- i * 3 + 3][j * 3 - 1]  # from ver
if n % 3 == 1:
    for i in range(n // 3):
        for j in range(n // 3):
            ans[3 * i][3 * j + 1] = ver[3 * i + 1][3 * j + 1] - ans[3 * i + 1][3 * j + 1] - ans[3 * i + 2][3 * j + 1]
            ans[3 * i][3 * j + 2] = ver[3 * i + 1][3 * j + 2] - ans[3 * i + 1][3 * j + 2] - ans[3 * i + 2][3 * j + 2]
            ans[3 * i + 1][3 * j] = gor[3 * i + 1][3 * j + 1] - ans[3 * i + 1][3 * j + 1] - ans[3 * i + 1][3 * j + 2]
            ans[3 * i + 2][3 * j] = gor[3 * i + 2][3 * j + 1] - ans[3 * i + 2][3 * j + 1] - ans[3 * i + 2][3 * j + 2]
        ans[-1][3 * i + 1] = ver[-2][3 * i + 1] - ans[-2][3 * i + 1] - ans[-3][3 * i + 1]
        ans[-1][3 * i + 2] = ver[-2][3 * i + 2] - ans[-2][3 * i + 2] - ans[-3][3 * i + 2]
        ans[3 * i + 1][-1] = gor[3 * i + 1][-2] - ans[3 * i + 1][-2] - ans[3 * i + 1][-3]
        ans[3 * i + 2][-1] = gor[3 * i + 2][-2] - ans[3 * i + 2][-2] - ans[3 * i + 2][-3]
    for y in range(n // 3 + 1):
        for x in range(n // 3 + 1):
            start_y, end_y = 0 if y == 0 else y*3 - 1, y*3 + 2 if y*3 < n - 1 else y*3 + 1
            start_x, end_x = 0 if x == 0 else x*3 - 1, x*3 + 2 if x*3 < n - 1 else x*3 + 1
            ans[3*y][3*x] = arr[3*y][3*x] - sum(ans[i][j] for i in range(start_y, end_y) for j in range(start_x, end_x))
elif n % 3 == 0:
    for i in range(n // 3):
        for j in range(n // 3):
            ans[3*i][3*j+1] = gor[3*i][3*j+1] - ans[3*i][3*j] - ans[3*i][3*j+2]
            ans[-3*i-1][3*j+1] = gor[-3*i-1][3*j+1] - ans[-3*i-1][3*j] - ans[-3*i-1][3*j+2]
            ans[3*j+1][3*i] = ver[3*j+1][3*i] - ans[3*j][3*i] - ans[3*j+2][3*i]
            ans[3*j+1][-3*i-1] = ver[3*j+1][-3*i-1] - ans[3*j][-3*i-1] - ans[3*j+2][-3*i-1]
    for y in range(n // 3):
        for x in range(n // 3):
            ans[3*y+1][3*x+1] = arr[3*y+1][3*x+1] - sum(ans[i+1][j+1] for i in range(y*3-1, y*3+2) for j in range(x*3-1, x*3+2))
else:
    pass  # ToDo
# print(*gor, sep='\n')
# print()
# print(*ver, sep='\n')
# print()
for i in ans:
    print(*i)
print(ans == wasArr)
