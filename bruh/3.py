s = int(input())
nums = [int(input()) for _ in range(s)]
ans = []
for x in sorted(nums):
    a, b = x-1 if x != 1 else 1, x+1 if x != s else s
    if a not in ans:
        ans.append(a)
    elif x not in ans:
        ans.append(x)
    elif b not in ans:
        ans.append(b)
print(len(ans))
