import pygame
from random import randint
pygame.font.init()


def font(size: int, text, colour=(255, 255, 255)):
    return pygame.font.SysFont('verdana', size).render(str(text), True, colour)


def button(x, y, text):
    sc.blit(font(18, text, green if difficult == text else white), [x, y])


def change_difficult(dif):
    global bombs, cells, sc, sc_w, sc_h, loose, win
    loose = False
    win = False
    num_x, num_y = k_dif[dif][0]
    num_bombs = k_dif[dif][1]
    bombs = []
    for x in range(num_bombs):
        b_pos = [randint(0, num_x-1), randint(0, num_y-1)]
        while b_pos in bombs:
            b_pos = [randint(0, num_x-1), randint(0, num_y-1)]
        else:
            bombs.append(Bomb(*b_pos))
    cells = []
    sc_w = num_x * c_size
    sc_h = num_y * c_size + bd_h
    sc = pygame.display.set_mode((sc_w, sc_h))
    pygame.display.set_caption('сапер')
    for but in buttons:
        button(*but)
    pygame.draw.rect(sc, white, [sc_w/2-50, 40, 100, 30])
    sc.blit(font(25, 'Начать', black), [sc_w/2-45, 40])
    for i in range(num_x):
        for j in range(num_y):
            if not [i, j] in [[bom.x, bom.y] for bom in bombs]:
                cells.append(Cell(i, j, cells))
            pygame.draw.rect(sc, gray[140], [i*c_size, j*c_size + bd_h, *[c_size - 1] * 2])
            pygame.draw.rect(sc, white, [i*c_size, j*c_size + bd_h, c_size - 1, 2])
            pygame.draw.rect(sc, white, [i*c_size, j*c_size + bd_h, 2, c_size - 1])


def search(x, y):
    m = 0
    for c in [x+1, y], [x, y+1], [x+1, y+1], [x-1, y+1], [x+1, y-1], [x-1, y], [x, y-1], [x-1, y-1]:
        if c in [[bom.x, bom.y] for bom in bombs]:
            m += 1
    return m


def empty(x, y):
    for c in cells:
        for d in [x+1, y], [x, y+1], [x-1, y], [x, y-1]:
            if [c.x, c.y] == d:
                c.update('open')
        for d in [x+1, y+1], [x-1, y+1], [x+1, y-1], [x-1, y-1]:
            if [c.x, c.y] == d and search(c.x, c.y) != 0:
                c.update('open')


