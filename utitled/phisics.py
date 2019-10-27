import pygame
width = 720
height = 540
radius = 25
screen = pygame.display.set_mode((width, height))
x = 100
y = 100
gravity = 1
tr = 3.5   # trenie
y_speed = 0
x_speed = 0
clock = pygame.time.Clock()
done = False
while not done:
    pressed = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()
    screen.fill((0, 0, 15))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                y_speed = - (radius - pos[1]/16)
                x = radius
                x_speed = pos[0]/16
                y = height-radius
    if y < radius:
        y = radius
        y_speed = abs(y_speed)-tr if abs(y_speed) > tr else 0
        x_speed = x_speed-tr/20 if x_speed > 0 else x_speed+tr/5 if abs(x_speed)-tr/20 > 0 else 0
    elif y > height-radius:
        y = height-radius
        y_speed = -abs(y_speed)+tr if abs(y_speed) > tr else 0
        x_speed = x_speed-tr/20 if x_speed > 0 else x_speed+tr/5 if abs(x_speed)-tr/20 > 0 else 0
    if x > width-radius:
        x = width - radius
        x_speed = -x_speed+tr if abs(x_speed) > tr else 0
    elif x < radius:
        x = radius
        x_speed = abs(x_speed)-tr if abs(x_speed) > tr else 0
    y += y_speed
    y_speed += gravity
    x += x_speed
    pygame.draw.circle(screen, (0, 0, 255), [int(x), int(y)], radius)
    pygame.display.flip()
    clock.tick(60)
