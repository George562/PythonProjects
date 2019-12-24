ans = set()
s = int(input())
for _ in range(s):
    x = int(input())
    a, b = x-1 if x != 1 else 1, x+1
    ans |= {a, x, b}
print(len(ans) if len(ans) < s else s)
