s = int(input())
nums = [int(input()) for _ in range(s)]
ans = []
h = {}
a = set(nums)
for i in a:
    h[i] = nums.count(i)
print(h)
s = 0
d = h.keys()
for i in range(len(d)-1):
    if h[d[i]] != 0:
        if h[d[i]] == 1:
            s += 1
        elif h[d[i]] == 2:
            if (d[i] != s and d[i] != 1 and (d[i]+1 not in d or d[i]-1 in d)) or (d[i] == 1 and 2 not in d) or (d[i] == s and s-1 not in d):
                s += 2
            elif
print(s)

for x in sorted(nums):
    a, b = x-1 if x != 1 else 1, x+1 if x != s else s
    if a not in ans:
        ans.append(a)
    elif x not in ans:
        ans.append(x)
    elif b not in ans:
        ans.append(b)
print(len(ans))
input()