class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.activate = False
        self.blocked = False

    def turn(self):
        x, y = self.x*c_size, self.y*c_size
        if x < pos[0] < x+c_size and y < pos[1]-bd_h < y+c_size and not self.blocked:
            self.activate = True

    def draw(self):
        pygame.draw.rect(sc, gray[140], [self.x * c_size, self.y * c_size + bd_h, *[c_size - 1] * 2])
        pygame.draw.circle(sc, red, [self.x*c_size+c_size//2, self.y*c_size+c_size//2+bd_h], rad)

    def update(self):
        x, y = self.x*c_size, self.y*c_size
        if x < pos[0] < x+c_size and y < pos[1]-bd_h < y+c_size:
            if self.blocked:
                pygame.draw.rect(sc, gray[140], [self.x * c_size, self.y * c_size + bd_h, *[c_size - 1] * 2])
                pygame.draw.rect(sc, white, [self.x * c_size, self.y * c_size + bd_h, c_size - 1, 2.9])
                pygame.draw.rect(sc, white, [self.x * c_size, self.y * c_size + bd_h, 2.9, c_size - 1])
            else:
                pygame.draw.circle(sc, blue, [self.x*c_size+c_size//2, self.y*c_size+c_size//2+bd_h], rad)
            self.blocked = not self.blocked


class Cell:
    def __init__(self, x, y, we):
        self.x = x
        self.y = y
        self.state = 'close'
        self.number = 0
        self.was_draw = False
        self.we = we

    def draw(self):
        if self.state == 'close':
            pygame.draw.rect(sc, gray[140], [self.x * c_size, self.y * c_size + bd_h, *[c_size - 1] * 2])
            pygame.draw.rect(sc, white, [self.x * c_size, self.y * c_size + bd_h, c_size - 1, 2.9])
            pygame.draw.rect(sc, white, [self.x * c_size, self.y * c_size + bd_h, 2.9, c_size - 1])

    def update(self, method=True):
        x, y = self.x*c_size, self.y*c_size
        if method == 'open' and self.state != 'open' and self.state != 'block':
            self.state = 'open'
            self.number = search(self.x, self.y)
            pygame.draw.rect(sc, gray[140], [self.x * c_size, self.y * c_size + bd_h, *[c_size - 1] * 2])
            if self.number > 0:
                sc.blit(font(15, self.number, black), [self.x * c_size + 5, self.y * c_size + 5 + bd_h])
            else:
                empty(self.x, self.y)
        elif x < pos[0] < x+c_size and y < pos[1]-bd_h < y+c_size and self.state != 'open':
            if method and self.state == 'close':
                self.state = 'open'
                self.number = search(self.x, self.y)
                pygame.draw.rect(sc, gray[140], [self.x * c_size, self.y * c_size + bd_h, *[c_size - 1]*2])
                if self.number > 0:
                    sc.blit(font(15, self.number, black), [self.x * c_size + 5, self.y * c_size + 5 + bd_h])
                else:
                    empty(self.x, self.y)
            if not method:
                if self.state == 'close':
                    self.state = 'block'
                    pygame.draw.circle(sc, blue, [self.x*c_size+c_size//2, self.y*c_size+c_size//2+bd_h], rad)
                else:
                    self.state = 'close'
                    self.draw()


white = (255, 255, 255)
black = (5, 5, 15)
gray = [(i, i, i) for i in range(256)]
red = (175, 0, 0)
blue = (0, 0, 255)
green = (0, 175, 0)
c_size = 26
bd_h = 80
rad = c_size//2-4
bombs = []
cells = []
buttons = [[10, 5, 'easy'], [80, 5, 'normal'], [175, 5, 'hard'], [240, 5, 'master'], [335, 5, 'impossible']]

difficult = 'easy'
k_dif = {'easy': [[17, 11], 25], 'normal': [[24, 14], 60], 'hard': [[31, 17], 125], 'master': [[38, 20], 220],
         'impossible': [[45, 23], 350]}
sc_w, sc_h = 1, 1
sc = pygame.display.set_mode((k_dif[difficult][0]))
change_difficult(difficult)
posses = {'easy': range(10, 56), 'normal': range(80, 146), 'hard': range(175, 220), 'master': range(240, 310),
          'impossible': range(335, 436)}
loose = False
win = False
pos = ()
m_press = None


def main():
    global pos, m_press, win, loose, difficult
    done = False
    while not done:
        pos = pygame.mouse.get_pos()
        m_press = pygame.mouse.get_pressed()
        if not loose and not win:
            if len(bombs) == len(cells) == 0:
                win = True
            if any([bomb.activate for bomb in bombs]):
                for bob in bombs:
                    bob.draw()
                loose = True
        elif win:
            win_text = font(65, 'Победа', (200, 47, 0))
            sc.blit(win_text, [sc_w/2-win_text.get_width()/2, sc_h/2-win_text.get_height()/2])
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if pos[1] <= 30:
                        for key in posses:
                            if pos[0] in posses[key]:
                                difficult = key
                                change_difficult(difficult)
                                break
                    if sc_w/2-50 <= pos[0] <= sc_w/2+50 and 40 <= pos[1] <= 70:
                        change_difficult(difficult)
                    if not loose and not win:
                        for cell in cells:
                            cell.update()
                        for bomb in bombs:
                            bomb.turn()
                if event.button == 3:
                    if not loose and not win:
                        for cell in cells:
                            cell.update(False)
                        for bomb in bombs:
                            bomb.update()


if __name__ == '__main__':
    main()
