import pygame

pygame.init()


def back():
    sc.fill((0, 0, 0) if color_steal else (255, 255, 255))
    for i in range(0, sc_w, c_size):
        pygame.draw.line(sc, (75, 75, 75), [i, 0], [i, sc_h])
    for i in range(0, sc_h, c_size):
        pygame.draw.line(sc, (75, 75, 75), [0, i], [sc_w, i])
    for i in crosses:
        pygame.draw.line(sc, red, i, [i[0] + c_size, i[1] + c_size], 3)
        pygame.draw.line(sc, red, [i[0] + c_size, i[1]], [i[0], i[1] + c_size], 3)
    for i in circle:
        pygame.draw.ellipse(sc, (0, 0, 255), [i[0], i[1], c_size, c_size], 3)
    mini_update()
    pygame.display.update()


def added(pos):
    p = [pos[0] - pos[0] % c_size, pos[1] - pos[1] % c_size]
    if len(crosses) == len(circle) and p not in crosses + circle:
        crosses.append(p)
        pygame.draw.line(sc, red, p, [p[0] + c_size, p[1] + c_size], 3)
        pygame.draw.line(sc, red, [p[0] + c_size, p[1]], [p[0], p[1] + c_size], 3)
    elif p not in circle + crosses:
        circle.append(p)
        pygame.draw.ellipse(sc, (0, 0, 255), [p[0], p[1], c_size, c_size], 3)
    else:
        return 1


def mini_update():
    pygame.draw.rect(sc, (0, 0, 0) if color_steal else (255, 255, 255), [0, 0, mini_c_size, mini_c_size])
    if len(crosses) == len(circle):
        pygame.draw.line(sc, red, [0, 0], [mini_c_size, mini_c_size], 3)
        pygame.draw.line(sc, red, [0, mini_c_size], [mini_c_size, 0], 3)
    else:
        pygame.draw.ellipse(sc, (0, 0, 255), [0, 0, mini_c_size, mini_c_size])


red = (255, 0, 0)
sc_w, sc_h = 810, 660
c_size, mini_c_size = 30, 10
color_steal = True
crosses = []
circle = []
map_change = {274: [0, c_size], 273: [0, -c_size], 276: [-c_size, 0], 275: [c_size, 0]}
sc = pygame.display.set_mode((sc_w, sc_h))
pygame.display.set_caption('крестики-нолики')
back()
while 1:
    event = pygame.event.wait()
    if event.type == pygame.QUIT: break
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            if added(pygame.mouse.get_pos()) is None:
                mini_update()
                pygame.display.update()
    if event.type == pygame.KEYDOWN:
        if event.key == 9:
            color_steal = not color_steal
        if event.key in map_change:
            chan = map_change[event.key]
            for j in range(len(crosses)):
                crosses[j] = [crosses[j][0] + chan[0], crosses[j][1] + chan[1]]
            for j in range(len(circle)):
                circle[j] = [circle[j][0] + chan[0], circle[j][1] + chan[1]]
        back()
