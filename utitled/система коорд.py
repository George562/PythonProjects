import pygame


def zoomer(arr: list, param, center: list):
    x, y = center
    for i in range(len(arr)):
        arr[i] = ((arr[i][0] - x) * param + x, (arr[i][1] - y) * param + y)
    return arr


pygame.init()
black = (7, 7, 20)
white = (255, 255, 255)
gray = (70, 70, 70)
width = 1080
height = 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
rel_x = rel_y = del_y = del_x = 0
k = 1.1**36
font = pygame.font.SysFont('Comic Sans MS', 13)
zero_text = font.render('0', True, white)
done = False
while not done:
    screen.fill(black)
    # оси координат
    pygame.draw.aaline(screen, white, [0, height//2+rel_y], [width, height//2+rel_y], True)
    pygame.draw.aaline(screen, white, [width//2+rel_x, 0], [width//2+rel_x, height], True)
    screen.blit(zero_text, [width//2-15 + rel_x, rel_y+height//2])
    # движение всей системы
    if pygame.mouse.get_pressed()[0]:
        rel2 = pygame.mouse.get_rel()
        rel_x += rel2[0]
        rel_y += rel2[1]
    rel1 = pygame.mouse.get_rel()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            if event.key == pygame.K_SPACE:  # сброс всего
                rel_x = rel_y = 0
                k = 1.1**36
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2:  # перемещает в записанное положение
                rel_x = del_x
                rel_y = del_y
            if event.button == 3:  # записывает положение
                del_x = -pygame.mouse.get_pos()[0]+width//2+rel_x
                del_y = -pygame.mouse.get_pos()[1]+height//2+rel_y
            if event.button == 4:  # прокрутка вверх
                k *= 1.1
            if event.button == 5:  # прокрутка вниз
                k /= 1.1
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
