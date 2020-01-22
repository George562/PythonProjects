import pygame as pg
from math import hypot, cos, sin, atan2
from time import time

def zoom(do):
    x, y = pg.mouse.get_pos()
    if do:
        for i in range(len(arr)):
            arr[i] = (arr[i][0]-x)*1.05+x, (arr[i][1]-y)*1.05+y, arr[i][2]
    else:
        for i in range(len(arr)):
            arr[i] = (arr[i][0]-x)/1.05+x, (arr[i][1]-y)/1.05+y, arr[i][2]

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
z = 1
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
    for i in range(len(arr)-1):
        if 0 <= arr[i][0] <= scw and 0 <= arr[i][1] <= sch or 0 <= arr[i+1][0] <= scw and 0 <= arr[i+1][1] <= sch:
            pg.draw.line(sc, (255, 255, 255), arr[i][0:2], arr[i+1][0:2])
            if all([0 <= arr[i][0] <= scw, 0 <= arr[i][1] <= sch, 0 <= arr[i+1][0] <= scw, 0 <= arr[i+1][1] <= sch]):
                dh = hypot(arr[i][0]-arr[i+1][0], arr[i][1]-arr[i+1][1])
                if dh > 20:
                    dop = lom(*arr[i], *arr[i+1])
                    for j in range(3):
                        arr.insert(i+j+1, dop[j])
                elif dh < 0.1:
                    letDel = True
    if 0 <= arr[0][0] <= scw and 0 <= arr[0][1] <= sch or 0 <= arr[-1][0] <= scw and 0 <= arr[-1][1] <= sch:
        pg.draw.line(sc, (255, 255, 255), arr[-1][0:2], arr[0][0:2])
        if all([0 <= arr[0][0] <= scw, 0 <= arr[0][1] <= sch, 0 <= arr[-1][0] <= scw, 0 <= arr[-1][1] <= sch]):
            dh = hypot(arr[0][0] - arr[-1][0], arr[0][1] - arr[-1][1])
            if dh > 20:
                dop = lom(*arr[-1], *arr[0])
                for j in range(3):
                    arr.append(dop[j])
            elif dh < 0.1:
                letDel = True
    if letDel and topColeno > 5:
        for i in range(len(arr)-1, -1, -1):
            if arr[i][2] >= topColeno-1:
                arr.pop(i)
        topColeno -= 1
    if pg.mouse.get_pressed()[0]:
        zoom(True)
        z *= 1.05
    if pg.mouse.get_pressed()[2]:
        zoom(False)
        z /= 1.05
    for e in pg.event.get():
        if e.type == pg.QUIT:
            done = True
    pg.display.flip()
    clock.tick(30)
