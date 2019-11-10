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
    return My_fonts[font][size].render(str(text), True, color)


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
