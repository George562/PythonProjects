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


def graphic(a):
    pg.draw.line(sc, white, (N * size + 15, N * size - 115), (N * size + 15, N * size - 15))
    data = {i: a.count(i) for i in set(a)}
    for j, i in enumerate(sorted(data.keys())):
        pg.draw.rect(sc, white, (N * size + 15 + 30 * j + 5, N * size - 20, 8, -data[i] * 5))
        sc.blit(font(i, 20),    [N * size + 15 + 30 * j + 5, N * size - 15])


class Dude:
    angle = (0, 0)
    Energy = 100
    energy = Energy
    geneSpeed = 1
    genes = {
        "sensitivity": 2.5
    }
    chances = {
        "sensitivity": 25
    }

    found = False

    ate = 0
    need_to_eat = 2

    def __init__(self, genes=None):
        self.genes = genes or self.genes
        if randint(0, 1) == 1:
            self.x = (N - 1) * randint(0, 1)
            self.y = randint(1, N - 2)
        else:
            self.x = randint(1, N - 2)
            self.y = (N - 1) * randint(0, 1)
        self.target = (randint(1, N - 2), randint(1, N - 2))

    def draw(self):
        pg.draw.polygon(sc, (255, 50, 50), (
            ((self.x + 0.25) * size, (self.y + 0.75) * size),
            ((self.x + 0.5) * size, (self.y + 0.25) * size),
            ((self.x + 0.75) * size, (self.y + 0.75) * size)
        ))
        pg.draw.circle(sc, (0, 0, 255), (int((self.x + 0.5) * size),
                                         int((self.y + 0.5) * size)), round(self.genes["sensitivity"] * size), 1)
        pg.draw.line(sc, (255, 0, 0), ((self.x + 0.5) * size, (self.y + 0.5) * size),
                     ((self.target[0] + 0.5) * size, (self.target[1] + 0.5) * size))
        sc.blit(font(self.ate), ((self.x + 0.5) * size, (self.y + 0.5) * size))

    def move(self):
        if min(self.x, N - 1 - self.x, self.y, N - 1 - self.y) < self.energy and self.ate < self.need_to_eat:
            if not self.found or self.angle == (0, 0):
                self.sensitivity()
                self.energy -= self.genes["sensitivity"]
        else:
            self.move_out()
        self.setAngle()

        x, y = self.x + self.angle[0], self.y + self.angle[1]

        self.energy -= abs(self.angle[0])
        self.energy -= abs(self.angle[1])

        self.x = x
        self.y = y

    def move_out(self):
        if 0 != self.x != N - 1 != self.y != 0:

            X = 0 if self.x < N - 1 - self.x else N - 1
            Y = 0 if self.y < N - 1 - self.y else N - 1

            self.target = (X, self.y) if abs(N//2 - self.x) > abs(N//2 - self.y) else (self.x, Y)

    def setAngle(self):
        dx = self.target[0] - self.x
        dy = self.target[1] - self.y
        self.angle = (abs(dx) // dx if dx != 0 else 0, abs(dy) // dy if dy != 0 else 0)

    def reply(self, a):
        genes = self.genes.copy()

        genes["sensitivity"] += (0.05, -0.05)[randint(0, 1)] if randint(0, 100) < self.chances["sensitivity"] else 0
        genes["sensitivity"] = round(genes["sensitivity"], 2)

        a.append(Dude(genes))

    def sensitivity(self):
        if self.target == (self.x, self.y):
            self.target = (randint(1, N - 2), randint(1, N - 2))
        rad = 2 * N
        self.found = False
        for x in range(-mt.ceil(self.genes["sensitivity"]), mt.ceil(self.genes["sensitivity"]) + 1):
            for y in range(-mt.ceil(self.genes["sensitivity"]), mt.ceil(self.genes["sensitivity"]) + 1):
                if (self.x + x, self.y + y) in food and rad > mt.hypot(x, y) <= self.genes["sensitivity"] + 0.5:
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
        elif L[m][0] > R[k][0] or (L[m][0] == R[k][0] and L[m][1] > R[k][1]):
            A[i] = R[k]
            k += 1
        i += 1
    A[i:] = L[m:] + R[k:]


def startDay(n, dudes):
    for dude in dudes:
        dude.energy = dude.Energy
        dude.ate = 0
    for i in range(n):
        food[i] = (randint(1, N - 2), randint(1, N - 2))
    sort(food)
    newDay = round(sum([i.genes["sensitivity"] for i in population]) / len(population), 3)
    amount.append(len(population))
    averageSensitivity.append(newDay)
    showState(population)


def runDay(dudes):
    done = True
    for dude in dudes:
        dude.move()
        if (dude.x, dude.y) in food:
            food[food.index((dude.x, dude.y))] = (-100, -100)
            if dude.ate < dude.need_to_eat:
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
        elif dude.ate == dude.need_to_eat:
            dude.reply(dudes)


def draw(a, dudes):
    for line in a:
        for sector in line:
            sector.draw()
    for f in food:
        pg.draw.circle(sc, (50, 50, 255), (int((f[0] + 0.5) * size),
                                           int((f[1] + 0.5) * size)), size // 4)
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
    s = sum([dude.genes["sensitivity"] for dude in dudes])
    if len(dudes):
        sc.blit(font(round(s/len(dudes), 4)), (N * size + 15, 15))
    sc.blit(font(f"food count: {len(food)}"), (N * size + 125, 15))
    sc.blit(font(f"dudes count: {len(dudes)}"), (N * size + 125, 45))
    sc.blit(font(f"days: {len(amount)}"), (N * size + 125, 75))
    graphic([dude.genes["sensitivity"] for dude in dudes])


N = 38
size = 18
showPlace = 600

scs = N * size  # screen size
sc = pg.display.set_mode((scs+showPlace, scs))
pg.display.set_caption("simulacrum")

area = [[Sector(x, y, green) for x in range(N)] for y in range(N)]

foodN = 50
food = [(0, 0)] * foodN

FPS = 1
leftFrame = FPS

persons = 3
population = [Dude() for i in range(persons)]

amount = []
averageSensitivity = []

startDay(foodN, population)

draw(area, population)


pause = True
doneDay = False
worked = True
while worked:
    if not pause and not doneDay:
        leftFrame -= 1
        doneDay = runDay(population)
        if leftFrame == 0:
            draw(area, population)
            leftFrame = FPS
    if doneDay:
        endDay(population)
        # if len(averageSensitivity) > 1:
        #     if abs(averageSensitivity[-2] - 2 * averageSensitivity[-1] + newDay) < 0.1:
        #         print(f'среднее убывание ({averageSensitivity[-2]}; {averageSensitivity[-1]}; {newDay})')
        #         averageSensitivity[-1] = newDay
        #     elif abs(averageSensitivity[-1] - newDay) < 0.1:
        #         print(f'среднее знаение ({averageSensitivity[-1]}; {newDay})')
        #         averageSensitivity[-1] = round((newDay + averageSensitivity[-1]) / 2, 4)
        #     else:
        #         averageSensitivity.append(newDay)
        # else:
        startDay(foodN, population)
        doneDay = False
    for e in pg.event.get():
        if e.type == pg.QUIT:
            worked = False
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_SPACE:
                pause = not pause
            if e.key == pg.K_TAB:
                population = [Dude() for i in range(persons)]
            if e.key == pg.K_RETURN:
                plt.plot(np.linspace(1, (len(amount) + 1) / 4, len(amount)), amount, 'bo')
                # plt.plot(np.linspace(1, (len(amount) + 1), len(amount)), mid_value(amount, generates, len(amount)))
                plt.plot(np.linspace(1, (len(averageSensitivity) + 1) / 4, len(averageSensitivity)), averageSensitivity, 'go')
                plt.show()
    pg.display.update()
pg.quit()
