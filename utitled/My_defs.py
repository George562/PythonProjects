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
    return My_fonts[font][(size-5) % 41].render(str(text), True, color)


class Slider:
    h = 20  # height
    rad = 10  # radius
    bg = yellow  # background
    l_c = white  # line color
    c_c = red  # circle color

    def __init__(self, win, w, x, y, pos, start, stop, step, name=''):
        self.win = win  # place for draw
        self.name = font_return(18, name) if name != '' else None
        self.x = x  # x coordinate
        self.y = y  # y coordinate
        self.w = w  # width
        self.scalar = self.x+int((self.w-10)*(pos-start)/(stop-start))+5  # pos of slider
        self.value = pos  # present value
        self.start = start  # minimum value
        self.stop = stop  # maximum value
        self.step = step  # value step
        self.name_x = self.x-self.name.get_width()-15 if name != '' else self.x
        self.default = (win, w, x, y, pos, start, stop, step, name)  # default parameters

    def draw(self):
        if self.name is not None:
            self.win.blit(self.name, [self.name_x, self.y])
        self.win.blit(font_return(18, self.value), [self.x+self.w+self.rad*3, self.y])
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

    def custom(self, rad=None, w=None, h=None, bg=None, l_c=None, c_c=None):
        self.rad = rad if rad is not None else self.rad
        self.w = w if w is not None else self.w
        self.h = h if h is not None else self.h
        self.bg = bg if bg is not None else self.bg
        self.l_c = l_c if l_c is not None else self.l_c
        self.c_c = c_c if c_c is not None else self.c_c


class Button:
    bc = (155, 0, 0)  # back color
    bs = 2  # board size
    active = False
    n_bc = red

    def __init__(self, win, w, h, x, y, text='', t_size=20, t_color=white, b_size=bs, b_color=bc):
        self.win = win
        self.w = w  # width
        self.h = h  # height
        self.x = x
        self.y = y
        self.text = font_return(t_size, text, t_color)
        self.text_pos = (x+(w-self.text.get_width())/2, y+(h-self.text.get_height())/2)
        self.bs = b_size  # board size
        self.bc = b_color  # back color
        self.sr = (self.bc[0]+self.bc[1]+self.bc[2])/3

    def draw(self):
        pg.draw.rect(self.win, self.n_bc, (self.x, self.y, self.w, self.h))
        pg.draw.rect(self.win, (130, 130, 130), (self.x, self.y, self.w, self.h), self.bs)
        self.win.blit(self.text, self.text_pos)

    def update(self, x, y, turn):
        if self.x <= x <= self.x+self.w and self.y <= y <= self.y+self.h:
            if not turn:
                self.n_bc = (abs(self.bc[0]-50) if self.sr >= 128 else self.bc[0]+35 if self.bc[0]+50 < 256 else 255,
                             abs(self.bc[1]-50) if self.sr >= 128 else self.bc[1]+35 if self.bc[1]+50 < 256 else 255,
                             abs(self.bc[2]-50) if self.sr >= 128 else self.bc[2]+35 if self.bc[2]+50 < 256 else 255)
                if self.active:
                    self.active = False
            else:
                self.n_bc = (abs(self.bc[0]-100) if self.sr >= 128 else self.bc[0]+70 if self.bc[0]+100 < 256 else 255,
                             abs(self.bc[1]-100) if self.sr >= 128 else self.bc[1]+70 if self.bc[1]+100 < 256 else 255,
                             abs(self.bc[2]-100) if self.sr >= 128 else self.bc[2]+70 if self.bc[2]+100 < 256 else 255)
                if not self.active:
                    self.active = True
                    self.draw()
                    return self.active
        else:
            self.n_bc = self.bc
        self.draw()
