import pygame as pg
from math import hypot, cos, sin, atan2
from time import time


def zoom(do):
    x, y = pg.mouse.get_pos()
    if do:
        for i in range(len(arr)):
            arr[i] = (arr[i][0]-x)*1.05+x, (arr[i][1]-y)*1.05+y, *arr[i][2:]
    else:
        for i in range(len(arr)):
            arr[i] = (arr[i][0]-x)/1.05+x, (arr[i][1]-y)/1.05+y, *arr[i][2:]


def lom(x, y, c, x1, y1, c1):
    global topColeno
    if c+1 > topColeno:
        topColeno = c+1
        print(topColeno)
    h = hypot(x-x1, y-y1)
    rx, ry = (x1-x), (y1-y)
    angle = -atan2(rx, ry)
    return (x+rx/3, y+ry/3, c+1), ((x+x1)/2+cos(angle)*h/3, (y1+y)/2+sin(angle)*h/3, c+1), (x+rx*2/3, y+ry*2/3, c+1)


def fractal(depth):
    if depth > 0:
        for i in range(len(arr)-1):
            dop = lom(*arr[i*4], *arr[i*4+1])
            for j in range(3):
                arr.insert(i*4+j+1, dop[j])
        dop = lom(*arr[-1], *arr[0])
        for i in range(3):
            arr.append(dop[i])
        fractal(depth-1)


topTime = time()
scw, sch = 750, 750
sc = pg.display.set_mode((scw, sch))
d = 5
topColeno = 0
arr = [(scw/3, sch/3, 0), (scw*2/3, sch/3, 0), (scw/2, sch/3*(0.75**0.5)+sch/3, 0)]
fractal(d)
print(len(arr))
print(time()-topTime)
clock = pg.time.Clock()
done = False
while not done:
    sc.fill((0, 0, 0))
    letDel = False
    for i in range(-1, len(arr)-1):
        if 0 <= arr[i][0] <= scw and 0 <= arr[i][1] <= sch or 0 <= arr[i+1][0] <= scw and 0 <= arr[i+1][1] <= sch:
            pg.draw.line(sc, (255, 255, 255), arr[i][:2], arr[i+1][:2])
            if all([0 <= arr[i][0] <= scw, 0 <= arr[i][1] <= sch, 0 <= arr[i+1][0] <= scw, 0 <= arr[i+1][1] <= sch]):
                dh = hypot(arr[i][0]-arr[i+1][0], arr[i][1]-arr[i+1][1])
                if dh > 25:
                    dop = lom(*arr[i], *arr[i+1])
                    for j in range(3):
                        arr.insert(i+j+1, dop[j])
                if dh < 0.05:
                    letDel = True
    if letDel:
        if topColeno > 5:
            topColeno -= 1
            print(topColeno)
        for i in range(-len(arr), 0):
            if arr[i][2] > topColeno:
                arr.pop(i)
    if pg.mouse.get_pressed()[0]:
        zoom(True)
    if pg.mouse.get_pressed()[2]:
        zoom(False)
    if pg.mouse.get_pressed()[1]:
        relX, relY = pg.mouse.get_rel()
        arr = list(map(lambda i: (i[0] + relX, i[1] + relY, i[2]), arr))
    pg.mouse.get_rel()
    for e in pg.event.get():
        if e.type == pg.QUIT:
            done = True
    pg.display.flip()
    clock.tick(30)
