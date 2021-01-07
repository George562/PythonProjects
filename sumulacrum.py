import math as mt
from random import randint
import matplotlib.pyplot as plt
import numpy as np
import pygame as pg

pg.init()

white = (255, 255, 255)
black = (0, 0, 0)
green = ((215, 255, 179), (202, 255, 153), (189, 255, 128), (176, 255, 102),
         (163, 255,  77), (150, 255,  51), (86,  179,   0), (74,  153,   0),
         (62,  128,   0), (49,  102,   0), (37,   77,   0), (25,   51,   0))

font = (lambda text, t_size=25: pg.font.SysFont("Roboto", t_size).render(str(text), True, white))
is_full = (lambda a: sum(a) // len(a))
mid_value = (lambda a, b, l: [a[i] / b[i] for i in range(l)])
sign = (lambda x: 1 if x > 0 else -1 if x < 0 else 0)

def graphic(a):
    pg.draw.line(sc, white, (N * size + 15, N * size - 115), (N * size + 15, N * size - 15))
    data = {i: a.count(i) for i in set(a)}
    for j, i in enumerate(sorted(data.keys())):
        pg.draw.rect(sc, white, (N * size + 15 + 30 * j + 5, N * size - 20, 8, -data[i] * 5))
        sc.blit(font(i, 20),    [N * size + 15 + 30 * j + 5, N * size - 15])

class Dude:
    dx = dy = 0
    Energy = 350
    cur_energy = Energy
    geneSpeed = 1  # ToDo
    genes = {
        "sens": 2
    }
    chances = {
        "sens": 35
    }
    found = False
    ate = 0
    need_eat = 2

    def __init__(self, genes=None):
        self.genes = genes or self.genes
        self.x = (N - 1) * randint(0, 1)
        self.y = randint(1, N - 2)
        if randint(0, 1) == 0:
            self.x, self.y = self.y, self.x
        self.target = (randint(1, N - 2), randint(1, N - 2))

    def draw(self):
        pg.draw.polygon(sc, (255, 50, 50), (
            ((self.x + 0.25) * size, (self.y + 0.75) * size),
            ((self.x + 0.5) * size, (self.y + 0.25) * size),
            ((self.x + 0.75) * size, (self.y + 0.75) * size)
        ))
        pg.draw.circle(sc, (0, 0, 255), (int((self.x + 0.5) * size),
                                         int((self.y + 0.5) * size)), round(self.genes["sens"] * size), 1)
        # pg.draw.line(sc, (255, 0, 0), ((self.x + 0.5) * size, (self.y + 0.5) * size),
        #              ((self.target[0] + 0.5) * size, (self.target[1] + 0.5) * size))
        # sc.blit(font(self.ate), ((self.x + 0.5) * size, (self.y + 0.5) * size))

    def move(self):
        if min(self.x, N - 1 - self.x, self.y, N - 1 - self.y) < self.cur_energy and self.ate < self.need_eat:
            if not self.found or (self.dx == 0 and self.dy == 0):
                self.sens()
                self.cur_energy -= self.genes["sens"]
        else:  # move_out
            if 0 != self.x != N - 1 != self.y != 0:
                X = 0 if self.x < N - 1 - self.x else N - 1
                Y = 0 if self.y < N - 1 - self.y else N - 1
                self.target = (X, self.y) if abs(N//2 - self.x) > abs(N//2 - self.y) else (self.x, Y)
        self.dx = sign(self.target[0] - self.x); self.dy = sign(self.target[1] - self.y)
        self.x, self.y = self.x + self.dx, self.y + self.dy
        self.cur_energy -= abs(self.dx) + abs(self.dy)

    def reply(self, a):
        genes = self.genes.copy()
        if randint(0, 100) < self.chances["sens"]:
            genes["sens"] += 0.1 if randint(0, 1) else -0.1
            genes["sens"] = round(genes["sens"], 2)
        a.append(Dude(genes))

    def sens(self):
        if self.target == (self.x, self.y):
            self.target = (randint(1, N - 2), randint(1, N - 2))
        rad = 2 * N
        self.found = False
        for x in range(-mt.ceil(self.genes["sens"]), mt.ceil(self.genes["sens"]) + 1):
            for y in range(-mt.ceil(self.genes["sens"]), mt.ceil(self.genes["sens"]) + 1):
                if (self.x + x, self.y + y) in food and rad > mt.hypot(x, y) <= self.genes["sens"] + 0.5:
                    self.target = (self.x + x, self.y + y)
                    rad = mt.hypot(x, y)
                    self.found = True

def sort(A):
    if len(A) < 2:
        return
    L, R = A[:len(A) // 2], A[len(A) // 2:]
    sort(L)
    sort(R)
    i = m = k = 0
    while m < len(L) and k < len(R):
        if L[m][0] < R[k][0] or (L[m][0] == R[k][0] and L[m][1] <= R[k][1]):
            A[i] = L[m]
            m += 1
        else:
            A[i] = R[k]
            k += 1
        i += 1
    A[i:] = L[m:] + R[k:]

def startDay(n, dudes):
    for dude in dudes:
        dude.cur_energy = dude.Energy
        dude.ate = 0
    for i in range(n):
        food[i] = (randint(1, N - 2), randint(1, N - 2))
    sort(food)
    if len(population) == 0:
        plt.plot(np.linspace(1, (len(averageSens) + 1) / 4, len(averageSens)), averageSens, 'go')
        plt.show()
        pg.quit()
    else:
        newDay = round(sum([i.genes["sens"] for i in population]) / len(population), 3)
    amount.append(len(population))
    averageSens.append(newDay)
    showState(population)

def runDay(dudes):
    done = True
    for dude in dudes:
        dude.move()
        if (dude.x, dude.y) in food:
            food[food.index((dude.x, dude.y))] = (-100, -100)
            if dude.ate < dude.need_eat:
                dude.ate += 1
                dude.found = False
        if not (dude.x in (0, N - 1) or dude.y in (0, N - 1)):
            done = False
    showState(dudes)
    # pg.time.Clock().tick(30)
    return done

def endDay(dudes):
    for dude in dudes.copy():
        if dude.ate == 0:
            dudes.remove(dude)
        elif dude.ate == dude.need_eat:
            dude.reply(dudes)

def draw(a, dudes):
    for line in a:
        for sector in line:
            sector.draw()
    for f in food:
        pg.draw.circle(sc, (50, 50, 255), (int((f[0] + 0.5) * size), int((f[1] + 0.5) * size)), size // 4)
    for dude in dudes:
        dude.draw()

class Sector:
    def __init__(self, x, y, colors):
        self.sc = sc
        self.x = x
        self.y = y
        self.color = colors[randint(0, len(colors) - 1)]

    def draw(self):
        pg.draw.rect(sc, self.color, (self.x * size, self.y * size, size, size))

def showState(dudes):
    pg.draw.rect(sc, black, (N * size, 0, showPlace, N * size))
    s = sum([dude.genes["sens"] for dude in dudes])
    if len(dudes):
        sc.blit(font(round(s/len(dudes), 3)), (N * size + 15, 15))
    sc.blit(font(f"food count: {foodN}"), (N * size + 125, 15))
    sc.blit(font(f"dudes count: {len(dudes)}"), (N * size + 125, 45))
    sc.blit(font(f"days: {len(amount)}"), (N * size + 125, 75))
    graphic([dude.genes["sens"] for dude in dudes])

N = 150
size = 6
showPlace = 600

scs = N * size  # screen size
sc = pg.display.set_mode((scs+showPlace, scs))
pg.display.set_caption("simulacrum")

area = [[Sector(x, y, green) for x in range(N)] for y in range(N)]

foodN = 40
food = [(0, 0)] * foodN

FPS = 1
leftFrame = FPS

persons = 3
population = [Dude() for i in range(persons)]

amount = []
averageSens = []

startDay(foodN, population)
draw(area, population)

ShowMod = True
pause = True
doneDay = False
worked = True
while worked:
    if not pause and not doneDay:
        leftFrame -= 1
        doneDay = runDay(population)
        if leftFrame <= 0:
            if ShowMod:
                draw(area, population)
            leftFrame = FPS
    if doneDay:
        endDay(population)
        # if len(averageSens) > 1:
        #     if abs(averageSens[-2] - 2 * averageSens[-1] + newDay) < 0.1:
        #         print(f'среднее убывание ({averageSens[-2]}; {averageSens[-1]}; {newDay})')
        #         averageSens[-1] = newDay
        #     elif abs(averageSens[-1] - newDay) < 0.1:
        #         print(f'среднее знаение ({averageSens[-1]}; {newDay})')
        #         averageSens[-1] = round((newDay + averageSens[-1]) / 2, 4)
        #     else:
        #         averageSens.append(newDay)
        # else:
        startDay(foodN, population)
        doneDay = False
    for e in pg.event.get():
        if e.type == pg.QUIT:
            worked = False
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_SPACE:
                pause = not pause
            if e.key == pg.K_LALT:
                ShowMod = not ShowMod
            if e.key == pg.K_TAB:
                population = [Dude() for i in range(persons)]
            if e.key == pg.K_DOWN:
                foodN -= 1
            if e.key == pg.K_UP:
                foodN += 1
            if e.key == pg.K_RETURN:
                # plt.plot(np.linspace(1, (len(amount) + 1) / 4, len(amount)), amount, 'bo')
                # plt.plot(np.linspace(1, (len(amount) + 1), len(amount)), mid_value(amount, generates, len(amount)))
                plt.plot(np.linspace(1, (len(averageSens) + 1) / 4, len(averageSens)), averageSens, 'go')
                plt.show()
    pg.display.update()
pg.quit()
