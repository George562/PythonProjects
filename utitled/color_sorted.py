import pygame as pg
import random as rd

pg.init()


def permutation(arr):
    t = len(arr)
    for i in range(t):
        k = rd.randint(0, t - 1)
        arr[k], arr[i] = arr[i], arr[k]


def sort(arr):
    q = False
    for i in range(len(arr) - 1):
        a, b, c = arr[i]
        a1, b1, c1 = arr[i + 1]
        if a == 254:
            if b == 0 and c != 0:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]  # 6 to 1-5
                q = True
        elif b == 254:
            if b1 == 254:
                if c1 == 0:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]  # 3 to 2
                    q = True
            elif a1 == 254 and c1 != 0:
                if a != 0:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]  # 2 to 1, 4-6
                    q = True
                else:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]  # 3 to 1, 4-6
        elif c == 254:
            if c1 == 254:
                if a1 == 0:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]  # 5 to 4
                    q = True
            elif a1 == 254 and b1 != 0:
                if b != 0:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]  # 4 to 1, 2, 5-6
                    q = True
                else:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]  # 5 to 1-4, 6
                    q = True
        elif a == a1:
            if b == b1:
                if c < c1:
                    if b < a:
                        arr[i], arr[i + 1] = arr[i + 1], arr[i]  # 6
                        q = True
                elif c1 < c:
                    if a < b:
                        arr[i], arr[i + 1] = arr[i], arr[i + 1]  # 3
                        q = True
            elif c == c1:
                if b1 < b:
                    if c < a:
                        arr[i], arr[i + 1] = arr[i + 1], arr[i]  # 1
                        q = True
                if b < b1:
                    if a < c:
                        arr[i], arr[i + 1] = arr[i + 1], arr[i]  # 4
                        q = True
        elif b == b1:
            if c == c1 == 0:
                if a1 < a:
                    if b < c:
                        arr[i], arr[i + 1] = arr[i + 1], arr[i]  # 5
                        q = True
                if a < a1:
                    if c > b:
                        arr[i], arr[i + 1] = arr[i + 1], arr[i]  # 2
                        q = True
    return q


scw, sch = 1524, 512
sc = pg.display.set_mode((scw, sch))
color = [(254, a, 0) for a in range(0, 254, 2)] + [(a, 254, 0) for a in range(254, 0, -2)] + \
        [(0, 254, a) for a in range(0, 254, 2)] + [(0, a, 254) for a in range(254, 0, -2)] + \
        [(a, 0, 254) for a in range(0, 254, 2)] + [(254, 0, a) for a in range(254, 0, -2)]
sc.fill((0, 0, 0))
run = False
s = 0
done = False
while not done:
    for j in range(s, len(color)):
        pg.draw.rect(sc, color[j], [2 * (j - s), 0, 2, sch])
    for j in range(s):
        pg.draw.rect(sc, color[j], [scw - 2 * (s - j), 0, 2, sch])
    # s = (s+1) % len(color)
    sort(color)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
    pg.display.flip()
