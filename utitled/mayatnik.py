import math
import pygame as pg
pg.init()

# colors
white = (255, 255, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)
green = (0, 255, 0)

my_fonts = {}  # used fonts


def font_return(size, text, font='verdana'):
    if font not in my_fonts.keys():  # if font not in list, add it
        my_fonts[font] = [pg.font.SysFont(font, i) for i in range(5, 46)]
    return my_fonts[font][size].render(str(text), True, white)


class Scale:
    w = 180  # width
    h = 20  # height

    def __init__(self, win, x, y, pos, start, stop, step, name=''):
        self.win = win  # place for draw
        self.name = font_return(18, name, 'verdana')  # self name
        self.x = x  # x coordinate
        self.y = y  # y coordinate
        self.scalar = self.x+int((self.w-10)*(pos-start)/(stop-start))+5  # pos of slider
        self.value = pos  # present value
        self.start = start  # minimum value
        self.stop = stop  # maximum value
        self.step = step  # value step
        self.name_x = self.x-self.name.get_width()-15
        self.name_y = self.y
        self.default = (win, x, y, pos, start, stop, step, name)  # default parameters

    def draw(self):
        self.win.blit(self.name, [self.name_x, self.name_y])
        self.win.blit(font_return(18, self.value, 'verdana'), [self.x + self.w + 15, self.name_y])
        pg.draw.rect(self.win, yellow, (self.x-10, self.y-3, self.w+20, self.h+9))  # back
        pg.draw.line(self.win, white, (self.x, self.y+self.h//2),
                     (self.x+self.w, self.y+self.h//2), 4)  # slider line
        pg.draw.circle(self.win, red, (self.scalar, self.y+self.h//2+1), 10)  # slider

    def update(self, x, y):  # update external value
        if self.x <= x <= self.x+self.w and self.y <= y <= self.y+self.h:
            self.value = (x-self.x)/self.w*(self.stop-self.start)+self.start
            self.value = round(self.value-self.value % self.step, 4)
            self.scalar = round(self.x+self.w*self.value/(self.stop-self.start))
        if not self.value % 1:
            self.value = int(self.value)
        return self.value


class Cube:  # объект
    def __init__(self, win, hor, mass=None, gamma=None):
        self.win = win
        self.pos0 = [550, 300 if hor else 350]  # начальное положение
        self.pos = [550., 300. if hor else 350.]  # положение
        self.mass = mass or 1  # масса
        self.v = [0., 0.]  # скорость
        self.a = [0., 0.]  # ускорение
        self.gamma = gamma or 1  # сопротивление среды


def prugina(win, obj, k, dT):  # функция считает
    x, y = pg.mouse.get_pos()
    if horizont:  # в горизонтальном положении без g
        pg.draw.rect(win, white, (5, 270, 25, 60))  # основание пружины
        pg.draw.line(win, white, (550, 0), (550, 650))  # положение равновесия
        for i in range(31):
            pg.draw.circle(win, white, (30+int(i*(obj.pos[0]-30)/30), 300+int(60*math.sin(i*math.pi/6))), 6)
        if pg.mouse.get_pressed()[0] and not (x >= scale_x-25 and y >= scale_y-25):  # менять положение
            obj.v[0] = pg.mouse.get_rel()[0]*100
            obj.a[0] = obj.v[0]
            obj.pos[0] = x
        else:
            obj.a[0] = -(obj.gamma*obj.v[0]+k*(obj.pos[0]-obj.pos0[0]))/obj.mass
            obj.v[0] += obj.a[0]*dT
            obj.pos[0] += obj.v[0]*dT
    else:  # в вертикальном положении с g
        pg.draw.rect(win, white, (520, 5, 60, 25))  # основание пружины
        pg.draw.line(win, (255, 0, 255), (0, 350), (1300, 350))  # положение равновесия без g
        pg.draw.line(win, white, (0, 350+(g*obj.mass/k)*500), (1300, 350+(g*obj.mass/k)*500))  # с g
        for i in range(25):
            pg.draw.circle(win, white, (550+int(60*math.sin(i*math.pi/6)), 30+int(i*(obj.pos[1]-30)/24)), 6)
        if pg.mouse.get_pressed()[0] and not (x >= scale_x-25 and y >= scale_y-25):  # менять положение
            obj.v[1] = pg.mouse.get_rel()[1]*100
            obj.a[1] = obj.v[0]
            obj.pos[1] = y
        else:
            obj.a[1] = -(obj.gamma*obj.v[1]+k*(obj.pos[1]-obj.pos0[1]))/obj.mass+g*500
            obj.v[1] += obj.a[1]*dT
            obj.pos[1] += obj.v[1]*dT


screen = pg.display.set_mode((1300, 650))  # рабочая область (ширина, высота)
pg.display.set_caption('Маятник')  # название приложения
horizont = True  # горизонтально расположенна пружина или нет
g = 9.81  # ускорение свободного падения
k = 100  # упругость пружины
dT = 0.005  # период измерений

cube = Cube(screen, horizont)  # наш объект
clock = pg.time.Clock()

# все шкалы
scale_x = 1050  # крайняя левая точка размещения шкал
scale_y = 400  # крайняя верхняя точка размещения шкал
scale_of_small_mass = Scale(screen, scale_x, scale_y+160, cube.mass, 0.01, 1, 0.01, 'mass')
scale_of_mass = Scale(screen, scale_x, scale_y, cube.mass, 1, 70, 1, 'mass')
scale_of_gamma = Scale(screen, scale_x, scale_y+40, cube.gamma, 0, 10, 0.1, 'gamma')
scale_of_g = Scale(screen, scale_x, scale_y+80, g, 0, 10, 0.01, 'g')
scale_of_k = Scale(screen, scale_x, scale_y+120, k, 1, 1400, 10, 'k')

done = False
while not done:
    screen.fill((0, 0, 0))  # закрашиваю экран черным
    pg.draw.rect(screen, green, (cube.pos[0]-15, cube.pos[1]-15, 30, 30))  # рисую квадрат
    prugina(screen, cube, k, dT)
    if pg.mouse.get_pressed()[0]:
        m_pos = pg.mouse.get_pos()
        if scale_of_mass.y <= m_pos[1] <= scale_of_mass.y+Scale.h:
            cube.mass = scale_of_mass.update(*m_pos)
        elif scale_of_small_mass.y <= m_pos[1] <= scale_of_small_mass.y+Scale.h:
            cube.mass = scale_of_small_mass.update(*m_pos)
        cube.gamma = scale_of_gamma.update(*m_pos)
        k = scale_of_k.update(*m_pos)
        if not horizont:  # если в вертикальном положении, то можно менять g
            g = scale_of_g.update(*m_pos) or g
    scale_of_mass.draw()
    scale_of_gamma.draw()
    scale_of_k.draw()
    scale_of_small_mass.draw()
    if not horizont:  # и рисовать ползунок
        scale_of_g.draw()
    for event in pg.event.get():  # проверяю все события
        if event.type == pg.QUIT:  # закрыть приложение на крестик
            done = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_TAB:  # на TAB менять положение пружины
                horizont = not horizont
                cube = Cube(screen, horizont, cube.mass, cube.gamma)
            elif event.key == pg.K_SPACE:  # выставляю значения дефолту
                cube = Cube(screen, horizont)
                g = 9.81
                k = 100
                scale_of_mass.__init__(*scale_of_mass.default)
                scale_of_gamma.__init__(*scale_of_gamma.default)
                scale_of_g.__init__(*scale_of_g.default)
                scale_of_k.__init__(*scale_of_k.default)
                scale_of_small_mass.__init__(*scale_of_small_mass.default)
    pg.display.flip()  # обновляем экран
    clock.tick(100)  # скорость обновления экрана
