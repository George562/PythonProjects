import pygame as pg
from random import randint
from time import time

class Figure:
    def __init__(self, space, figs):
        self.space = space
        self.figs = figs
        self.fig = figs[randint(0, len(figs)-1)]
        self.fig = figs[1]
        self.arr = []
        for i in range(len(self.fig)):
            for j in range(self.fig[i]):
                self.space[i][4+j] = 1
                self.arr.append([i, 4+j])
        self.time = time()
        self.iter = 0

    def rotate(self):
        if self.fig != [4]:
            if self.fig == [3, 1]:
                new_arr = [i for i in self.arr]
                if self.iter == 0:
                    new_arr[1] = new_arr[1][0]+(1 if self.iter < 1 else -1), new_arr[1][1]+(1 if 0 < self.iter < 2 else -1)
                    new_arr[2] = new_arr[2][0]+(2 if self.iter < 1 else -2), new_arr[2][1]+(2 if 0 < self.iter < 2 else -2)
                    new_arr[3] = new_arr[3][0]+(1 if 0 < self.iter < 2 else -1), new_arr[3][1]+(1 if self.iter < 1 else -1)
                for i in new_arr:
                    if i in self.space and i not in self.arr:
                        break
                else:
                    for i in self.arr:
                        self.space[i[0]][i[1]] = 0
                    self.arr = [i for i in new_arr]
                    for i in self.arr:
                        self.space[i[0]][i[1]] = 1
        self.iter = self.iter % 4

    def move(self, to=''):
        if time()-self.time > 1:
            self.time = time()
            for i in self.arr:
                if i[0]+1 == top or (self.space[i[0]+1][i[1]] and [i[0]+1, i[1]] not in self.arr):
                    self.__init__(self.space, self.figs)
                    pg.time.delay(100000)
                    break
            else:
                for i in range(len(self.arr)-1, -1, -1):
                    y, x = self.arr[i]
                    self.space[y][x] = 0
                    self.space[y+1][x] = 1
                    self.arr[i][0] += 1
        if to == 'r':
            for i in self.arr:
                if i[1]+1 == top or (self.space[i[0]][i[1]+1] and [i[0], i[1]+1] not in self.arr):
                    break
            else:
                for i in range(len(self.arr)-1, -1, -1):
                    y, x = self.arr[i]
                    self.space[y][x] = 0
                    self.space[y][x+1] = 1
                    self.arr[i][1] += 1
        elif to == 'l':
            for i in self.arr:
                if i[1] == 0 or (self.space[i[0]][i[1]-1] and [i[0], i[1]-1] not in self.arr):
                    break
            else:
                for i in range(len(self.arr)):
                    y, x = self.arr[i]
                    self.space[y][x] = 0
                    self.space[y][x-1] = 1
                    self.arr[i][1] -= 1
        if to == 'd':
            for i in self.arr:
                if i[1]+1 == top or (self.space[i[0]][i[1]+1] and [i[0], i[1]+1] not in self.arr):
                    break
            else:
                for i in range(len(self.arr)-1, -1, -1):
                    y, x = self.arr[i]
                    self.space[y][x] = 0
                    self.space[y][x+1] = 1
                    self.arr[i][1] += 1

size = 16*4
top = 10
scw = sch = size*top
gmap = [[0]*top for _ in range(top)]
figures = [
    [4],
    [3, 1],
    [1, 1, 2],
    [2, 2],
    [1, 2, 1]
]
colors = [[55+i*20]*3 for i in range(top)]
sc = pg.display.set_mode((scw, sch))
fig = Figure(gmap, figures)
clock = pg.time.Clock()
done = False
while not done:
    sc.fill((0, 0, 0))
    fig.move()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_d or event.key == pg.K_RIGHT:
                fig.move('r')
            if event.key == pg.K_a or event.key == pg.K_LEFT:
                fig.move('l')
            if event.key == pg.K_SPACE:
                fig.rotate()
    for line in range(top):
        for cell in range(top):
            if gmap[line][cell] == 1:
                pg.draw.rect(sc, colors[line], (cell*size+1, line*size+1, size-2, size-2))
    pg.display.flip()
    clock.tick(60)
