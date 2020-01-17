import pygame
from random import randint

pygame.init()


def font(size: int, text, colour=(255, 255, 255)):
    return pygame.font.SysFont('virgina', size).render(str(text), True, colour)


def load(file, k=0):
    place = ['player sprites/', 'enemy sprites/', 'state sprites/']
    return pygame.image.load(place[k] + file + '.png').convert()


def add(e, j, arr):
    print(e)
    for i1 in range(e[0]):
        ss = 2 if randint(0, 100) <= 15 else 1
        arr[0].append(Enemy(randint(0, 1) * scw - 26, player.y, j[0] * i1, en_hp[0] * ss, en_mny[0] * ss, com1_l,
                            com1_r, en_spd[0] * ss, en_dmg[0] * ss, 18, en_exp[0] * ss))
    for i1 in range(e[1]):
        ss = 2 if randint(0, 100) <= 20 else 1
        arr[1].append(Enemy(randint(0, 1) * scw - 26, player.y, j[1] * i1, en_hp[1] * ss, en_mny[1] * ss, com2_l,
                            com2_r, en_spd[1], en_dmg[1] * ss, 21, en_exp[1] * ss))
    for i1 in range(e[2]):
        ss = 2 if randint(0, 100) <= 10 else 1
        arr[2].append(Enemy(randint(0, 1) * scw - 26, player.y, j[2] * i1, en_hp[2] * ss, en_mny[2] * ss, rar1_l,
                            rar1_r, en_spd[2], en_dmg[2] * ss, 15, en_exp[2] * ss))
    for i1 in range(e[3]):
        ss = 2 if randint(0, 100) <= 10 else 1
        arr[3].append(Enemy(randint(0, 1) * scw - 26, player.y, j[3] * i1, en_hp[3] * ss, en_mny[3] * ss, rar2_l,
                            rar2_r, en_spd[3], en_dmg[3] * ss, 19, en_exp[3] * ss))
    if wave_number % 5 == 0:
        arr[4].append(Enemy(randint(0, 1) * scw - 26, player.y, 0, en_hp[4], en_mny[4], bos1_l, bos1_r,
                            en_spd[4], en_dmg[4], 18, en_exp[4]))
    if wave_number % 7 == 0:
        arr[5].append(Enemy(randint(0, 1) * scw - 26, player.y, 0, en_hp[5], en_mny[5], bos2_l, bos2_r,
                            en_spd[5], en_dmg[5], 18, en_exp[5]))
    return arr


def data_loading(d):
    ret = []
    for i1 in d.split('\n'):
        if '[' in i1:
            ret.append([])
            i1 = i1.replace('[', '')
            i1 = i1.replace(']', '')
            for el in i1.split(', '):
                if el.isdigit():
                    ret[-1].append(int(el))
                else:
                    ret[-1].append(float(el))
        else:
            try:
                ret.append(int(i1))
            except ValueError:
                try:
                    ret.append(float(i1))
                except ValueError:
                    ret.append(i1 == 'True')
    return ret


def saves(local_data, location='wave data.txt'):
    data1 = open(location, 'w')
    data1.write('')
    data1.close()
    data1 = open(location, 'a')
    for i1 in range(len(local_data)):
        if type(local_data[i1]) == dict:
            local_data[i1] = list(local_data[i1].values())
        data1.write(str(local_data[i1]))
        if i1 != len(local_data)-1:
            data1.write('\n')
    data1.close()
    data1 = open(location)
    data1.close()


white = (255, 255, 255)
black = (0, 0, 0)
gray = [(i, i, i) for i in range(1, 255)]
red = [(100, 0, 0), (255, 0, 0), (255, 100, 100), (255, 175, 175)]
green = (100, 255, 100)
yellow = (0, 255, 255)

jpg = pygame.image.load

scw = 640
sch = 320
screen_visible = 'start screen'
screen = pygame.display.set_mode((scw, sch))
pygame.display.set_caption('some shooter')
start_screen = [jpg('state sprites/main screen.jpg'), jpg('state sprites/full main screen.jpg')]
screen.blit(start_screen[0], [0, 0])
pygame.display.update()
battle_bg = [jpg('state sprites/bg.jpg'), jpg('state sprites/full bg.jpg')]
setting_bg = [jpg('state sprites/sett.jpg'), jpg('state sprites/full sett.jpg')]
hp = [load('hp', 2), load('full_hp', 2)]
icon = jpg('state sprites/icon.jpg')
lvl_up = load('lvl up', 2)
lvl_up.set_colorkey(white)
save = [load('save delete', 2), load('full save delete', 2)]
save[0].set_colorkey(white)
save[1].set_colorkey(white)
for i in hp:
    i.set_colorkey(white)
pygame.display.set_icon(icon)
full_screen = False


