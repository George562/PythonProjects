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
            if b == 0:  # 6
                if a1 == 254 and b1 == 0:
                    if c < c1:
                        arr[i], arr[i + 1] = arr[i + 1], arr[i]
                        q = True
                else:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    q = True
            else:  # 1
                if a1 == 254 and c1 == 0:
                    if b1 < b:
                        arr[i], arr[i + 1] = arr[i + 1], arr[i]
                        q = True
        elif c == 254:
            if b == 0:  # 5
                if c1 == 254 and b1 == 0:
                    if a1 < a:
                        arr[i], arr[i + 1] = arr[i + 1], arr[i]
                        q = True
                else:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    q = True
            else:  # 4
                if c1 == 254:
                    if b < b1:
                        arr[i], arr[i + 1] = arr[i + 1], arr[i]
                        q = True
                else:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    q = True
        elif b == 254:
            if a == 0:  # 3
                if b1 == 254 and a1 == 0:
                    if c1 < c:
                        arr[i], arr[i + 1] = arr[i + 1], arr[i]
                        q = True
                else:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    q = True
            else:  # 2
                if b1 == 254:
                    if a < a1:
                        arr[i], arr[i + 1] = arr[i + 1], arr[i]
                        q = True
                else:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    q = True
    return q


color = [(254, a, 0) for a in range(0, 254, 2)] + [(a, 254, 0) for a in range(254, 0, -2)] + \
        [(0, 254, a) for a in range(0, 254, 2)] + [(0, a, 254) for a in range(254, 0, -2)] + \
        [(a, 0, 254) for a in range(0, 254, 2)] + [(254, 0, a) for a in range(254, 0, -2)]
scw, sch = 762, 512
sc = pg.display.set_mode((scw, sch))
sc.fill((0, 0, 0))
run = False
s = 0
permutation(color)
done = False
while not done:
    for j in range(s, len(color)):
        pg.draw.rect(sc, color[j], [(j - s), 0, 1, sch])
    for j in range(s):
        pg.draw.rect(sc, color[j], [scw - (s - j), 0, 1, sch])
    # s = (s+1) % len(color)
    sort(color)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
    pg.display.flip()
