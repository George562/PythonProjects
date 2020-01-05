from math import cos, sin, pi
import pygame
import random


def zoom(do):
    x, y = pg.mouse.get_pos()
    if do:
        for i in range(len(arr)):
            arr[i] = (arr[i][0]-x)*1.05+x, (arr[i][1]-y)*1.05+y
    else:
        for i in range(len(arr)):
            arr[i] = (arr[i][0]-x)/1.05+x, (arr[i][1]-y)/1.05+y


def fractal(depth):
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
            arr.insert(i+3, (x+rx*2/3, y+ry*2/3))
        x, y, x1, y1 = *arr[-1], *arr[0]
        rx, ry = (x1-x), (y1-y)
        angle = -atan2(rx, ry)
        arr.append((x+rx/3, y+ry/3))
        arr.append(((x+x1)/2+cos(angle)*h/3, (y+y1)/2+sin(angle)*h/3))
        arr.append((x+rx*2/3, y+ry*2/3))
        fractal(depth-1)


def three(point, ang, deep=10, pha=pi, st_deep=None, l=None):
    st_deep = st_deep or deep
    x, y = point
    leng = l or 150
    color = green if deep > 0 else red
    if random.randint(0, 100) >= 10:
        pygame.draw.line(screen, color, point, (x-cos(pha-ang)*leng, y-sin(pha-ang)*leng), 2)
        if deep != 0:
            three((x-cos(pha-ang)*leng, y-sin(pha-ang)*leng), ang, deep-1, pha+(pi/2-ang), st_deep, 3*leng/4)
    if random.randint(0, 100) >= 10:
        pygame.draw.line(screen, color, point, (x+cos(pha+ang)*leng, y+sin(pha+ang)*leng), 2)
        if deep != 0:
            three((x+cos(pha+ang)*leng, y+sin(pha+ang)*leng), ang, deep-1, pha-(pi/2-ang), st_deep, 3*leng/4)


def figure_turn(points, alpha, deep=10):
    arr = points[0]
    le = len(points)
    if deep < 1:
        return
    for i in range(le-1):
        pygame.draw.line(screen, white, points[i], points[i + 1])
    pygame.draw.line(screen, white, points[le - 1], points[0])
    for i in range(le-1):
        points[i] = [points[i][0]*(1-alpha)+points[i+1][0]*alpha, points[i][1]*(1-alpha)+points[i+1][1]*alpha]
    points[le-1] = [points[le-1][0]*(1-alpha)+arr[0]*alpha, points[le-1][1]*(1-alpha)+arr[1]*alpha]
    figure_turn(points, deep-1)


pygame.init()
screen = pygame.display.set_mode((1200, 950))
white = (255, 255, 255)
green = (50, 255, 50)
red = (255, 50, 50)
black = (5, 5, 15)
a = 1
num = 10

done = False
while not done:
    screen.fill((50, 50, 50))
    three((600, 575), pi/2-2*pi*(a/15000), num)
    pygame.display.update()
    a += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k and num != 0:
                num -= 1
            elif event.key == pygame.K_l:
                num += 1
    pygame.display.update()
pygame.quit()
