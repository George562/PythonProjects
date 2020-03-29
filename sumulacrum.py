import pygame as pg
from random import randint
from time import time

pg.init()

white = (255, 255, 255)
black = (0, 0, 0)
green = (
    (215, 255, 179), (202, 255, 153),
    (189, 255, 128), (176, 255, 102), (163, 255, 77), (150, 255, 51),
    (136, 255, 26), (123, 255, 0), (111, 230, 0), (99, 204, 0),
    (86, 179, 0), (74, 153, 0), (62, 128, 0), (49, 102, 0),
    (37, 77, 0), (25, 51, 0)
)


font = (lambda text: pg.font.SysFont("Georgia", 20).render(str(text), True, white))


def moveIn(dude, was):
    pass


class Dude:
    angles = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
    angle = angles[randint(0, 7)]
    eat = False
    ready = False
    Energy = 10
    energy = 10
    geneSpeed = 1
    chances = {
        "speed": 25
    }
    size = 10
    speedtick = 3
    wasStep = []

    def __init__(self, n, m, genes=None):
        if genes:
            self.geneSpeed = genes["speed"]
            self.Energy = genes["energy"]
            self.energy = self.Energy
        if randint(0, 1):
            self.x = (n - 1) * randint(0, 1)
            self.y = randint(1, n - 2)
            self.angle = (-1, 0) if self.x else (1, 0)
        else:
            self.x = randint(1, n - 2)
            self.y = (n - 1) * randint(0, 1)
            self.angle = (0, -1) if self.y else (0, 1)
        self.map = m

    def draw(self):
        pg.draw.polygon(sc, (255, 50, 50), (
            ((self.x + 0.25) * size, (self.y + 0.75) * size),
            ((self.x + 0.5) * size, (self.y + 0.25) * size),
            ((self.x + 0.75) * size, (self.y + 0.75) * size)
        ))

    def move(self, a):
        if self.speedtick != 0:
            self.speedtick -= 1
        else:
            self.angle = self.angles[randint(0, 7)]
            self.speedtick = 3
        x, y = self.x + self.angle[0], self.y + self.angle[1]
        if (not self.eat or min(self.x, N - 1 - self.x, self.y, N - 1 - self.y) < self.energy) and not self.ready:
            k = randint(0, 1)
            if x <= 0:
                self.energy -= k
                self.x += k
            elif x >= N - 1:
                self.energy -= k
                self.x -= k
            else:
                self.energy -= abs(self.angle[0])
                self.x = x
            m = randint(0, 1) if k == 1 else 1
            if y <= 0:
                self.energy -= m
                self.y += m
            elif y >= N - 1:
                self.energy -= m
                self.y -= m
            else:
                self.energy -= abs(self.angle[1])
                self.y = y
            if not (0 < x < N - 1 and 0 < y < N - 1):
                self.angle = (k if x <= 0 else -k, m if y <= 0 else -m)
                self.speedtick = 3
        elif self.x != 0 and self.x != N - 1 and self.y != 0 and self.y != N - 1:
            self.energy -= 1
            if self.x - 1 < N - 2 - self.x:
                if self.y - 1 < N - 2 - self.y:
                    if self.y < self.x:
                        self.y -= 1
                    else:
                        self.x -= 1
                else:
                    if N - 2 - self.y < self.x - 1:
                        self.y += 1
                    else:
                        self.x -= 1
            else:
                if self.y - 1 < N - 2 - self.y:
                    if self.y - 1 < N - 2 - self.x:
                        self.y -= 1
                    else:
                        self.x += 1
                else:
                    if N - self.y < N - self.x:
                        self.y += 1
                    else:
                        self.x += 1

    def reply(self, n, a):
        if self.ready:
            k = randint(0, 100)
            m = randint(-10, 10) / 100 if k < self.chances["speed"] else 0
            genes = {
                "speed": self.geneSpeed + m,
                "energy": self.Energy + m * 100
            }
            a.append(Dude(n, self.map, genes))


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
        elif L[m][0] > R[k][0] or (L[m][0] == R[k][0] and R[k][1] <= L[m][1]):
            A[i] = R[k]
            k += 1
        i += 1
    A[i:] = L[m:] + R[k:]


def newDay(food, n, dudes):
    for dude in dudes:
        dude.energy = dude.Energy
        dude.ready = False
        dude.eat = False
    for i in range(n):
        food[i] = (randint(1, N - 2), randint(1, N - 2))


def runDay(a, dudes, food):  # ToDo
    done = True
    for dude in dudes:
        dude.move(a)
        if (dude.x, dude.y) in food:
            food[food.index((dude.x, dude.y))] = (-1, -1)
            if not dude.eat:
                dude.eat = True
            else:
                dude.ready = True
        if (dude.energy > 0 and not dude.ready) or (dude.ready and not (dude.x in (0, N - 1) or dude.y in (0, N - 1))):
            done = False
    return done


def endDay(dudes):  # ToDo
    for dude in dudes.copy():
        if not dude.eat:
            dudes.remove(dude)
        elif dude.ready:
            dude.reply(N, dudes)


def draw(a, dudes, food):
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


def showState(dudes, foods):
    pg.draw.rect(sc, black, (N * size, 0, showPlace, N * size))
    s = sum([dude.Energy for dude in dudes])
    if len(dudes):
        sc.blit(font(round(s/len(dudes), 4)), (N * size + 15, 15))
    sc.blit(font(f"dudes count: {len(dudes)}"), (N * size + 15, 45))
    sc.blit(font(f"food count: {len(foods)}"), (N * size + 125, 15))


N = 20
size = 30
showPlace = 350

scs = N * size
sc = pg.display.set_mode((scs+showPlace, scs))
pg.display.set_caption("simulacrum")

area = [[Sector(x, y, green) for x in range(N)] for y in range(N)]

foodN = 50
food = [0] * foodN

frameRate = 18

persons = 15
population = [Dude(N, area) for i in range(10)]
newDay(food, foodN, population)


draw(area, population, food)

pause = True
doneDay = False
done = False
while not done:
    if not pause and not doneDay:
        frameRate -= 1
        doneDay = runDay(area, population, food)
        showState(population, food)
        if frameRate == 0:
            draw(area, population, food)
            frameRate = 4
    if doneDay:
        endDay(population)
        newDay(food, foodN, population)
        doneDay = False
    for e in pg.event.get():
        if e.type == pg.QUIT:
            done = True
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_SPACE:
                pause = not pause
            if e.key == pg.K_TAB:
                population = [Dude(N, area)]
    pg.display.update()
pg.quit()
