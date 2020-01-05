import pygame as pg
from math import hypot, cos, sin, atan2
import os
from time import time



def zoom(do):
    x, y = pg.mouse.get_pos()
    if do:
        for i in range(len(arr)):
            arr[i] = (arr[i][0]-x)*1.05+x, (arr[i][1]-y)*1.05+y
    else:
        for i in range(len(arr)):
            arr[i] = (arr[i][0]-x)/1.05+x, (arr[i][1]-y)/1.05+y


def fractal(depth, sd=0):
    print(depth, time()-t)
    if depth > 0:
        h = hypot(arr[0][0]-arr[1][0], arr[0][1]-arr[1][1])
        for i in arr.copy()[:len(arr)-1]:
            x, y, x1, y1 = *i, *arr[arr.index(i)+1]
            i = arr.index(i)
            rx, ry = (x1-x), (y1-y)
            angle = -atan2(rx, ry)
            arr.insert(i+1, (x+rx/3, y+ry/3))
            arr.insert(i+2, ((x+x1)/2+cos(angle)*h/3, (y1+y)/2+sin(angle)*h/3))
            if sd != 0:
                arr.insert(i+3, (x+rx*2/3, y+ry*2/3))
        fractal(depth-1, depth)


topTime = t = time()
scw, sch = 750, 750
sc = pg.display.set_mode((scw, sch))
z = 1
d = 9
arr = [(scw/3, sch/3), (scw*2/3, sch/3)]
fractal(d)
print(len(arr))
print(time()-topTime)
a = len(arr)//(3**(d))
clock = pg.time.Clock()
done = False
while not done:
    sc.fill((0, 0, 0))
    for i in range(0, len(arr)-1, int(a/z)+1):
        if 0 <= arr[i][0] <= scw and 0 <= arr[i][1] <= sch and 0 <= arr[i+1][0] <= scw and 0 <= arr[i+1][1] <= sch:
            pg.draw.line(sc, (255, 255, 255), arr[i], arr[i+1])
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
    clock.tick(60)
