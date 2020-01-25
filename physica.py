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

font = (lambda size, text: pg.font.SysFont('verdana', size).render(str(text), False, white))


class Obj:
    def __init__(self, x, y, vx=0, vy=0, ax=0, ay=0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay


class Slider:
    h = 30  # height

    def __init__(self, win, w, x, y, value, name=''):
        self.win = win  # place for draw
        self.name = font(18, name) if name != '' else None
        self.x = x  # x coordinate
        self.y = y  # y coordinate
        self.w = w  # width
        self.value = value  # present value
        self.name_x = self.x-self.name.get_width()-15 if name != '' else self.x
        self.default = (win, w, x, y, value, name)  # default parameters

    def draw(self):
        if self.name is not None:
            self.win.blit(self.name, [self.name_x, self.y])
        self.win.blit(font(18, self.value), [self.x+3, self.y])
        pg.draw.rect(self.win, white, (self.x, self.y, self.w, self.h), 2)  # bg

    def update(self, x, y):
        global actTyp, typing
        if self.x <= x <= self.x+self.w+1 and self.y <= y <= self.y+self.h:
            if pg.mouse.get_pressed()[0]:
                actTyp = self
                typing = True
                self.value = 0


def physic():
    global simulate
    obj.ax = obj.ay = 0
    ea = E*obj.q/obj.mass
    if obj.x > L + start[0]:
        obj.ax -= ea*m.cos(m.radians(-Eangle))
        obj.ay -= ea*m.sin(m.radians(-Eangle))
    obj.vx += obj.ax * DT
    obj.x += obj.vx * DT
    obj.ay += gravity
    obj.vy += obj.ay * DT
    obj.y += obj.vy * DT
    if obj.y > start[1]:
        simulate = False


scw, sch = 1000, 700
sc = pg.display.set_mode((scw, sch))

typing = False
actTyp = None

gravity = 9.81
E = 100
Eangle = 180

v = 100
angle = 45
start = (50, 600)
obj = Obj(*start)
obj.q = 1
obj.mass = 1
L = 500
Tstart, Tend = 0, 0
zoom = 1
DT = 2 * 10e-3
workplace = [(50, 600), (50, 50), (850, 50), (850, 600)]

# sliders
vSlider = Slider(sc, 80, 50, 620, 100, 'v')
angleSlider = Slider(sc, 40, 220, 620, 45, 'angle')
lSlider = Slider(sc, 80, 310, 620, 500, 'L')
ESlider = Slider(sc, 80, 430, 620, 100, 'E')
qSlider = Slider(sc, 80, 560, 620, 1, 'q')
EangleSlider = Slider(sc, 80, 740, 620, 180, 'E angle')

mapX, mapY = 0, 0

simulate = False
done = False
while not done:
    sc.fill(black)
    mPos = pg.mouse.get_pos()
    sc.blit(font(18, f'x = {round(obj.x-start[0], 5)}'), [860, 50])
    sc.blit(font(18, f'y = {round(start[1]-obj.y, 5)}'), [860, 75])
    sc.blit(font(18, f'vx = {round(obj.vx, 5)}'), [860, 100])
    sc.blit(font(18, f'vy = {round(-obj.vy, 5)}'), [860, 125])
    sc.blit(font(18, f'ax = {round(obj.ax, 5)}'), [860, 150])
    sc.blit(font(18, f'ay = {round(obj.ay, 5)}'), [860, 175])
    sc.blit(font(18, f'timer = {round(Tend-Tstart, 3)}'), [860, 200])
    if simulate:
        physic()
        Tend = time()
    pg.draw.circle(sc, white, (round(obj.x)+mapX, round(obj.y)+mapY), 10)
    pg.draw.polygon(sc, white, workplace, 1)
    pg.draw.line(sc, yellow, (L+start[0]+mapX, 50), (L+start[0]+mapX, 600))

    pg.draw.aaline(sc, yellow, (700, 300), (700-m.cos(m.radians(-Eangle+45))*20, 300-m.sin(m.radians(-Eangle+45))*20), 2)
    pg.draw.aaline(sc, yellow, (700, 300), (700-m.cos(m.radians(-Eangle))*50, 300-m.sin(m.radians(-Eangle))*50), 2)
    pg.draw.aaline(sc, yellow, (700, 300), (700-m.cos(m.radians(-Eangle-45))*20, 300-m.sin(m.radians(-Eangle-45))*20), 2)

    vSlider.update(*mPos)
    angleSlider.update(*mPos)
    lSlider.update(*mPos)
    ESlider.update(*mPos)
    qSlider.update(*mPos)
    EangleSlider.update(*mPos)

    vSlider.draw()
    ESlider.draw()
    angleSlider.draw()
    lSlider.draw()
    qSlider.draw()
    EangleSlider.draw()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        elif event.type == pg.KEYDOWN:
            if typing:
                if event.key in range(48, 58):
                    actTyp.value = int(f'{actTyp.value}{event.key - 48}')
                elif event.key == pg.K_BACKSPACE:
                    actTyp.value = int(str(actTyp.value)[:-1] or 0)
            if event.key == pg.K_RETURN:
                typing = False
                angle = angleSlider.value
                v = vSlider.value
                L = lSlider.value
                E = ESlider.value
                obj.q = qSlider.value
                Eangle = EangleSlider.value
            if event.key == pg.K_SPACE:
                if (obj.x, obj.y) != start:
                    obj.x, obj.y = start
                    obj.vx = obj.vy = obj.ax = obj.ay = 0
                    simulate = False
                    mapX = mapY = 0
                else:
                    simulate = True
                    Tstart = time()
                    obj.vx = m.cos(m.radians(angle)) * v
                    obj.vy = - m.sin(m.radians(angle)) * v
                    timer = time()
            if event.key in range(pg.K_UP, pg.K_LEFT+1):
                if event.key in (273, 274):  # 273 Up / 274 Down
                    mapY += 50 * (1 - 2 * (274 - event.key))
                if event.key in (275, 276):  # 275 RIGHT / 276 LEFT
                    mapX += 50 * (- 1 + 2 * (276 - event.key))
    pg.display.update()

pg.quit()
