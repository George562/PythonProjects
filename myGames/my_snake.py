import pygame
import random
scW = scH = 16*10
sc = pygame.display.set_mode((scW, scH))
spd = {'w': [0, -1, 's'], 'a': [-1, 0, 'd'], 's': [0, 1, 'w'], 'd': [1, 0, 'a']}
move_keys = {'w': 119, 'a': 97, 's': 115, 'd': 100}
s_spd = spd['d']
s = [[1, 1], [2, 1], [3, 1]]
for x, y in s:
    pygame.draw.rect(sc, (0, 255, 255), [x*16, y*16, 15, 15])
food = [scW//2, scH//2]
ms = scW//16  # width/height
pygame.draw.rect(sc, (255, 0, 0), [food[0]*16, food[1]*16, 15, 15])
loose = False
done = False
clock = pygame.time.Clock()
while not done:
    was_change = False  # was change
    for event in pygame.event.get():
        if event.type == 12:
            done = True
        if event.type == 2:
            if event.key == 27:
                done = True
            if event.key == 32:
                loose = False
                sc.fill((0, 0, 0))
                s_spd = spd['d']
                s = [[1, 1], [2, 1], [3, 1]]
                food = [scW//2, scH//2]
                pygame.draw.rect(sc, (255, 0, 0), [food[0]*16, food[1]*16, 15, 15])
                for x, y in s:
                    pygame.draw.rect(sc, (0, 255, 255), [x*16, y*16, 15, 15])
            for key in move_keys:
                if event.key == move_keys[key] and s_spd[2] != key and not was_change:
                    s_spd = spd[key]
                    was_change = True
    if s[-1] == food:
        while food in s:
            food = [random.randint(0, ms-1), random.randint(0, ms-1)]
        pygame.draw.rect(sc, (255, 0, 0), [food[0]*16, food[1]*16, 15, 15])
        s.append([s[-1][0]+s_spd[0], s[-1][1]+s_spd[1]])
        print(len(s))
    elif not loose:
        block = s.pop(0)
        pygame.draw.rect(sc, (0, 0, 0), [block[0]*16, block[1]*16, 15, 15])
        s.append([s[-1][0]+s_spd[0], s[-1][1]+s_spd[1]])
    pygame.draw.rect(sc, (0, 255, 255), [s[-1][0]*16, s[-1][1]*16, 15, 15])
    if s[-1] in s[:-1] or s[-1][0] in [-1, ms] or s[-1][1] in [-1, ms]:
        loose = True
    pygame.display.update()
    clock.tick(4+len(s)//10)
