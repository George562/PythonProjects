try:
    import pygame as pg
except ModuleNotFoundError:
    import os

    os.system('pip install pygame')
    import pygame as pg
import math as m
from time import time

pg.init()

black = (0, 0, 0)
yellow = (255, 255, 0)
white = (255, 255, 255)
green = (50, 255, 50)

temp = 80

font = (lambda size, text: pg.font.SysFont('verdana', size).render(str(text), False, white))
real = (lambda x: x * temp / mapDX)


def coordinates(dx):
    for i in range((workplace[3][0] - workplace[1][0]) // temp + 1):
        val = font(15, -int(mapX) + i * dx)
        sc.blit(val, (workplace[1][0] + i * temp - val.get_width() / 2, workplace[3][1]))
    for i in range((workplace[3][1] - workplace[1][1]) // temp + 1):
        val = font(15, int(mapY) + i * dx)
        sc.blit(val, (workplace[1][1], workplace[3][1] - i * temp - 15))


class Obj:
    def __init__(self, x=0, y=0, vx=0, vy=0, ax=0, ay=0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay


class Slider:
    actTyp = None
    h = 30  # height

    def __init__(self, win, w, x, y, value, name=''):
        self.win = win  # place for draw
        self.name = font(18, name) if name != '' else None
        self.x = x  # x coordinate
        self.y = y  # y coordinate
        self.w = w  # width
        self.value = value  # present value
        self.name_x = self.x - self.name.get_width() - 10 if name != '' else self.x
        self.default = (win, w, x, y, value, name)  # default parameters

    def draw(self):
        if self.name is not None:
            self.win.blit(self.name, [self.name_x, self.y])
        val = font(18, self.value)
        self.win.blit(val, [self.x + (self.w - val.get_width()) / 2, self.y + (self.h - val.get_height()) / 2])
        pg.draw.rect(self.win, white, (self.x, self.y, self.w, self.h), 2)  # bg

    def update(self, x, y):
        if 0 <= x - self.x <= self.w and 0 <= y - self.y <= self.h:
            if pg.mouse.get_pressed()[0]:
                Slider.actTyp = self
                self.value = 0


def physic():
    global simulate
    obj.ax = obj.ay = 0
    ea = E.value * q.value / obj.mass
    if obj.x > L.value:
        obj.ax -= ea * m.cos(m.radians(-Eangle.value))
        obj.ay -= ea * m.sin(m.radians(-Eangle.value))
    obj.vx += obj.ax * DT
    obj.x += obj.vx * DT
    obj.ay += gravity
    obj.vy += obj.ay * DT
    obj.y += obj.vy * DT
    if obj.y > 0:
        simulate = False


scw, sch = 1000, 700
sc = pg.display.set_mode((scw, sch))

gravity = 9.81

start = (50, 560)
obj = Obj()
obj.mass = 1
Tstart, Tend = 0, 0
zoom = 1
DT = 2 * 10e-3
workplace = [(50, 560), (50, 10), (850, 10), (850, 560)]
trajectory = []
lastAdd = 0

# sliders
V = Slider(sc, 80, 50, 620, 100, 'v')
angle = Slider(sc, 40, 220, 620, 45, 'angle')
L = Slider(sc, 80, 310, 620, 500, 'L')
E = Slider(sc, 80, 430, 620, 100, 'E')
q = Slider(sc, 80, 560, 620, 1, 'q')
Eangle = Slider(sc, 80, 740, 620, 180, 'E angle')

mapX, mapY = 0, 0
mapDX = 50
mapDT = Slider(sc, 60, 890, 620, 30, 'rate')

simulate = False
done = False
while not done:
    sc.fill(black)
    coordinates(mapDX)
    mPos = pg.mouse.get_pos()
    sc.blit(font(18, f'x = {round(obj.x, 4)}'), [860, 50])
    sc.blit(font(18, f'y = {round(-obj.y, 4)}'), [860, 75])
    sc.blit(font(18, f'vx = {round(obj.vx, 4)}'), [860, 100])
    sc.blit(font(18, f'vy = {round(-obj.vy, 4)}'), [860, 125])
    sc.blit(font(18, f'ax = {round(obj.ax, 4)}'), [860, 150])
    sc.blit(font(18, f'ay = {round(obj.ay, 4)}'), [860, 175])
    sc.blit(font(18, f'timer = {round(Tend - Tstart, 3)}'), [860, 200])
    if simulate:
        physic()
        if time() - lastAdd > 1 / (mapDT.value + 1):
            trajectory.append((obj.x, obj.y))
            lastAdd = time()
        Tend = time()
        if not - 3 < real(obj.x + mapX) < workplace[3][0] - start[0] + 3:
            mapX += -mapDX if workplace[3][0] - start[0] < real(obj.x + mapX) else mapDX
        if not workplace[1][1] - 3 < real(obj.y + mapY) + start[1] < workplace[3][1] + 3:
            mapY += -mapDX if workplace[3][1] + 3 < real(obj.y + mapY) + start[1] else mapDX
    pg.draw.circle(sc, white, (round(real(obj.x + mapX)) + start[0], round(real(obj.y + mapY)) + start[1]), 10)
    pg.draw.polygon(sc, white, workplace, 1)
    pg.draw.line(sc, yellow, (real(L.value + mapX) + start[0], 10), (real(L.value + mapX) + start[0], 560))

    pg.draw.aaline(sc, yellow, (700, 300),
                   (700 - m.cos(m.radians(-Eangle.value + 45)) * 20, 300 - m.sin(m.radians(-Eangle.value + 45)) * 20))
    pg.draw.aaline(sc, yellow, (700, 300),
                   (700 - m.cos(m.radians(-Eangle.value)) * 50, 300 - m.sin(m.radians(-Eangle.value)) * 50))
    pg.draw.aaline(sc, yellow, (700, 300),
                   (700 - m.cos(m.radians(-Eangle.value - 45)) * 20, 300 - m.sin(m.radians(-Eangle.value - 45)) * 20))

    for slider in V, E, angle, L, q, Eangle, mapDT:
        slider.update(*mPos)
        slider.draw()

    for point in range(len(trajectory) - 1):
        first = real(trajectory[point][0] + mapX) + start[0], real(trajectory[point][1] + mapY) + start[1]
        second = real(trajectory[point + 1][0] + mapX) + start[0], real(trajectory[point + 1][1] + mapY) + start[1]
        pg.draw.line(sc, green, first, second)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        elif event.type == pg.KEYDOWN:
            if Slider.actTyp:
                if event.key in range(48, 58):
                    Slider.actTyp.value = int(f'{Slider.actTyp.value}{event.key - 48}')
                elif event.key == pg.K_BACKSPACE:
                    Slider.actTyp.value = int(str(Slider.actTyp.value)[:-1] or 0)
            if event.key == pg.K_RETURN:
                Slider.actTyp = None
            if event.key == pg.K_TAB:
                mapX = mapY = 0
            if event.key == pg.K_p and obj.x != 0 and obj.y != 0:
                simulate = not simulate
            if event.key == pg.K_SPACE:
                if (obj.x, obj.y) != (0, 0):
                    obj.x = obj.y = obj.vx = obj.vy = obj.ax = obj.ay = mapX = mapY = 0
                    simulate = False
                    trajectory.clear()
                else:
                    simulate = True
                    Tstart = time()
                    obj.vx = m.cos(m.radians(angle.value)) * V.value
                    obj.vy = - m.sin(m.radians(angle.value)) * V.value
            if event.key in range(pg.K_UP, pg.K_LEFT + 1):
                if event.key in (273, 274):  # 273 Up / 274 Down
                    mapY -= mapDX * (1 - 2 * (274 - event.key))
                if event.key in (275, 276):  # 275 RIGHT / 276 LEFT
                    mapX -= mapDX * (- 1 + 2 * (276 - event.key))
            if event.key == pg.K_d or event.key == pg.K_u:
                mapX, mapY = mapX // mapDX, mapY // mapDX
                mapDX += 50 if event.key == pg.K_u else -50 if mapDX != 50 else 0
                mapX, mapY = mapX * mapDX, mapY * mapDX
    pg.display.update()
pg.quit()
