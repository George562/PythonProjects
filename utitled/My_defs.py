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


def font_return(size, text, font='verdana', color=white):
    if font not in My_fonts.keys():  # if font not in list, add it
        My_fonts[font] = [pg.font.SysFont(font, i) for i in range(5, 46)]
    return My_fonts[font][(size-5)%41].render(str(text), True, color)


class Slider:
    w = 180  # width
    h = 20  # height
    rad = 10  # radius
    bg = yellow  # background
    l_c = white  # line color
    c_c = red  # circle color

    def __init__(self, win, x, y, pos, start, stop, step, name=''):
        self.win = win  # place for draw
        self.name = font_return(18, name, 'verdana') if name != '' else None
        self.x = x  # x coordinate
        self.y = y  # y coordinate
        self.scalar = self.x+int((self.w-10)*(pos-start)/(stop-start))+5  # pos of slider
        self.value = pos  # present value
        self.start = start  # minimum value
        self.stop = stop  # maximum value
        self.step = step  # value step
        self.name_x = self.x-self.name.get_width()-15 if name != '' else self.x
        self.default = (win, x, y, pos, start, stop, step, name, self.w, self.h)  # default parameters

    def draw(self):
        if self.name is not None:
            self.win.blit(self.name, [self.name_x, self.y])
        self.win.blit(font_return(18, self.value, 'verdana'), [self.x+self.w+self.rad*3, self.y])
        pg.draw.rect(self.win, self.bg, (self.x-self.rad, self.y-3, self.w+self.rad*3, self.h+9))  # bg
        pg.draw.line(self.win, self.l_c, (self.x+self.rad/2, self.y+self.h//2),
                     (self.x+self.w+self.rad/2, self.y+self.h//2), 4)  # slider line
        pg.draw.circle(self.win, self.c_c, (self.scalar, self.y+self.h//2+1), self.rad)  # slider

    def update(self, x, y):  # update external value
        if self.x <= x <= self.x+self.w+1 and self.y <= y <= self.y+self.h:
            self.value = (x-self.x)/self.w*(self.stop-self.start)+self.start
            self.value = round(self.value-self.value % self.step, 4)
            self.scalar = self.x+round(self.w*self.value/(self.stop-self.start))
        if not self.value % 1:
            self.value = int(self.value)
        return self.value

    def customize(self, rad=None, w=None, h=None, bg=None, l_c=None, c_c=None):
        self.rad = rad if rad is not None else self.rad
        self.w = w if w is not None else self.w
        self.h = h if h is not None else self.h
        self.bg = bg if bg is not None else self.bg
        self.l_c = l_c if l_c is not None else self.l_c
        self.c_c = c_c if c_c is not None else self.c_c


class Button:
    w = 150
    h = 30