class Player:
    def __init__(self):
        self.w = 30  # width
        self.h = 40  # height
        self.x = scw / 2  # start point x
        self.y = 300  # start point y
        self.speed = 3.5  # speed of move
        self.hp = {'now': 50, 'max': 50}  # now hp; max hp
        self.wave_money = {'now': 0, 'max': 0}  # money in battle
        self.money = 0  # main money
        self.kills = 0  # kills for all battle
        self.exp = {'now': 0, 'max': 200}  # now exp; exp for next level
        self.lvl = 1  # level
        self.arm = {'max': 50, 'now': 50, 'buyOne': 3, 'priceUpToOne': 1.2, 'buyUp': 250, 'priceUpToUp': 1.35}
        self.arm_fill = [1 / 120, 1 / 60, 0, 275, 0.45]
        self.gun = guns[0]  # active gun
        self.side = 'center'
        self.last_side = 'right'
        self.jump = [False, 13, 13]  # jump[0: True/False, 1: state, 2: dynamic]
        self.right = [0, load('right1'), load('right2'), load('right3'), load('right4'), load('right5'), load('right6'),
                      load('right7'), load('right8'), load('full_right1'), load('full_right2'), load('full_right3'),
                      load('full_right4'), load('full_right5'), load('full_right6'), load('full_right7'),
                      load('full_right8'), load('stay_right'), load('full_stay_right')]
        self.left = [0, load('left1'), load('left2'), load('left3'), load('left4'), load('left5'), load('left6'),
                     load('left7'), load('left8'), load('full_left1'), load('full_left2'), load('full_left3'),
                     load('full_left4'), load('full_left5'), load('full_left6'), load('full_left7'),
                     load('full_left8'), load('stay_left'), load('full_stay_left')]
        for image in self.left[1:]:
            image.set_colorkey((255, 255, 255))
        for image in self.right[1:]:
            image.set_colorkey((255, 255, 255))

    def move(self, press):
        if press[pygame.K_w] and self.y > sch - (33 * f):
            self.y -= self.speed
        if press[pygame.K_s] and self.y < sch:
            self.y += self.speed
        if press[pygame.K_a] and self.x > 0:
            self.x -= self.speed
            self.side = 'left'
            self.last_side = 'left'
        elif press[pygame.K_d] and self.x < scw - self.w:
            self.x += self.speed
            self.side = 'right'
            self.last_side = 'right'
        else:
            self.side = 'center'
        if press[pygame.K_SPACE]:
            self.jump[0] = True
        if self.jump[0]:
            if self.jump[2] > -self.jump[1] * 1.01:
                self.y -= self.jump[2]
                self.jump[2] -= self.jump[1] / 10
            else:
                self.jump[0] = False
                self.jump[2] = self.jump[1]
        if self.y > sch:
            self.y = sch

    def draw(self):
        if self.side == 'right':
            if self.right[0] < 24:
                self.h = self.right[(1 if not full_screen else 9) + self.right[0] // 3].get_height()
                screen.blit(self.right[(1 if not full_screen else 9) + self.right[0] // 3], [self.x, self.y - self.h])
                self.right[0] += 1
            else:
                self.right[0] = 0
            self.left[0] = 0
        elif self.side == 'left':
            if self.left[0] < 24:
                self.h = self.left[(1 if not full_screen else 9) + self.left[0] // 3].get_height()
                screen.blit(self.left[(1 if not full_screen else 9) + self.left[0] // 3], [self.x, self.y - self.h])
                self.left[0] += 1
            else:
                self.left[0] = 0
            self.right[0] = 0

        else:  # center
            if self.last_side == 'left':
                screen.blit(self.left[17 if not full_screen else 18],
                            [self.x, self.y - self.right[17 if not full_screen else 18].get_height()])
            else:
                screen.blit(self.right[17 if not full_screen else 18],
                            [self.x, self.y - self.right[17 if not full_screen else 18].get_height()])
            self.right[0] = 0
            self.left[0] = 0

    def lvl_up(self):
        if self.exp['now'] >= self.exp['max']:
            self.lvl += 1
            self.hp['max'] = self.hp['max'] // 5
            self.hp['now'] = self.hp['max']
            self.exp['now'] = 0
            self.exp['max'] *= 2
            self.gun.damage[1] += 1
            self.gun.damage[3] += 1
            self.arm['max'] += self.arm['max'] // 10
            self.arm['now'] = self.arm['max']


class Weapon:
    def __init__(self, speed, radius, damage, ammunition, rarity, money, up_pay, get):
        self.bullets = []
        self.speed = speed
        self.radius = radius  # self.money[0: state, 1: dynamic, 2,3: out of waves]
        self.money = [money, 0.25, money * 1.5, 0.17]
        self.up_pay = [0.5, up_pay, 0.65, up_pay * 1.5]  # смотри "пояснения к коду"
        self.damage = [3, damage, 4, damage]
        self.ammunition = ammunition
        self.get = get
        self.rarity = [rarity, 0]  # self.rarity[0: state, 1: dynamic]
        self.delete = []
        self.cos = 0
        self.sin = 0

    def shoot(self, press, pos):
        if ((press[0] and pos[1] > p) or pressed[275] or pressed[276] or pressed[273]) and self.ammunition > 0:
            if self.rarity[1] == self.rarity[0]:
                self.rarity[1] = 0
                self.ammunition -= 1
                if press[0]:
                    rad2 = ((pos[0] - player.x) ** 2 + (pos[1] - player.y) ** 2) ** 0.5
                    self.cos = (pos[0] - player.x) / rad2 if pos[0] != player.x else 0
                    self.sin = (pos[1] - player.y + player.h / 2) / rad2 if pos[1] != player.y else 0
                    self.bullets.append([player.x + (player.w if self.cos > 0 else 0), player.y - player.h // 2,
                                         self.cos * self.speed, self.sin * self.speed])
                elif pressed[pygame.K_RIGHT]:
                    self.bullets.append([player.x + player.w, player.y - player.h // 2, self.speed, 0])
                elif pressed[pygame.K_LEFT]:
                    self.bullets.append([player.x, player.y - player.h // 2, -self.speed, 0])
                elif pressed[pygame.K_UP]:
                    self.bullets.append([player.x, player.y - player.h // 2, 0, -self.speed])
                player.last_side = 'right' if pos[0] > player.x + player.w / 2 or pressed[275] else 'left'
            else:
                self.rarity[1] += 1
        else:
            self.rarity[1] = self.rarity[0]

        for bullet in self.bullets:
            bullet[0] += bullet[2]
            bullet[1] += bullet[3]

    def draw(self):
        for bullet in self.bullets:
            if 0 <= bullet[0] <= scw or 0 <= bullet[1] <= sch:
                pygame.draw.circle(screen, red[1], [int(bullet[0]), int(bullet[1])], self.radius)
            else:
                self.delete.append(bullet)

    def deleted(self):
        try:
            for d in self.delete:
                self.bullets.pop(self.bullets.index(d))
        except ValueError:
            self.bullets.clear()
        self.delete.clear()


class Enemy:
    def __init__(self, x, y, rarity, xp, money, left, right, speed, damage, dmg_speed, exp):
        self.w = 26
        self.h = 44
        self.x = x
        self.y = y
        self.speed = [speed, 1]
        self.rarity = rarity
        self.rar = 18
        self.dmg_speed = [dmg_speed, dmg_speed]
        self.damage = damage
        self.exp = exp
        self.xp = xp
        self.money = money
        self.left = left
        self.right = right
        for image in self.left[1::]:
            image.set_colorkey(white)
        for image in self.right[1::]:
            image.set_colorkey(white)

    def moved(self):
        if player.x > self.x + self.w:
            self.speed[1] = 1
            self.x += self.speed[0] * self.speed[1]
        elif player.x + player.w < self.x:
            self.speed[1] = -1
            self.x += self.speed[0] * self.speed[1]
        if not player.jump[0]:
            if self.y > player.y:
                self.y -= self.speed[0] / 3
            elif self.y < player.y:
                self.y += self.speed[0] / 3

    def draw(self):
        if self.speed[1] == 1:
            if self.right[0] < 40:
                self.h = self.right[1 if not full_screen else 5 + self.right[0] // 10].get_height()
                screen.blit(self.right[1 if not full_screen else 5 + self.right[0] // 10], [self.x, self.y - self.h])
                self.right[0] += 1
            else:
                self.right[0] = 0
        else:
            if self.left[0] < 40:
                self.h = self.left[1 if not full_screen else 5 + self.left[0] // 10].get_height()
                screen.blit(self.left[1 if not full_screen else 5 + self.left[0] // 10], [self.x, self.y - self.h])
                self.left[0] += 1
            else:
                self.left[0] = 0

    def update(self):
        if abs(self.x - player.x - player.w / 2) <= (
                player.w / 2 + 5 if self.speed[1] < 0 else player.w / 2 + self.w) and \
                player.y >= self.y - self.h and (player.y <= self.y):
            if self.dmg_speed[1] > self.dmg_speed[0] // 2:
                if player.arm['now'] < player.hp['now']:
                    player.hp['now'] -= round(self.damage * (1 - player.arm['now'] / player.hp['max']))
                player.arm['now'] = (player.arm['now'] - self.damage) if player.arm['now'] - self.damage > 0 else 0
                self.dmg_speed[1] = 0
            else:
                self.dmg_speed[1] += 1
        for bullet in player.gun.bullets:
            x, y, z, tmp8 = bullet
            if self.x <= x <= self.x + self.w and self.y - self.h <= y <= self.y:
                self.xp -= player.gun.damage[1]
                self.x += dropping * f * (1 if z > 0 else -1)
                player.gun.delete.append(bullet)
                return

    def dead(self):
        if self.rar == 18:
            player.exp['now'] += self.exp
            player.wave_money['now'] += round(self.money)
            player.wave_money['max'] += round(self.money)
            player.kills += 1
            player.lvl_up()
        if self.rar > 0:
            screen.blit(font(15 * f, '+' + str(round(self.money)), red[1]), [self.x, self.y - (95 - self.rar) * f])
            self.rar -= 1
            return True
        else:
            return False


pistol = Weapon(6, 3, 5, 60, 3, 50, 300, 15)
guns = [pistol]
player = Player()


def up_board():
    global screen_visible

    if screen_visible == 'start screen':
        if 170 * f < mouse_pos[0] < 275 * f and 200 * f < mouse_pos[1] < 240 * f:
            pygame.draw.rect(screen, red[1 if not mouse_pressed[0] else 0], [170 * f, 200 * f, 115 * f, 40 * f])
        screen.blit(font(35 * f, 'Играть'), [174 * f, 200 * f])

        if 345 * f < mouse_pos[0] < 520 * f and 200 * f < mouse_pos[1] < 240 * f:
            pygame.draw.rect(screen, red[1 if not mouse_pressed[0] else 0], [345 * f, 200 * f, 193 * f, 40 * f])
        screen.blit(font(35 * f, 'Управление'), [348 * f, 200 * f])

    if screen_visible == 'setting':
        screen.blit(font(25 * f, 'WASD - движение'), [30 * f, 25 * f])
        screen.blit(font(25 * f, 'TAB - магазин'), [40 * f, 70 * f])
        screen.blit(font(25 * f, 'ESC - назад'), [18 * f, 94 * f])
        screen.blit(font(25 * f, 'ЛКМ - огонь'), [30 * f, 125 * f])

    if screen_visible == 'main screen' or screen_visible == 'battle':
        pygame.draw.rect(screen, black, [0, 0, 640 * f, 20 * f])
        screen.blit(font(15 * f, f'уровень: {player.lvl}'), [0, 0])
        pygame.draw.rect(screen, white, [90, 1, 50, 18 * f])
        pygame.draw.rect(screen, green, [90, 1, 50 * player.exp['now'] / player.exp['max'], 18 * f])
        screen.blit(font(15 * f, 'опыт', black), [90, 5])
        screen.blit(hp[abs(1 - f)], [160 * f, 0])
        screen.blit(font(15 * f, 'патроны: ' + str(player.gun.ammunition)), [290 * f, 0])
        screen.blit(font(15 * f, 'броня: ' + str(round(player.arm['now']))), [390 * f, 0])

    if screen_visible == 'main screen':
        screen.blit(font(15 * f, str(round(player.hp['max']))), [180 * f, 0])
        screen.blit(font(15 * f, str(int(player.money)) + '$'), [220 * f, 0])
        screen.blit(font(15 * f, 'урон: ' + str(int(player.gun.damage[3]))), [480 * f, 0])

    if screen_visible == 'battle':
        screen.blit(font(15 * f, str(int(player.hp['now']))), [180 * f, 0])
        screen.blit(font(15 * f, str(player.wave_money['now']) + '$'), [220 * f, 0])

    if mouse_pos[0] < scw - p or mouse_pos[1] > p:  # exit button
        pygame.draw.rect(screen, red[3], [scw - p, 0, p, p])
        pygame.draw.line(screen, black, [scw - p + 5, 5], [scw - 5, p - 5], 2)
        pygame.draw.line(screen, black, [scw - p + 5, p - 5], [scw - 5, 5], 2)
    else:
        pygame.draw.rect(screen, red[1], [scw - p, 0, p, p])
        if mouse_pressed[0]:
            pygame.draw.rect(screen, red[0], [scw - p, 0, p, p])
        pygame.draw.line(screen, white, [scw - p + 5, 5], [scw - 5, p - 5], 2)
        pygame.draw.line(screen, white, [scw - p + 5, p - 5], [scw - 5, 5], 2)

    if scw - 2 * p < mouse_pos[0] < scw - p and mouse_pos[1] < p:  # full_screen button
        pygame.draw.rect(screen, gray[200], [scw - 2 * p, 0, p, p])
        if mouse_pressed[0]:
            pygame.draw.rect(screen, gray[100], [scw - 2 * p, 0, p, p])
    else:
        pygame.draw.rect(screen, white, [scw - 2 * p, 0, p, p])

    if not full_screen:
        pygame.draw.rect(screen, black, [scw - 35, 5, p / 2, p / 2], 3)
    else:
        pygame.draw.rect(screen, gray[50], [scw - 53, 7, p / 2, p / 2], 4)

    screen.blit(save[0 if not full_screen else 1], [scw - 3 * p - 2, 0])


def change_screen(f_sc):
    global scw, sch, dropping, screen
    pygame.display.quit()
    pygame.display.init()
    scw = 1280 if not f_sc else 640
    sch = 640 if not f_sc else 320
    player.w = 50 if not f_sc else 25
    player.h = 84 if not f_sc else 43
    player.speed = 8 if not f_sc else 4
    player.x = player.x * 2 if not f_sc else player.x // 2
    player.y = player.y * 2 if not f_sc else player.y // 2
    player.jump[1] = player.jump[1] * 2 if not f_sc else player.jump[1] // 2
    player.jump[2] = player.jump[2] * 2 if not f_sc else player.jump[2] // 2
    dropping = dropping * 2 if not f_sc else dropping // 2
    for weapon1 in guns:
        weapon1.speed = 12 if not f_sc else 6
        weapon1.radius = 6 if not f_sc else 3
    for bul1 in player.gun.bullets:
        bul1[0] = bul1[0] * 2 if not f_sc else bul1[0] // 2
        bul1[1] = bul1[1] * 2 if not f_sc else bul1[1] // 2
    for i1 in range(len(wave_enemy) - 1):
        for en1 in wave_enemy[i1]:
            en1.x = en1.x * 2 if not f_sc else en1.x / 2
            en1.y = en1.y * 2 if not f_sc else en1.y / 2
            en1.speed[i1] = en1.speed[i1] * 2 if not f_sc else en1.speed[i1] / 2
    for i1 in range(len(en_spd) - 1):
        en_spd[i1] = en_spd[i1] * 2 if not f_sc else en_spd[i1] / 2
    screen = pygame.display.set_mode((scw, sch))
    pygame.display.set_caption('some shooter')
    pygame.display.set_icon(icon)


time_out = True
wave_tick = 0
wave_number = 1

com1_l = [0, load('com1_l1', 1), load('com1_l2', 1), load('com1_l3', 1), load('com1_l4', 1), load('full_com1_l1', 1),
          load('full_com1_l2', 1), load('full_com1_l3', 1), load('full_com1_l4', 1)]
com1_r = [0, load('com1_r1', 1), load('com1_r2', 1), load('com1_r3', 1), load('com1_r4', 1), load('full_com1_r1', 1),
          load('full_com1_r2', 1), load('full_com1_r3', 1), load('full_com1_r4', 1)]

com2_l = [0, load('com2_l1', 1), load('com2_l2', 1), load('com2_l3', 1), load('com2_l4', 1), load('full_com2_l1', 1),
          load('full_com2_l2', 1), load('full_com2_l3', 1), load('full_com2_l4', 1)]
com2_r = [0, load('com2_r1', 1), load('com2_r2', 1), load('com2_r3', 1), load('com2_r4', 1), load('full_com2_r1', 1),
          load('full_com2_r2', 1), load('full_com2_r3', 1), load('full_com2_r4', 1)]

rar1_l = [0, load('rar1_l1', 1), load('rar1_l2', 1), load('rar1_l3', 1), load('rar1_l4', 1), load('full_rar1_l1', 1),
          load('full_rar1_l2', 1), load('full_rar1_l3', 1), load('full_rar1_l4', 1)]
rar1_r = [0, load('rar1_r1', 1), load('rar1_r2', 1), load('rar1_r3', 1), load('rar1_r4', 1), load('full_rar1_r1', 1),
          load('full_rar1_r2', 1), load('full_rar1_r3', 1), load('full_rar1_r4', 1)]

rar2_l = [0, load('rar2_l1', 1), load('rar2_l2', 1), load('rar2_l3', 1), load('rar2_l4', 1), load('full_rar2_l1', 1),
          load('full_rar2_l2', 1), load('full_rar2_l3', 1), load('full_rar2_l4', 1)]
rar2_r = [0, load('rar2_r1', 1), load('rar2_r2', 1), load('rar2_r3', 1), load('rar2_r4', 1), load('full_rar2_r1', 1),
          load('full_rar2_r2', 1), load('full_rar2_r3', 1), load('full_rar2_r4', 1)]

bos1_l = [0, load('bos1_l1', 1), load('bos1_l2', 1), load('bos1_l3', 1), load('bos1_l4', 1), load('full_bos1_l1', 1),
          load('full_bos1_l2', 1), load('full_bos1_l3', 1), load('full_bos1_l4', 1)]
bos1_r = [0, load('bos1_r1', 1), load('bos1_r2', 1), load('bos1_r3', 1), load('bos1_r4', 1), load('full_bos1_r1', 1),
          load('full_bos1_r2', 1), load('full_bos1_r3', 1), load('full_bos1_r4', 1)]

bos2_l = [0, load('bos2_l1', 1), load('bos2_l2', 1), load('bos2_l3', 1), load('bos2_l4', 1), load('full_bos2_l1', 1),
          load('full_bos2_l2', 1), load('full_bos2_l3', 1), load('full_bos2_l4', 1)]
bos2_r = [0, load('bos2_r1', 1), load('bos2_r2', 1), load('bos2_r3', 1), load('bos2_r4', 1), load('full_bos2_r1', 1),
          load('full_bos2_r2', 1), load('full_bos2_r3', 1), load('full_bos2_r4', 1)]

enemies = [10, 0, 0, 0, 0, 0]
en_add = [4, 4, 2, 2]
en_hp = [18, 12, 32, 25, 2500, 2200]
en_mny = [12, 15, 25, 30, 450, 600]
en_dmg = [5, 7, 15, 17, 95, 60]
en_spd = [2.5, 4, 2.2, 2.4, 2.1, 2.9]
tick = [19, 22, 140, 170]
en_exp = [5, 8, 14, 18, 250, 350]
up_xp = [0.15, 0.15, 0.2, 0.2, 0.65, 0.55]  # every wave
up_money = [0.1, 0.1, 0.15, 0.15, 0.65, 0.65]  # every wave
enemy_last = [10, 0, 0, 0, 0, 0]
dropping = 3

try:
    data = open('wave data.txt')
    tmr = data.read()
    data.close()
    try:
        player.x, player.y, player.wave_money, player.gun.ammunition, wave_number, enemies, enemy_last, en_hp, en_mny, \
            en_dmg, tick, player.kills = data_loading(tmr)
    except ValueError:
        saves([player.x, player.y, player.wave_money, player.gun.ammunition, wave_number, enemies, enemy_last, en_hp,
               en_mny, en_dmg, tick, player.kills])
except FileNotFoundError:
    saves([player.x, player.y, player.wave_money, player.gun.ammunition, wave_number, enemies, enemy_last, en_hp,
           en_mny, en_dmg, tick, player.kills])

try:
    data = open('data.txt')
    tmr = data.read()
    data.close()
    if tmr != '':
        player.hp, player.money, player.gun.money, player.gun.damage, player.gun.up_pay, player.exp, player.lvl, \
            player.arm, player.arm_fill, full_screen = data_loading(tmr)
    else:
        saves([player.hp, player.money, player.gun.money, player.gun.damage, player.gun.up_pay,
               player.exp, player.lvl, player.arm, player.arm_fill, full_screen], 'data.txt')
except FileNotFoundError:
    saves([player.hp, player.money, player.gun.money, player.gun.damage, player.gun.up_pay,
           player.exp, player.lvl, player.arm, player.arm_fill, full_screen], 'data.txt')

wave_enemy = add(enemy_last, tick, [[], [], [], [], [], []])
enemy_number = sum(len(wave_enemy[i1]) for i1 in range(6))


def new_wave():
    global wave_enemy, en_hp, en_mny, enemy_number
    enemies[0] += en_add[0]
    enemies[1] += en_add[1]
    for i1 in range(len(up_xp) - 2):
        en_hp[i1] = en_hp[i1] * (1 + up_xp[i1])
        en_mny[i1] = en_mny[i1] * (1 + up_money[i1])
    if wave_number % 5 == 0:
        if tick[0] > 13:
            for i1 in range(len(tick) - 2):
                tick[i1] -= 1 + 5 * (i1 // 2)
    if wave_number % 5 == 1 and wave_number != 1:
        en_mny[4] = en_mny[4] * (1 + up_money[4])
        en_hp[4] = en_hp[4] * (1 + up_xp[4])
    if wave_number % 5 == 0:
        enemies[4] = 1
    else:
        enemies[4] = 0
    if wave_number % 7 == 1 and wave_number != 1:
        en_mny[5] = en_mny[5] * (1 + up_money[5])
        en_hp[5] = en_hp[5] * (1 + up_xp[5])
    if wave_number % 7 == 0:
        enemies[5] = 1
    else:
        enemies[5] = 0
    if wave_number == 2:
        enemies[1] += en_add[2]
    if wave_number > 3:
        enemies[2] += en_add[3]
        if wave_number > 4:
            enemies[3] += 2
    for i in range(len(en_add)):
        en_add[i] += enemies[i] // 20
    print(en_add)


def waves():
    global wave_tick, time_out, wave_number, wave_enemy, enemy_number
    delete = []
    if not time_out:
        if enemy_number > 0:
            for i1 in range(len(wave_enemy)):
                if i1 < 4:
                    for enemy in wave_enemy[i1]:
                        if enemy.rarity <= 0:
                            if enemy.xp > 0:
                                enemy.draw()
                                enemy.update()
                                player.gun.deleted()
                                enemy.moved()
                            elif not enemy.dead():
                                delete.append(wave_enemy[i1].index(enemy))
                                enemy_number -= 1
                        else:
                            enemy.rarity -= 1
                            enemy.y = player.y if not player.jump[0] else 300 * f
                elif enemy_number < 4:
                    for enemy in wave_enemy[i1]:
                        screen.blit(font(15 * f, round(enemy.xp), (red[1] if i1 == 4 else yellow)),
                                    [50 + (scw - 200) * (i1 - 4), 15 * f])
                        enemy.update()
                        player.gun.deleted()
                        enemy.moved()
                        enemy.draw()
                        if enemy.xp <= 0:
                            delete.append(wave_enemy[i1].index(enemy))
                            player.wave_money['now'] += enemy.money
                            player.wave_money['max'] += enemy.money
                for d in delete:
                    try:
                        wave_enemy[i1].pop(d)
                    except IndexError:
                        continue
                delete.clear()
        else:
            wave_number += 1
            time_out = True
            new_wave()
            wave_enemy = add(enemies, tick, wave_enemy)
            enemy_number = sum(len(wave_enemy[i1]) for i1 in range(6))

    else:
        if wave_tick >= 60:
            time_out = False
            wave_tick = 0
        else:
            wave_tick += 1
            screen.blit(font(25 * f, 'волна: ' + str(wave_number), gray[200]), [160 * f, 160 * f])
            screen.blit(font(25 * f, 'враги: ' + str(enemy_number), gray[200]), [390 * f, 160 * f])


if full_screen:
    change_screen(not full_screen)
clock = pygame.time.Clock()
from_start = False
sav = True
pause = False
shopping = False
done = False
while not done:
    pressed = pygame.key.get_pressed()
    mouse_pressed = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    f = 1 if not full_screen else 2
    p = 20 if not full_screen else 30

    if screen_visible == 'start screen':
        screen.blit(start_screen[abs(1 - f)], [0, 0])

    elif screen_visible == 'setting':
        screen.blit(setting_bg[abs(1 - f)], [0, 0])

    elif screen_visible == 'main screen':
        screen.blit(battle_bg[abs(1 - f)], [0, 0])
        if not shopping:
            player.move(pressed)
            player.draw()
        else:
            screen.blit(font(17 * f, f'a - купить {player.gun.get} патронов за {int(player.gun.money[2])}$'),
                        [40 * f, sch / 2 - 20 * f])
            screen.blit(font(17 * f, 'улучшения:'), [40 * f, sch / 2 + 20 * f])
            screen.blit(font(17 * f, 'u - урон оружия на ' + str(player.gun.damage[3] // 10 + player.gun.damage[2]) +
                             ' за ' + str(player.gun.up_pay[3]) + '$'), [40 * f, sch / 2 + (40 * f)])
            screen.blit(font(17 * f, f'g - вместимость брони до {int(player.arm["max"] * player.arm["priceUpToOne"])}' +
                        ' за ' + str(player.arm['buyUp']) + '$'), [40 * f, sch / 2 + (60 * f)])
            screen.blit(
                font(17 * f, 't - востановление брони с ' + str(((30 * player.arm_fill[0] * 1000) // 10) / 100) +
                     '/sec до ' + str(((30 * (player.arm_fill[0] + player.arm_fill[1]) * 1000) // 10) / 100) +
                     '/sec за ' + str(player.arm_fill[3]) + '$'), [40 * f, sch / 2 + (80 * f)])

    elif screen_visible == 'battle':
        screen.blit(battle_bg[abs(1 - f)], [0, 0])
        if not pause:
            if player.arm['now'] < player.arm['max']:
                player.arm['now'] += player.arm_fill[0]
            if player.arm['now'] > player.arm['max']:
                player.arm['now'] = player.arm['max']
            player.move(pressed)
            player.gun.shoot(mouse_pressed, mouse_pos)
            waves()
            player.gun.deleted()
            player.draw()
            player.gun.draw()

        else:
            t = font(30 * f, 'Пауза')
            screen.blit(t, [scw / 2 - t.get_width() / 2, sch / 2 - t.get_height() / 2])
            screen.blit(font(20 * f, f'a - купить {player.gun.get} патронов  за {player.gun.money[0]}$'),
                        [scw / 2 - (140 * f), sch / 2 + 30 * f])
            screen.blit(
                font(20 * f, 'u - повысить урон оружия  на ' + str(player.gun.damage[1] // 10 + player.gun.damage[0]) +
                     ' за ' + str(player.gun.up_pay[1]) + '$'), [scw / 2 - (140 * f), sch / 2 + (50 * f)])
            screen.blit(font(20 * f, 'урон: ' + str(player.gun.damage[1])), [scw / 2 - (140 * f), sch / 2 + (70 * f)])

    elif screen_visible == 'dead':
        screen.blit(font(50 * f, 'Вы мертвы', red[0]), [scw / 2 - 100 * f, sch / 2])
        pygame.display.update()
        pygame.time.delay(1500)
        screen_visible = 'main screen'
        print(player.wave_money['max'], player.kills)
        player.money += player.wave_money['max'] // 20 + player.kills // 2
        data = open('save for death.txt')
        player.wave_money, player.gun.ammunition, tmp, enemies, enemy_last, en_hp, en_mny, en_dmg, en_add, tick, \
            player.kills = data_loading(data.read())
        data.close()
        data = open('data.txt')
        tmp3, tmp1, player.gun.money, tmp6, player.gun.up_pay, tmp4, tmp5, player.arm, \
            player.arm_fill, tmp2 = data_loading(data.read())
        player.arm['now'] = player.arm['max']
        player.gun.damage[1] = player.gun.damage[3]
        player.hp['now'] = player.hp['max']
        wave_number = 1
        data.close()
        wave_enemy = add(enemy_last, tick, [[], [], [], [], [], []])
        enemy_number = sum(len(wave_enemy[i1]) for i1 in range(6))
        time_out = True
        wave_tick = 0
        player.gun.bullets.clear()
        player.x = 320 * f
        player.y = 300 * f

    up_board()

    if player.hp['now'] <= 0:
        screen_visible = 'dead'
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if scw - 3 * p < mouse_pos[0] < scw - 2 * p and mouse_pos[1] < p:
                data = open('wave data.txt', 'w')
                data.write('')
                data.close()
                data = open('data.txt', 'w')
                data.write('')
                data.close()
                data = open('save for death.txt', 'w')
                data.write('')
                data.close()
                sav = False

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if 170 * f < mouse_pos[0] < 275 * f and 200 * f < mouse_pos[1] < 240 * f and \
                    screen_visible == 'start screen':
                screen_visible = 'main screen'
            if mouse_pos[0] > scw - p and mouse_pos[1] < p:
                done = True
            if 345 * f < mouse_pos[0] < 520 * f and 200 * f < mouse_pos[1] < 240 * f:
                if screen_visible == 'start screen':
                    screen_visible = 'setting'
            if scw - p * 2 <= mouse_pos[0] <= scw - p and mouse_pos[1] <= p:
                change_screen(full_screen)
                full_screen = not full_screen

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if screen_visible == 'start screen':
                    done = True
                elif screen_visible == 'main screen' or screen_visible == 'setting':
                    screen_visible = 'start screen'
                elif screen_visible == 'battle':
                    screen_visible = 'main screen'

            if screen_visible == 'start screen':
                if event.key == pygame.K_RETURN:
                    screen_visible = 'main screen'
                    from_start = True
                if event.key == pygame.K_TAB:
                    change_screen(full_screen)
                    full_screen = not full_screen

            if screen_visible == 'main screen':
                if event.key == pygame.K_RETURN and not from_start:
                    screen_visible = 'battle'
                    try:
                        data = open('save for death.txt')
                        read = data_loading(data.read())
                        if len(read) == 0:
                            saves([player.wave_money, player.gun.ammunition, wave_number, enemies, enemy_last, en_hp,
                                   en_mny, en_dmg, en_add, tick, player.kills], 'save for death.txt')
                        elif wave_number == 1:
                            saves([player.wave_money, player.gun.ammunition, wave_number, enemies, enemy_last,
                                   en_hp, en_mny, en_dmg, en_add, tick, player.kills], 'save for death.txt')
                    except FileNotFoundError:
                        saves([player.wave_money, player.gun.ammunition, wave_number, enemies, enemy_last,
                               en_hp, en_mny, en_dmg, en_add, tick, player.kills], 'save for death.txt')
                    saves([player.hp, player.money, player.gun.money, player.gun.damage, player.gun.up_pay, player.exp,
                           player.lvl, player.arm, player.arm_fill, full_screen], 'data.txt')
                else:
                    from_start = False
                if event.key == pygame.K_TAB:
                    shopping = not shopping
                if shopping:
                    if event.key == pygame.K_a and player.money >= player.gun.money[2]:
                        player.money -= player.gun.money[2]
                        player.gun.money[2] = player.gun.money[2] * (1 + player.gun.money[1])
                        player.gun.ammunition += player.gun.get

                    if event.key == pygame.K_u and player.money >= player.gun.up_pay[3]:
                        player.money -= player.gun.up_pay[3]
                        player.gun.damage[3] += player.gun.damage[2] + player.gun.damage[3] // 10
                        player.gun.up_pay[3] = player.gun.up_pay[3] * (1 + player.gun.up_pay[2])
                        player.gun.money[2] = player.gun.up_pay[3] * player.gun.money[3]  # menu

                        player.gun.damage[1] = player.gun.damage[3]
                        player.gun.up_pay[1] = player.gun.up_pay[1] * (1 + player.gun.up_pay[0])
                        player.gun.money[0] = player.gun.up_pay[1] * player.gun.money[3]  # battle

                        player.gun.ammunition = 60

                    if event.key == pygame.K_g and player.money >= player.arm['buyUp']:
                        player.money -= player.arm['buyUp']
                        player.arm['max'] = player.arm['max'] * player.arm['priceUpToOne']
                        player.arm['buyUp'] = player.arm['buyUp'] * player.arm['priceUpToUp']
                        player.arm['now'] = player.arm['max']

                    if event.key == pygame.K_t and player.money >= player.arm_fill[3]:
                        player.money -= player.arm_fill[3]
                        player.arm_fill[3] = round(player.arm_fill[3] * (1 + player.arm_fill[4]))
                        player.arm_fill[0] += player.arm_fill[1]
                        player.arm_fill[2] += 1
                        if player.arm_fill[2] == 3:
                            player.arm_fill[2] = 0
                            if player.arm_fill[1] < 1 / 15:
                                player.arm_fill[1] *= 2
                            elif player.arm_fill[1] == 1 / 15:
                                player.arm_fill[1] *= 3
                            elif player.arm_fill[1] == 1 / 5:
                                player.arm_fill[1] *= 5
                            elif player.arm_fill[1] >= 1:
                                player.arm_fill[1] *= 3

            if screen_visible == 'battle':
                if event.key == pygame.K_TAB:
                    pause = not pause
                    pygame.time.delay(100)
                if pause:
                    if event.key == pygame.K_a and player.wave_money['now'] >= player.gun.money[0]:
                        player.wave_money['now'] -= player.gun.money[0]
                        player.gun.ammunition += player.gun.get

                    if event.key == pygame.K_u and player.wave_money['now'] >= player.gun.up_pay[1]:
                        player.wave_money['now'] -= player.gun.up_pay[1]
                        player.gun.damage[1] += player.gun.damage[0] + player.gun.damage[1] // 10
                        player.gun.up_pay[1] = player.gun.up_pay[1] * (1 + player.gun.up_pay[0])
                        player.gun.money[0] = player.gun.up_pay[1] * player.gun.money[3]

                    if event.key == pygame.K_RETURN:
                        player.wave_money['now'] += wave_number * 25
                        wave_number += 1
                        time_out = True
                        new_wave()
                        wave_enemy = add(enemies, tick, wave_enemy)
                        enemy_number = sum(len(wave_enemy[i1]) for i1 in range(6))

    pygame.display.update()
    clock.tick(30)
else:
    if sav:
        enemy_last = [len(wave_enemy[i]) for i in range(len(wave_enemy))]
        print(enemy_last)
        saves([player.x if not full_screen else player.x // 2, player.y if not full_screen else player.y // 2,
               player.wave_money, player.gun.ammunition, wave_number, enemies, enemy_last, en_hp, en_mny, en_dmg, tick,
               player.kills])
        saves([player.hp, player.money, player.gun.money, player.gun.damage, player.gun.up_pay,
               player.exp, player.lvl, player.arm, player.arm_fill, full_screen], 'data.txt')

pygame.quit()
