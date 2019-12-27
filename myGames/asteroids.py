import pygame as pg
import math as m
from random import randint
from time import time
import sys


class Asteroid:
    def __init__(self, win, space):
        self.win = win
        self.space = space
        self.x = randint(0, scw)
        self.y = randint(0, sch)
        self.rad = randint(5, 25)
        self.color = (randint(150, 255), randint(150, 255), randint(150, 255))
        self.hp = self.rad // 5
        self.angle = m.radians(randint(0, 359))

    def draw(self):
        self.x += m.cos(self.angle)
        self.y += m.sin(self.angle)
        if self.x > scw:
            self.x = 0
        elif self.x < 0:
            self.x = scw
        if self.y > sch:
            self.y = 0
        elif self.y < 0:
            self.y = sch
        pg.draw.circle(self.win, self.color, (int(self.x), int(self.y)), self.rad)

    def update(self, arr):
        for bul in arr:
            if m.hypot(bul['x'] - self.x, bul['y'] - self.y) < self.rad:
                self.hp -= 1
                arr.pop(arr.index(bul))
                if self.hp == 0:
                    self.space.remove(self)


class Spaceship:
    angle = 0
    rad = 12
    rel = time()
    a = 0.05
    v = 0
    bulls = []

    def __init__(self, win, x, y):
        self.win = win
        self.x = x
        self.y = y

    def draw(self):
        pg.draw.polygon(self.win, (255, 255, 255), [
            [self.x + m.cos(self.angle + m.pi * 37 / 30) * self.rad,
             self.y + m.sin(self.angle + m.pi * 37 / 30) * self.rad],
            [self.x + m.cos(self.angle - m.pi * 37 / 30) * self.rad,
             self.y + m.sin(self.angle - m.pi * 37 / 30) * self.rad],
            [self.x + m.cos(self.angle) * self.rad, self.y + m.sin(self.angle) * self.rad]
        ])

    def move(self):
        k = pg.key.get_pressed()
        if k[pg.K_a] or k[pg.K_d]:
            self.angle += m.copysign(m.pi / 60, -1 if k[pg.K_a] else 1)
        if pg.mouse.get_pressed()[0] or pg.key.get_pressed()[pg.K_SPACE]:
            if time() - self.rel > 0.5:
                self.rel = time()
                self.bulls.append({'x': self.x, 'y': self.y, 'ang': self.angle})
            if self.v < 4:
                self.v += self.a
        elif self.v > 0:
            self.v -= self.a
        self.x += self.v * m.cos(self.angle)
        self.y += self.v * m.sin(self.angle)
        if self.x > scw:
            self.x = 0
        elif self.x < 0:
            self.x = scw
        if self.y > sch:
            self.y = 0
        elif self.y < 0:
            self.y = sch
        for bul in self.bulls:
            bul['x'] += m.cos(bul['ang']) * 5
            bul['y'] += m.sin(bul['ang']) * 5
            if bul['x'] > scw:
                bul['x'] = 0
            elif bul['x'] < 0:
                bul['x'] = scw
            if bul['y'] > sch:
                bul['y'] = 0
            elif bul['y'] < 0:
                bul['y'] = sch
            pg.draw.circle(self.win, (255, 255, 255), (int(bul['x']), int(bul['y'])), 4)


scw, sch = 800, 650
asteroids = []
t = time()
bg = pg.transform.scale(pg.image.load('background.jpeg'), (scw, sch))
sc = pg.display.set_mode((scw, sch))
pg.display.set_caption('asteroids')
spaceship = Spaceship(sc, scw // 2, sch // 2)
clock = pg.time.Clock()
done = False
while not done:
    if time() - t > 3:
        asteroids.append(Asteroid(sc, asteroids))
        t = time()
    sc.blit(bg, (0, 0))
    for ast in asteroids:
        ast.draw()
        ast.update(spaceship.bulls)
        if m.hypot(ast.x - spaceship.x, ast.y - spaceship.y) < ast.rad + spaceship.rad:
            sys.exit()
    spaceship.move()
    spaceship.draw()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
    pg.display.flip()
    clock.tick(60)
