def main():
    blohi = []
    for i in range(30):
        for k in range(30):
            blohi.append([i, k])
    for i in range(50):
        for b in range(900):
            s = [[1, 0], [-1, 0], [0, 1], [0, -1]]
            if blohi[b][0] == 29:  s.remove([1, 0])
            elif blohi[b][0] == 0: s.remove([-1, 0])
            if blohi[b][1] == 29:  s.remove([0, 1])
            elif blohi[b][1] == 0: s.remove([0, -1])
            up, left = rand.choice(s)
            blohi[b][0] += up
            blohi[b][1] += left
    i = -1
    while i < len(blohi)-1:
        i += 1
        while blohi.count(blohi[i]) > 1:
            blohi.remove(blohi[i])
    return 900-len(blohi)


if __name__ == '__main__':
    import random as rand
    otvet = 0
    for ggg in range(50):
        answer = 0
        for gg in range(150):
            answer += main()
        otvet += answer
        print(ggg, ':', answer/150)
    print(otvet/7500)
    print('готово')
    input()
    # 330.551067