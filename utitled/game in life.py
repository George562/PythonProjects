import pygame


def draw_line():
    for k in range(1, n+1):
        pygame.draw.line(screen, black, [0, k*c_s], [width, k*c_s], 1)
        pygame.draw.line(screen, black, [k*c_s, 0], [k*c_s, height], 1)
        pygame.display.update()


def filling_red(x=0, y=0, fill=True):
    pos = pygame.mouse.get_pos()
    x, y = pos[0]-pos[0] % c_s, pos[1]-pos[1] % c_s
    if fill and [x, y] not in f_cell:
        f_cell.append([x, y])
        pygame.draw.rect(screen, red, [x+1, y+1, c_s-1, c_s-1])
        pygame.display.update()
    elif not fill and [x, y] in f_cell:
        f_cell.remove([x, y])
        pygame.draw.rect(screen, white, [x+1, y+1, c_s-1, c_s-1])
        pygame.display.update()


def searching(c, old_c, m=0):
    if [(c[0]+c_s) if c[0] < top else 0, c[1]] in old_c:  # справа
        m += 1
    if [(c[0]-c_s) if c[0] > 0 else top, c[1]] in old_c:  # слева
        m += 1
    if [c[0], (c[1]+c_s) if c[1] < top else 0] in old_c:  # снизу
        m += 1
    if [c[0], (c[1]-c_s) if c[1] > 0 else top] in old_c:  # сверху
        m += 1
    if [(c[0]+c_s) if c[0] < top else 0, (c[1]+c_s) if c[1] < top else 0] in old_c:  # справа снизу
        m += 1
    if [(c[0]+c_s) if c[0] < top else 0, (c[1]-c_s) if c[1] > 0 else top] in old_c:  # справа сверху
        m += 1
    if [(c[0]-c_s) if c[0] > 0 else top, (c[1]+c_s) if c[1] < top else 0] in old_c:  # слева снизу
        m += 1
    if [(c[0]-c_s) if c[0] > 0 else top, (c[1]-c_s) if c[1] > 0 else top] in old_c:  # слева сверху
        m += 1
    return m


def play():
    for cell in g_map:
        search = searching(cell, old_f_cell)
        if cell not in old_f_cell:
            if search == 3:  # add cell
                f_cell.append(cell)
                pygame.draw.rect(screen, red, [cell[0]+1, cell[1]+1, c_s-1, c_s-1])
        else:
            if search < 2 or search > 3:  # death of cell
                f_cell.remove(cell)
                pygame.draw.rect(screen, white, [cell[0]+1, cell[1]+1, c_s-1, c_s-1])
    pygame.display.update()


white = (200, 200, 200)
black = (0, 0, 0)
red = (255, 0, 0)

old_f_cell = []  # old fill cells
f_cell = []  # fill cells
n = 30  # number cells in line/column
c_s = 25  # cell size
top = c_s*(n-1)
height = width = c_s*n
clock = pygame.time.Clock()
g_map = [[i*c_s, j*c_s] for i in range(n+1) for j in range(n+1)]  # game map
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('игра в жизнь')
screen.fill(white)
draw_line()
done = playing = False
while not done:
    if pygame.mouse.get_pressed()[0]:
        filling_red()
    elif pygame.mouse.get_pressed()[2]:
        filling_red(fill=False)
    if playing:
        play()
        clock.tick(25)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                playing = not playing
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button in [1, 3]:
                draw_line()
    old_f_cell = f_cell.copy()
pygame.quit()
