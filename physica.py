try:
    import pygame as pg
except ModuleNotFoundError:
    import os
    os.system('pip install pygame')
    import pygame as pg
import math as m

pg.init()

black  = (  0,   0,   0)
blue   = (  0,   0, 255)
green  = (  0, 255,   0)
red    = (255,   0,   0)
purple = (255,   0, 255)
yellow = (255, 255,   0)
white  = (255, 255, 255)

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


def physic():
    global simulate
    obj.ax = - E*obj.q/obj.mass if obj.x > L + start[0] else 0
    obj.vx += obj.ax * DT
    obj.x += obj.vx * DT
    obj.ay = gravity
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

v = 1
angle = 45
start = (50, 600)
obj = Obj(*start)
obj.q = 1
obj.mass = 1
L = 100
zoom = 1
DT = 2 * 10e-3
workplace = [(50, 600), (50, 50), (850, 50), (850, 600)]

# sliders
vSlider = Slider(sc, 80, 50, 620, 1, 'v')
angleSlider = Slider(sc, 40, 220, 620, 45, 'angle')
lSlider = Slider(sc, 80, 310, 620, 100, 'L')
ESlider = Slider(sc, 80, 430, 620, 100, 'E')

simulate = False
done = False
while not done:
    sc.fill(black)
    if simulate:
        physic()
    pg.draw.circle(sc, white, (round(obj.x), round(obj.y)), 10)
    pg.draw.polygon(sc, white, workplace, 1)
    pg.draw.line(sc, yellow, (L, 50), (L, 600))

    vSlider.update(*pg.mouse.get_pos())
    angleSlider.update(*pg.mouse.get_pos())
    lSlider.update(*pg.mouse.get_pos())
    ESlider.update(*pg.mouse.get_pos())

    vSlider.draw()
    ESlider.draw()
    angleSlider.draw()
    lSlider.draw()

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
            if event.key == pg.K_SPACE:
                if (obj.x, obj.y) != start:
                    obj.x, obj.y = start
                    print(1)
                else:
                    simulate = not simulate
                    obj.vx = m.cos(m.radians(angle)) * v
                    obj.vy = - m.sin(m.radians(angle)) * v
    pg.display.update()

pg.quit()
