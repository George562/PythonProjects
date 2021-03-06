import pygame as pg
import math as m

DT = 3 * 10e-4
K = 9 * 10e9
GAMMA = 1


def set_acceleration(el1, el2, k, dX, q):
    dx, dy = el1.x - el2.x, el1.y - el2.y
    h = m.hypot(dx, dy)
    if h != 0:
        a = k * (dX - h) + K * q / (h ** 2)
        el1.ax += a * dx / h
        el1.ay += a * dy / h


class Element:
    q = 10e-8
    block = False

    def __init__(self, x, y, vx=0, vy=0, ax=0, ay=0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay


class Thread:
    choice = None

    def __init__(self, x, y, num, k=200, dX=4):
        self.num = num
        self.k = k
        self.dX = dX
        r = num * self.dX / (m.pi * 2)
        self.els = []
        for i in range(num):
            self.els.append(Element(x + m.cos(i * 2 * m.pi / num) * r, y + m.sin(i * 2 * m.pi / num) * r))

    def update(self, x, y, q, r):
        for i in range(self.num):
            self.els[i].ax = - self.els[i].vx * GAMMA
            self.els[i].ay = - self.els[i].vy * GAMMA
            for j in mousePoints:
                dx, dy = j[0] - self.els[i].x, j[1] - self.els[i].y
                h = m.hypot(dx, dy)
                if h > r:
                    self.els[i].ax -= q * K / (h ** 2) * dx / h
                    self.els[i].ay -= q * K / (h ** 2) * dy / h
                pg.draw.circle(sc, (255, 255, 255), j, mouseR, 1)
            dx, dy = x - self.els[i].x, y - self.els[i].y
            h = m.hypot(dx, dy)
            if h > r:
                self.els[i].ax -= q * K / (h ** 2) * dx / h
                self.els[i].ay -= q * K / (h ** 2) * dy / h
            for j in range(self.num):
                if i != j:
                    set_acceleration(self.els[i], self.els[j], 0, 0, self.els[j].q)
            set_acceleration(self.els[i], self.els[(i + 1) % self.num], self.k, self.dX, 0)
            set_acceleration(self.els[i], self.els[i - 1], self.k, self.dX, 0)

            self.els[i].vx += self.els[i].ax * DT
            self.els[i].vy += self.els[i].ay * DT

            if not self.els[i].block:
                self.els[i].x += self.els[i].vx * DT
                self.els[i].y += self.els[i].vy * DT
            if pg.mouse.get_pressed()[0]:
                if h < self.dX + 3 and not self.choice:
                    self.choice = self.els[i]
                if self.choice:
                    self.choice.x, self.choice.y = x, y
            else:
                Thread.choice = None

            color = (255, 255, 0) if self.els[i].block else (255, 255, 255)
            pg.draw.circle(sc, color, (round(self.els[i].x), round(self.els[i].y)), 2)


scw, sch = 900, 700
sc = pg.display.set_mode((scw, sch))

thread = Thread(scw / 2, sch / 2, 50)
mouseQ = 10e-5
mouseR = 12
mousePoints = []

done = False
while not done:
    sc.fill((0, 0, 0))
    m_pos = pg.mouse.get_pos()
    thread.update(*m_pos, mouseQ, mouseR)
    pg.draw.circle(sc, (255, 255, 255), m_pos, mouseR, 1)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                Element.q = 0 if Element.q else 10e-8
            elif event.key == pg.K_e:
                mouseQ = 0 if mouseQ else 10e-7
            elif event.key == pg.K_f:
                for element in thread.els:
                    if m.hypot(element.x - m_pos[0], element.y - m_pos[1]) < thread.dX + 2:
                        element.block = not element.block
                        break
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 3:
                mousePoints.append(m_pos)
    pg.display.update()
