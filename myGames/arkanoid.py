import pygame as pg
import random as rd
import os
from math import sin, cos, pi, hypot


class Ball:
    rad = 8
    vx = 1
    vy = -1

    def __init__(self, win, x, y, color, angle=45):
        self.win = win
        self.x = x
        self.y = y-2
        self.color = color
        self.angle = angle

    def draw(self):
        pg.draw.circle(self.win, self.color, (round(self.x), round(self.y)), self.rad)

    def update(self):
        self.x += self.vx*abs(cos(self.angle*pi/180))
        self.y += self.vy*sin(self.angle*pi/180)


class Block:
    w = 50
    h = 15

    def __init__(self, win, n, color, strength, y=0):
        self.win = win
        self.x = self.w*n
        self.y = y
        self.color = color
        self.strength = strength

    def update(self, obj):
        if self.y <= obj.y <= self.y+self.h:
            if round(obj.x)+obj.rad == self.x or round(obj.x)-obj.rad == self.x+self.w:
                obj.vx *= -1
                obj.x += obj.vx*cos(obj.angle*pi/180)
                self.strength -= 1
                return self.strength
        if self.x <= obj.x <= self.x+self.w:
            if round(obj.y)+obj.rad == self.y or round(obj.y)-obj.rad == self.y+self.h:
                obj.vy *= -1
                obj.y += obj.vy*sin(obj.angle*pi/180)
                self.strength -= 1
                return self.strength
        for x in self.x, self.x+self.w:
            for y in self.y, self.y+self.h:
                if hypot(x-obj.x, y-obj.y) < obj.rad:
                    obj.vx *= -1
                    obj.vy *= -1
                    obj.update()
                    self.strength -= 1
                    return self.strength

    def draw(self):
        pg.draw.rect(self.win, self.color, [self.x, self.y, self.w, self.h])


scW, scH = 500, 650
sc = pg.display.set_mode((scW, scH))
colors = ((0, 0, 255), (0, 255, 0), (0, 255, 255), (255, 0, 0), (255, 0, 255), (255, 255, 0))
strengths = (*[1]*10, *[2]*5, 3, 3, 4)
last_line = 8
blocks = []
for j in range(last_line):
    blocks.append([Block(sc, i, rd.choice(colors), rd.choice(strengths), j*Block.h) for i in range(10)])

plot_W, plot_H = 75, 15
plot_x, plot_y = (scW-plot_W)//2, scH-plot_H
plot_c = (100, 255, 100)

balls = [Ball(sc, plot_x+plot_W//2, plot_y-Ball.rad, (255, 255, 255))]

fps = 600
clock = pg.time.Clock()
time_line = 20*fps

pic = None
for file in os.listdir(os.getcwd()):
    if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg'):
        pic = pg.transform.scale(pg.image.load(file), (scW, scH))

done = False
while not done:
    k_press = pg.key.get_pressed()
    if pic is None:
        sc.fill((0, 0, 0))
    else:
        sc.blit(pic, (0, 0))

    if k_press[pg.K_a] and plot_x >= 0:
        plot_x -= 1
    elif k_press[pg.K_d] and plot_x+plot_W <= scW:
        plot_x += 1
    pg.draw.rect(sc, plot_c, (plot_x, plot_y, plot_W, plot_H))

    for line in blocks:
        for block in line:
            for ball in balls:
                if block.update(ball) == 0:
                    blocks[blocks.index(line)].pop(blocks[blocks.index(line)].index(block))
                    if block.color == (255, 0, 0) or block.color == (255, 0, 255):
                        balls.append(Ball(sc, ball.x, ball.y, (255, 255, 255), rd.choice([-45, -135])))
            block.draw()
        if len(line) == 0:
            blocks.pop(blocks.index(line))

    for ball in balls:
        if 0 >= ball.x-ball.rad:
            ball.vx = 1
        elif scW <= ball.x+ball.rad:
            ball.vx = -1
        if ball.y-ball.rad <= 0:
            ball.vy = 1

        if plot_x <= round(ball.x) <= plot_x+plot_W and round(ball.y)+ball.rad == plot_y:
            ball.vy = -1
            ball.angle = 155-round(130*(ball.x-plot_x)/plot_W)
        ball.update()
        ball.draw()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
    time_line -= 1
    if time_line == 0:
        time_line = 30*fps
        for line in blocks:
            for block in line:
                block.y += block.h
        blocks.append([Block(sc, i, rd.choice(colors), rd.choice(strengths)) for i in range(10)])
    pg.display.flip()
    clock.tick(fps)
