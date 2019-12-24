ans = set()
s = int(input())
a = [0]*(5*10**5)
d = 0
for _ in range(s):
    x = int(input())
    if (x == 1 and a[0] == 2) or (x > 1 and a[x-1] == 3):
        d += 1
    else:
        a[x-1] += 1
    ans |= {x-1 if x > 2 else 1, x, x+1}
t = 0
for i in sorted(list(ans)):
    if i == 1:
        if a[0]+a[1] >= 3:
            t += a[0]+a[1]-3
            if a[2] >= 2:
                t += a[2]-1
    if i > 2:
        if a[i-2]+a[i] >= 5:
            t += a[i-1]+a[i-2]+a[i]-5
            a[i-1] = 0
        elif a[i-2]+a[i] == 4 and a[i-1] > 1:
            t += a[i-1]-1
            a[i-1] = 0
print(min(len(ans), s-d-t))
