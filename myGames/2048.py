import pygame as pg
from random import randint
pg.init()
font = (lambda size, text: pg.font.SysFont('verdana', size).render(str(text), True, (50, 50, 250)))
def up(arr):
    for line in range(1, len(arr)):
        for num in range(len(arr[line])):
            if arr[line][num] != 0:
                for dl in range(line - 1, -1, -1):
                    if arr[dl][num] != 0:
                        if arr[dl][num] == arr[line][num]:
                            arr[dl][num] *= 2
                            arr[line][num] = 0
                        elif dl + 1 != line:
                            arr[dl + 1][num], arr[line][num] = arr[line][num], 0
                        break
                    if arr[dl][num] == 0 and dl == 0:
                        arr[dl][num], arr[line][num] = arr[line][num], 0
def left(arr):
    for line in range(len(arr)):
        for num in range(1, len(arr[line])):
            if arr[line][num] != 0:
                for dn in range(num - 1, -1, -1):
                    if arr[line][dn] != 0:
                        if arr[line][dn] == arr[line][num]:
                            arr[line][dn] *= 2
                            arr[line][num] = 0
                        elif dn + 1 != num:
                            arr[line][dn + 1], arr[line][num] = arr[line][num], 0
                        break
                    if arr[line][dn] == 0 and dn == 0:
                        arr[line][dn], arr[line][num] = arr[line][num], 0
def down(arr):
    for line in range(len(arr) - 2, -1, -1):
        for num in range(len(arr[line])):
            if arr[line][num] != 0:
                for dl in range(line + 1, len(arr)):
                    if arr[dl][num] != 0:
                        if arr[dl][num] == arr[line][num]:
                            arr[dl][num] *= 2
                            arr[line][num] = 0
                        elif dl - 1 != line:
                            arr[dl - 1][num], arr[line][num] = arr[line][num], 0
                        break
                    if arr[dl][num] == 0 and dl == len(arr) - 1:
                        arr[dl][num], arr[line][num] = arr[line][num], 0
def right(arr):
    for line in range(len(arr)):
        for num in range(len(arr) - 2, -1, -1):
            if arr[line][num] != 0:
                for dn in range(num + 1, len(arr)):
                    if arr[line][dn] != 0:
                        if arr[line][dn] == arr[line][num]:
                            arr[line][dn] *= 2
                            arr[line][num] = 0
                        elif dn - 1 != num:
                            arr[line][dn - 1], arr[line][num] = arr[line][num], 0
                        break
                    if arr[line][dn] == 0 and dn == len(arr) - 1:
                        arr[line][dn], arr[line][num] = arr[line][num], 0
s = 85  # size of cell
scw = sch = 5  # width and height
sc = pg.display.set_mode((scw * s, sch * s))  # game display
game_map = [[0] * sch for _ in range(scw)]
game_map[scw // 2][sch // 2] = 2
nums = {2 ** i: font(25, 2 ** i) for i in range(1, 21)}
nums[0] = font(25, 0)
for x in range(scw):
    for y in range(sch):
        pg.draw.rect(sc, (250, 250, 50), (x * s + x, y * s + y, s, s))
        n = nums[game_map[y][x]]
        sc.blit(n, [x * s + (s - n.get_width()) / 2 + x, y * s + (s - n.get_height()) / 2 + y])
do = [up, left, down, right]
it = {pg.K_w: 0, pg.K_a: 1, pg.K_s: 2, pg.K_d: 3}
done = False
while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        elif event.type == pg.KEYDOWN:
            if event.key in it:
                was = [[game_map[y][x] for x in range(scw)] for y in range(sch)]
                do[it[event.key]](game_map)
                if game_map != was:
                    a, b = randint(0, scw - 1), randint(0, sch - 1)
                    while game_map[a][b] != 0: a, b = randint(0, scw - 1), randint(0, sch - 1)
                    game_map[a][b] = 2
                    for x in range(scw):
                        for y in range(sch):
                            pg.draw.rect(sc, (250, 250, 50), (x * s + x, y * s + y, s, s))
                            n = nums[game_map[y][x]]
                            sc.blit(n, [x * s + (s - n.get_width()) / 2 + x, y * s + (s - n.get_height()) / 2 + y])
    pg.display.flip()
