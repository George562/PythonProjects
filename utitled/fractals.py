import pygame

width = height = 600
screen = pygame.display.set_mode((600, 600))
white = (255, 255, 255)
black = (5, 5, 15)
alpha = 1


def figure_turn(p_list, deep=10):
    a = p_list[0]
    le = len(p_list)
    if deep < 1:
        return
    for i in range(le-1):
        pygame.draw.aaline(screen, white, p_list[i], p_list[i+1])
    pygame.draw.aaline(screen, white, p_list[le-1], p_list[0])
    for i in range(le-1):
        p_list[i] = [p_list[i][0]*(1-alpha)+p_list[i+1][0]*alpha, p_list[i][1]*(1-alpha)+p_list[i+1][1]*alpha]
    p_list[le-1] = [p_list[le-1][0]*(1-alpha)+a[0]*alpha, p_list[le-1][1]*(1-alpha)+a[1]*alpha]
    figure_turn(p_list, deep-1)


clock = pygame.time.Clock()
done = False
pause = False
s = {'down': -0.01, 'up': 0.01}
ch = 'down'
while not done:
    if not pause:
        screen.fill(black)
    # figure_turn([[100, 100], [250, 300], [100, 500], [300, 350], [500, 500], [350, 300], [500, 100], [300, 250]], 100)
        # figure_turn([[100, 100], [100, 500], [500, 500], [500, 100]], 30)
        press = pygame.key.get_pressed()
        alpha += s[ch]
        if alpha < 0:
            ch = 'up'
        elif alpha >= 1:
            ch = 'down'
        if press[pygame.K_UP] and alpha <= 1.49:
            alpha += 0.01
        if press[pygame.K_DOWN] and alpha >= 0:
            alpha -= 0.01
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == 32:
                pause = not pause
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4 and alpha <= 1.49:  # прокрутка вверх
                alpha += 0.01
            if event.button == 5 and alpha >= 0:  # прокрутка вниз
                alpha -= 0.01
    pygame.display.update()
    clock.tick(15)
