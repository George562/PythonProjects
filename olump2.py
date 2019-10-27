n = int(input())
a = input().split()
inter = [int(i) for i in a]
a = input().split()
out = [int(i) for i in a]  # ввод
run = False
for i in range(n):
    if out[i] != i+1:  # первая проверка
        run = True
        break
m = 0
timer = 0
while run or timer != 0:
    run = False
    m += 1
    done = False
    if timer != 0:
        timer -= 1
    inter.insert(0, out.pop(0))
    if 1 in inter:  # если у меня есть 1, то ждем пока появятся остальные
        for i in range(2, max(inter)+1):
            if i not in inter:
                if out.index(i) >= i-1:
                    timer = i-out.index(i)+1
                    break
    if timer == 0:
        for i in range(1, n+1):
            if inter[i]-1 == out[n-2] and not done:
                out.append(inter.pop(i))
                done = True
                break
        if not done:
            out.append(inter.pop(inter.index(0)))
        for i in range(n):  # проверка
            if out[i] != i+1:
                run = True
                break
    else:
        out.append(inter.pop(inter.index(0)))
print(m)
