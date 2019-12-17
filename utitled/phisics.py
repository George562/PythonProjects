import pygame as pg
import math

G = 1.66 * 10e-11
Time = 0.1 ** 6

CO = 1
SGO = 2


class CircleObject:
    type = CO

    def __init__(self, space, mass, x, y, radius=8, vx=0, vy=0, ax=0, ay=0):
        self.space = space
        self.mass = mass
        self.radius = radius
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay
        self.line = []

    def move(self):
        all_ax = 0
        all_ay = 0
        for obj in self.space:
            if obj != self:
                dx, dy = obj.x - self.x, obj.y - self.y
                hyp = math.hypot(dx, dy)
                if hyp >= 8:
                    if dx != 0:
                        cos = dx/hyp
                        all_ax += cos * G * obj.mass / ((hyp * 10e-9) ** 2)
                    if dy != 0:
                        sin = dy/hyp
                        all_ay += sin * G * obj.mass / ((hyp * 10e-9) ** 2)

        self.ax = all_ax
        self.vx += self.ax * Time
        self.x += self.vx * Time

        self.ay = all_ay
        self.vy += self.ay * Time
        self.y += self.vy * Time
        self.line.append((self.x, self.y))
        if len(self.line) > 1500:
            self.line.pop(0)

    def show(self, win):
        for i in range(len(self.line)-1):
            pg.draw.line(win, (0, 255, 100), self.line[i], self.line[i+1])
        pg.draw.circle(win, (255, 255, 255), (round(self.x), round(self.y)), self.radius)


class StaticGravityObject:
    type = SGO

    def __init__(self, space, mass, x, y):
        self.space = space
        self.mass = mass
        self.x = x
        self.y = y

    def show(self, win):
        pg.draw.circle(win, (100, 100, 100), (self.x, self.y), 40, 4)
        pg.draw.circle(win, (100, 100, 100), (self.x, self.y), 5)


place = []
place.append(CircleObject(place, 10e5, 400, 300))
place.append(CircleObject(place, 10e5, 300, 400))
place.append(CircleObject(place, 10e5, 300, 500))
place.append(StaticGravityObject(place, 10e5, 400, 400))
scw, sch = 800, 800
sc = pg.display.set_mode((scw, sch))
done = False
while not done:
    sc.fill((0, 0, 0))
    m_pos = pg.mouse.get_pos()
    for subject in place:
        if subject.type == CO:
            subject.move()
        subject.show(sc)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
    pg.display.flip()
