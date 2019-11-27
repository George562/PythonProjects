import pygame
pygame.init()


def back():
    sc.fill((0, 0, 0) if color_steal else (255, 255, 255))
    for i in range(0, sc_w, c_size):
        pygame.draw.line(sc, gray, [i, 0], [i, sc_h])
    for i in range(0, sc_h, c_size):
        pygame.draw.line(sc, gray, [0, i], [sc_w, i])
    for i in crosses:
        pygame.draw.line(sc, red, i, [i[0]+c_size, i[1]+c_size], 3)
        pygame.draw.line(sc, red, [i[0]+c_size, i[1]], [i[0], i[1]+c_size], 3)
    for i in circle:
        pygame.draw.ellipse(sc, (0, 0, 255), [i[0], i[1], c_size, c_size], 3)
    mini_update()
    pygame.display.update()


def added():
    p = [pos[0]-pos[0] % c_size, pos[1]-pos[1] % c_size]
    if first and p not in crosses+circle:
        crosses.append(p)
        pygame.draw.line(sc, red, p, [p[0]+c_size, p[1]+c_size], 3)
        pygame.draw.line(sc, red, [p[0]+c_size, p[1]], [p[0], p[1]+c_size], 3)
    elif p not in circle+crosses:
        circle.append(p)
        pygame.draw.ellipse(sc, (0, 0, 255), [p[0], p[1], c_size, c_size], 3)
    else:
        return 1


def move(chan):
    for i in range(len(crosses)):
        crosses[i] = [crosses[i][0]+chan[0], crosses[i][1]+chan[1]]
    for i in range(len(circle)):
        circle[i] = [circle[i][0]+chan[0], circle[i][1]+chan[1]]


def mini_update():
    mini.fill((0, 0, 0) if color_steal else (255, 255, 255))
    if first:
        pygame.draw.line(mini, red, [0, 0], [mini_c_size, mini_c_size], 3)
        pygame.draw.line(mini, red, [0, mini_c_size], [mini_c_size, 0], 3)
    else:
        pygame.draw.ellipse(mini, (0, 0, 255), [0, 0, mini_c_size, mini_c_size])
    sc.blit(mini, [3, 3])


gray = (75, 75, 75)
red = (255, 0, 0)
sc_w = 810
sc_h = 660
c_size = 30
mini_c_size = 10
color_steal = True
first = True
crosses = []
circle = []
done = False
map_change = {274: [0, -c_size], 273: [0, c_size], 276: [c_size, 0], 275: [-c_size, 0]}
sc = pygame.display.set_mode((sc_w, sc_h))
pygame.display.set_caption('крестики-нолики')
mini = pygame.Surface((mini_c_size, mini_c_size))
back()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if event.button == 1:
                if added() is None:
                    first = not first
                    mini_update()
                    pygame.display.update()
        if event.type == pygame.KEYDOWN:
            if event.key == 9:
                color_steal = not color_steal
            if event.key in range(273, 277):
                move(map_change[event.key])
            back()
pygame.quit()
