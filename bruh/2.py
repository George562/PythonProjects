ans = {}
k = int(input())
for i in range(k):
    a = list(input())
    b = a.copy()
    b.sort()
    b = ''.join(b)
    if b in ans:
        ans[b].append(''.join(a))
    else:
        ans[b] = [''.join(a)]
print(len(ans))
for i in ans:
    print(*ans[i])
