import pygame as pg

pg.init()

white  = (200, 200, 200)
red    = (255,   0,   0)
lwhite = (255, 255, 255)
lred   = (255, 100, 100)
gray   = (100, 100, 100)
bred   = (150,   0,   0)


def draw(pos, fill=True):
    x, y = pos[0] * size, pos[1] * size
    pg.draw.rect(sc, red if fill else white, (x, y, size, size))
    pg.draw.rect(sc, lred if fill else lwhite, (x, y, size, 2))
    pg.draw.polygon(sc, bred if fill else gray, ((x, y), (x, y + size), (x + 1, y + size), (x + 2, y + 2)))


class Dude:
    N = 0
    wasN = 0
    alive = False

    def __init__(self, x, y):
        self.x = x
        self.y = y
        draw((x, y), self.alive)

    def born(self):
        if not self.alive:
            draw((self.x, self.y))
        self.alive = True

    def kill(self):
        if self.alive:
            draw((self.x, self.y), False)
        self.alive = False


def play(a, n):
    update(a, n)
    for y in range(n):
        for x in range(n):
            if a[y][x].N == 3:
                a[y][x].born()
            elif a[y][x].N != 2:
                a[y][x].kill()


def find(a, d, n):
    for dy, dx in (0, 1), (1, -1), (1, 0), (1, 1):
        if a[(d.y + dy) % n][(d.x + dx) % n].alive:
            d.wasN += 1
        if d.alive:
            a[(d.y + dy) % n][(d.x + dx) % n].wasN += 1


def update(a, n):
    for y in range(1, n):
        for x in range(1, n):
            find(a, a[y][x], n)
            a[y][x].N = a[y][x].wasN
            a[y][x].wasN = 0
    for x in range(n):
        a[0][x].N = a[0][x].wasN
        a[0][x].wasN = 0
    for y in range(1, n):
        a[y][0].N = a[y][0].wasN
        a[y][0].wasN = 0


n = 16
size = 27
scs = n * size
sc = pg.display.set_mode((scs, scs))
pg.display.set_caption('игра в жизнь, но лучше')

area = [[Dude(x, y) for x in range(n)] for y in range(n)]

clock = pg.time.Clock()
pause = True
done = False
while not done:
    if not pause:
        play(area, n)

    mpos = pg.mouse.get_pos()
    mx, my = mpos[0] // size, mpos[1] // size
    if mx < n and my < n:
        if pg.mouse.get_pressed()[0]:
            area[my][mx].born()
        elif pg.mouse.get_pressed()[2]:
            area[my][mx].kill()

    for e in pg.event.get():
        if e.type == pg.QUIT:
            done = True
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_SPACE:
                pause = not pause
            if e.key == pg.K_TAB:
                area = [[Dude(x, y) for x in range(n)] for y in range(n)]
    pg.display.update()
pg.quit()
