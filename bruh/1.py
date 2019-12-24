m, n, k = [int(i) for i in input().split()]
kv = [int(i) for i in input().split()]
ans = []
now = (n - 1) * m + 1
for q in range(n):
    a = input().split()
    i = 0
    for j in range(m):
        now = (n - q - 1) * m + 1 + j
        for k in range(kv[j]):
            if a[i+k] == '1':
                break
        else:
            ans.append(now)
        i += kv[j]
print(len(ans))
print(*sorted(ans), sep=' ')
