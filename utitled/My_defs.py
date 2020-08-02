import pygame as pg

pg.init()

# colors
black  = (  0,   0,   0)
blue   = (  0,   0, 255)
green  = (  0, 255,   0)
sea    = (  0, 255, 255)
red    = (255,   0,   0)
purple = (255,   0, 255)
yellow = (255, 255,   0)
white  = (255, 255, 255)

My_fonts = {}  # used fonts


def font_return(size, text, color=white, font='verdana'):
    if font not in My_fonts.keys():  # if font not in list, add it
        My_fonts[font] = [pg.font.SysFont(font, i) for i in range(5, 46)]
    return My_fonts[font][(size - 5) % 41].render(str(text), True, color)


def zoom(arr, x, y, k):
    for i in range(len(arr)):
        arr[i] = (arr[i][0] - x) * k + x, (arr[i][1] - y) * k + y, *arr[i][2:]


motion = (lambda arr, rel: list(map(lambda i: (i[0] + rel[0], i[1] + rel[1]), arr)))


class Slider:
    bg = yellow  # background
    l_c = white  # line color
    c_c = red  # circle color

    def __init__(self, win, w, x, y, pos, start, stop, step, name='', h=20, rad=10):
        self.win = win  # place for draw
        self.name = font_return(18, name) if name != '' else None
        self.x = x  # x coordinate
        self.y = y  # y coordinate
        self.w = w  # width
        self.h = h  # height
        self.rad = rad
        self.scalar = self.x + int((self.w - 10) * (pos - start) / (stop - start)) + 5  # pos of slider
        self.value = pos  # present value
        self.start = start  # minimum value
        self.stop = stop  # maximum value
        self.step = step  # value step
        self.name_x = self.x - self.name.get_width() - 15 if name != '' else self.x
        self.default = (win, w, x, y, pos, start, stop, step, name)  # default parameters

    def draw(self):
        if self.name is not None:
            self.win.blit(self.name, [self.name_x, self.y])
        self.win.blit(font_return(18, self.value), [self.x + self.w + self.rad * 3, self.y])
        pg.draw.rect(self.win, self.bg, (self.x - self.rad, self.y - 3, self.w + self.rad * 3, self.h + 9))  # bg
        pg.draw.line(self.win, self.l_c, (self.x + self.rad / 2, self.y + self.h // 2),
                     (self.x + self.w + self.rad / 2, self.y + self.h // 2), 4)  # slider line
        pg.draw.circle(self.win, self.c_c, (self.scalar, self.y + self.h // 2 + 1), self.rad)  # slider

    def update(self, x, y):  # update external value
        if 0 <= x - self.x <= self.w + 1 and 0 <= y - self.y <= self.h:
            self.value = (x - self.x) / self.w * (self.stop - self.start) + self.start
            self.value = round(self.value - self.value % self.step, 4)
            self.scalar = self.x + round(self.w * self.value / (self.stop - self.start))
        if not self.value % 1:
            self.value = int(self.value)
        return self.value


class Button:
    bc = (255, 0, 0)  # back color
    bs = 2  # board size
    active = False

    def __init__(self, win, w, h, x, y, text='', t_size=20, t_color=white, b_size=bs, b_color=bc):
        self.win = win
        self.w = w  # width
        self.h = h  # height
        self.x = x
        self.y = y
        self.text = font_return(t_size, text, t_color)
        self.text_pos = (x + (w - self.text.get_width()) / 2, y + (h - self.text.get_height()) / 2)
        self.bs = b_size  # board size
        self.bc = b_color  # back color

    def draw(self):
        pg.draw.rect(self.win, self.bc, (self.x, self.y, self.w, self.h))
        pg.draw.rect(self.win, (130, 130, 130), (self.x, self.y, self.w, self.h), self.bs)
        self.win.blit(self.text, self.text_pos)

    def update(self, x, y, turn):
        if 0 <= x - self.x <= self.w and 0 <= y - self.y <= self.h:
            if not turn:
                self.active = False
            else:
                if not self.active:
                    self.active = True
                    self.draw()
                    return self.active
        self.draw()


class Entry:
    actTyp = None  # which is active now
    h = 30  # height

    def __init__(self, win, w, x, y, value, name=''):
        self.win = win  # place for draw
        self.name = font_return(18, name) if name != '' else None
        self.x = x  # x coordinate
        self.y = y  # y coordinate
        self.w = w  # width
        self.value = value  # present value
        self.name_x = self.x - self.name.get_width() - 10 if name != '' else self.x
        self.default = (win, w, x, y, value, name)  # default parameters

    def draw(self):
        if self.name is not None:
            self.win.blit(self.name, [self.name_x, self.y])
        val = font_return(18, self.value)  # font of self.value
        self.win.blit(val, [self.x + (self.w - val.get_width()) / 2, self.y + (self.h - val.get_height()) / 2])
        pg.draw.rect(self.win, white, (self.x, self.y, self.w, self.h), 2)  # bg

    def update(self, x, y):  # x and y is some coordinates
        if 0 <= x - self.x <= self.w and 0 <= y - self.y <= self.h:
            if pg.mouse.get_pressed()[0]:
                Entry.actTyp = self
                self.value = 0


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if type(other) == float or type(other) == int:
            return Point(self.x * other, self.y * other)

    def __truediv__(self, other):
        if type(other) == float or type(other) == int:
            return Point(self.x / other, self.y / other)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __str__(self):
        return f'({self.x}; {self.y})'

    def __int__(self):
        self.x, self.y = self.x // 1, self.y // 1
        return self
