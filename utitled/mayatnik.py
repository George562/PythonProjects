import pygame as pg  # графическая библиотека
import math
pg.init()
white = (255, 255, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)
green = (0, 255, 0)


def font(text):  # это текст возвращает
    return pg.font.SysFont('verdana', 18).render(str(text), True, white)


class Cube:  # объект
    def __init__(self, win, hor, mass=None, gamma=None):
        self.win = win
        self.pos0 = [550, 300 if hor else 350]  # начальная позиция
        self.pos = [550., 300. if hor else 350.]  # позиция
        self.mass = mass or 1  # масса
        self.v = [0., 0.]  # скорость
        self.a = [0., 0.]  # ускорение
        self.gamma = gamma or 1  # сопротивление среды

    def draw(self):  # рисует квадрат
        pg.draw.rect(self.win, green, (self.pos[0]-15, self.pos[1]-15, 30, 30))


class Scale:  # ползунок меняешь, меняется значение переменной
    def __init__(self, win, x, y, pos, start, stop, step, name):
        self.name = font(name)
        self.w = 230
        self.h = 30
        self.x = x
        self.y = y
        self.scalar = (self.x+int((self.w-10)*(pos-start)/(stop-start))+5, self.y+self.h//2)
        self.number = pos
        self.start = start
        self.stop = stop
        self.step = step
        self.name_x = self.x-self.name.get_width()-5
        self.name_y = self.y

    def draw(self):
        self.win.blit(self.name, [self.name_x, self.name_y])
        self.win.blit(font(self.number), [self.x+self.w+5, self.name_y])
        pg.draw.rect(self.win, yellow, (self.x, self.y, self.w+5, self.h+5))
        pg.draw.line(self.win, white, (self.x+5, self.y+self.h/2),
                                      (self.x+self.w-5, self.y+self.h/2), 4)
        pg.draw.circle(self.win, red, self.scalar, 10)

    def update(self, x, y):
        if self.x <= x <= self.x+self.w and self.y <= y <= self.y+self.h:
            self.scalar = (x, self.y+self.h//2)
            self.number = (x-self.x)/self.w*(self.stop-self.start)+self.start
            self.number = round(self.number-self.number % self.step, 2)
        return self.number


def prugina(win, obj, k):  # эта функция считает
    x, y = pg.mouse.get_pos()
    if horizont:  # в горизонтальном положении без g
        pg.draw.rect(win, white, (5, 270, 25, 60))  # основание пружины
        pg.draw.line(win, white, (550, 0), (550, 950))  # центр равновесия
        if pg.mouse.get_pressed()[0] and not (x >= scale_x-25 and y >= scale_y-25):
            obj.pos[0] = x
            obj.a[0] = 0
            obj.v[0] = 0
        else:
            obj.a[0] = -(obj.gamma*obj.v[0]/5+k*(obj.pos[0]-obj.pos0[0])/500)/obj.mass
            obj.v[0] += obj.a[0]
            obj.pos[0] += obj.v[0]
        for i in range(31):
            pg.draw.circle(win, white, (30+int(i*(obj.pos[0]-30)/30), 300+int(60*math.sin(i*math.pi/6))), 6)
    else:  # в вертикальном положении с g
        pg.draw.rect(win, white, (520, 5, 60, 25))  # основание пружины
        pg.draw.line(win, (255, 0, 255), (0, 350), (1300, 350))  # центр равновесия без g
        pg.draw.line(win, white, (0, 350+(g*obj.mass/k)*500), (1300, 350+(g*obj.mass/k)*500))  # центр равновесия с g
        if pg.mouse.get_pressed()[0] and not (x >= scale_x-25 and y >= scale_y-25):  # перемещаем квадрат
            obj.pos[1] = y
            obj.a[1] = 0
            obj.v[1] = 0
        else:
            obj.a[1] = -(obj.gamma*obj.v[1]/5+k*(obj.pos[1]-obj.pos0[1])/500)/obj.mass+g
            obj.v[1] += obj.a[1]
            obj.pos[1] += obj.v[1]
        for i in range(25):
            pg.draw.circle(win, white, (550+int(60*math.sin(i*math.pi/6)), 30+int(i*(obj.pos[1]-30)/24)), 6)


screen = pg.display.set_mode((1350, 950))  # рабочая область (ширина, высота)
pg.display.set_caption('маятник')  # название приложения
horizont = True  # горизонтально ли расположен маятник
g = 9.81  # ускорение свободного падения
k = 100  # упругость пружины

cube = Cube(screen, horizont)
clock = pg.time.Clock()

# шкалы
scale_x = 1050
scale_y = 600
scale_of_mass = Scale(screen, scale_x, scale_y, cube.mass, 1, 70, 1, 'mass')
scale_of_gamma = Scale(screen, scale_x, scale_y+40, cube.gamma, 0, 5.6, 0.1, 'gamma')
scale_of_g = Scale(screen, scale_x, scale_y+80, g, 0, 14, 0.01, 'g')
scale_of_k = Scale(screen, scale_x, scale_y+120, k, 1, 1400, 5, 'k')

done = False
while not done:
    screen.fill((0, 0, 0))  # закрашиваем черным экран
    cube.draw()
    prugina(screen, cube, k)
    if pg.mouse.get_pressed()[0]:
        cube.mass = scale_of_mass.update(*pg.mouse.get_pos())
        cube.gamma = scale_of_gamma.update(*pg.mouse.get_pos())
        k = scale_of_k.update(*pg.mouse.get_pos())
        if not horizont:  # если вертикальная пружина можно менять g
            g = scale_of_g.update(*pg.mouse.get_pos())
    scale_of_mass.draw()
    scale_of_gamma.draw()
    scale_of_k.draw()
    if not horizont:  # и рисовать ползунок
        scale_of_g.draw()
    for event in pg.event.get():  # обрабатываем события
        if event.type == pg.QUIT:  # если нажат крест, закрываем приложение
            done = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_TAB:  # если нажат TAB меняем положение пружины
                horizont = not horizont
                cube = Cube(screen, horizont, cube.mass, cube.gamma)
            elif event.key == pg.K_SPACE:  # выставить значения по дефолту
                cube = Cube(screen, horizont)
                g = 9.81
                k = 100
                scale_of_mass = Scale(screen, scale_x, scale_y, cube.mass, 1, 70, 1, 'mass')
                scale_of_gamma = Scale(screen, scale_x, scale_y + 40, cube.gamma, 0, 5.6, 0.1, 'gamma')
                scale_of_g = Scale(screen, scale_x, scale_y + 80, g, 0, 14, 0.01, 'g')
                scale_of_k = Scale(screen, scale_x, scale_y + 120, k, 1, 1400, 5, 'k')
    pg.display.flip()  # обновляем экран
    clock.tick(90)  # скорость обновления экрана
