import pygame
pygame.init()


def font(size: int, text, colour=(255, 255, 255)):
    return pygame.font.SysFont('verdana', size).render(str(text), True, colour)


def main_screen():
    screen.blit(pre_show_text1, (width / 2 - pre_show_text1.get_width() / 2, height - 175))
    screen.blit(pre_show_text2, (width / 2 - pre_show_text2.get_width() / 2, height - 35))
    screen.blit(pre_show_text3, (width / 2 - pre_show_text3.get_width() / 2, height / 8))
    pygame.draw.rect(screen, color[2 if game_mode[0] else 1], [width / 8, height / 4, 70, 70])
    pygame.draw.rect(screen, color[2 if game_mode[1] else 1], [width / 8 + width / 3, height / 4, 70, 70])
    pygame.draw.rect(screen, color[2 if game_mode[2] else 1], [width / 8 + 2 * width / 3, height / 4, 70, 70])
    screen.blit(number_text1, (width / 8 + 25, height / 4))
    screen.blit(number_text2, (width / 8 + width / 3 + 20, height / 4))
    screen.blit(number_text3, (width / 8 + 2 * width / 3 + 20, height / 4))
    screen.blit(for_number_text1, (width / 8, height - 280))
    screen.blit(for_number_text2, (width / 8, height - 245))
    screen.blit(for_number_text3, (width / 8, height - 210))
    screen.blit(pre_show_text4, (width / 2 - pre_show_text4.get_width() / 2, height - 65))
    screen.blit(pre_show_text5, (width / 2 - pre_show_text5.get_width() / 2, height - 140))
    screen.blit(pre_show_text6, (width / 2 - pre_show_text6.get_width() / 2, height - 105))


def choice_difficulty():
    pygame.draw.rect(screen, color[2 if bot_mode[0] else 1], [width / 8, height / 4, 70, 70])
    pygame.draw.rect(screen, color[2 if bot_mode[1] else 1], [width / 8 + width / 3, height / 4, 70, 70])
    pygame.draw.rect(screen, color[2 if bot_mode[2] else 1], [width / 8 + 2 * width / 3, height / 4, 70, 70])
    screen.blit(number_text1, (width / 8 + 25, height / 4))
    screen.blit(number_text2, (width / 8 + width / 3 + 20, height / 4))
    screen.blit(number_text3, (width / 8 + 2 * width / 3 + 20, height / 4))
    screen.blit(bot_text, (width / 2 - bot_text.get_width() / 2, height / 8))
    screen.blit(bot_text1, (width / 8, height / 2))
    screen.blit(bot_text2, (width / 8, height / 2 + 35))
    screen.blit(bot_text3, (width / 8, height / 2 + 70))


white = (255, 255, 255)
black = (0, 0, 10)
gray = (150, 150, 150)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
color = [blue, green, red, gray]

width, height = 480, 480
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))

platform_width, platform_height = 75, 10
x_player1 = x_player2 = x_bot = width/2 - platform_width/2
score = [0, 0]

radius = 10
boll_speed = 6
x_change = boll_speed
y_change = -boll_speed
x_boll = int(width/2)+17
y_boll = height - platform_height - radius

score_text = font(15, 'Счет:' + str(score[0]), gray)
pygame.display.set_caption('пин-понг')
pre_show_text1 = font(25, 'управление:', gray)
pre_show_text2 = font(25, 'чтобы начать игру нажмите пробел', gray)
pre_show_text3 = font(25, 'Выберите режим игры', gray)
pre_show_text4 = font(17, '"ESC" - выйти/вернуться к главному экрану', gray)
pre_show_text5 = font(25, 'первый игрок: "A","D"', gray)
pre_show_text6 = font(25, 'второй игрок: стрелки', gray)
text_for_game_over2 = font(25, 'нажмите пробел чтобы начать игру', gray)
text_win = font(25, 'Вы победили!!!', gray)
text_loose = font(25, 'Вы проиграли.', gray)
text_replay = font(25, 'Чтобы начать новую игру нажмите "R"', gray)
number_text1 = font(50, '1', white)
number_text2 = font(50, '2', white)
number_text3 = font(50, '3', white)
for_number_text1 = font(20, '1 - 1 игрок', gray)
for_number_text2 = font(20, '2 - 2 игрока', gray)
for_number_text3 = font(20, '3 - чеканка', gray)
bot_text = font(25, 'Выберите сложность бота', gray)
bot_text1 = font(20, '1 - лёгкий', gray)
bot_text2 = font(20, '2 - средний', gray)
bot_text3 = font(20, '3 - непобедимый', gray)
player1_win = font(25, 'Первый грок победил', gray)
player2_win = font(25, 'Второй игрок победил', gray)

bot_level = 3
bot_mode = [True, False, False]

done = False
choice_done = False
kick = [False, False]
game_type = 0
game_mode = [True, False, False]
while not done:
    pressed = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_type == 0:
                    done = True
                else:
                    choice_done = False
                    x_boll = int(width/2)+17
                    y_boll = height-platform_height-radius
                    x_player1 = width/2-platform_width/2
                    score = [0, 0]
                    x_change = 6
                    y_change = -6
                    game_type = 0
            if event.key == pygame.K_SPACE:
                if game_type == 1 and game_mode[0]:
                    choice_done = True

            if game_type == 0:
                if event.key == pygame.K_d and game_mode[2] != 1:
                    game_mode.insert(0, False)
                    game_mode.pop()
                elif event.key == pygame.K_a and game_mode[0] != 1:
                    game_mode.append(False)
                    game_mode.pop(0)

            if game_type == 1 and game_mode[0] and not choice_done:
                if event.key == pygame.K_d and bot_mode[2] != 1:
                    bot_mode.insert(0, False)
                    bot_mode.pop()
                elif event.key == pygame.K_a and bot_mode[0] != 1:
                    bot_mode.append(False)
                    bot_mode.pop(0)
            elif event.key == pygame.K_r:
                x_boll = int(width / 2)+17
                y_boll = height - platform_height - radius
                x_player1 = width / 2 - platform_width / 2
                score = [0, 0]
                x_change = 6
                y_change = -6
                game_type = 1

    screen.fill(black)
    if game_type == 0:
        main_screen()
        if pressed[pygame.K_SPACE]:
            game_type = 1

    if game_type == 1:
        if game_mode[0]:
            if not choice_done:
                choice_difficulty()
                if bot_mode[0]:
                    bot_level = 3
                elif bot_mode[1]:
                    bot_level = 5
                elif bot_mode[2]:
                    bot_level = 6
            else:
                if x_bot+platform_width/2-bot_level > x_boll and x_bot >= 0:
                    x_bot -= bot_level
                elif x_bot+platform_width/2+bot_level < x_boll and x_bot <= width:
                    x_bot += bot_level

                if y_boll + radius >= height - 10:
                    if (x_boll >= x_player1) and x_boll <= x_player1+75:
                        if not kick[0]:
                            y_change = -boll_speed
                            kick = [True, False]
                        for i in range(-6, 7):
                            if x_boll <= x_player1+45+5*i:
                                x_change = i
                                break
                    else:
                        score[1] += 1
                        game_type = 3
                if y_boll - radius <= 10:
                    if (x_boll >= x_bot) and x_boll <= x_bot+75:
                        if not kick[1]:
                            y_change = boll_speed
                            kick = [False, True]
                        for i in range(-6, 7):
                            if x_boll <= x_bot+45+5*i:
                                x_change = i
                                break
                    else:
                        score[0] += 1
                        game_type = 3

                if score[0] >= 11 or score[1] >= 11:
                    game_type = 2

                if x_boll >= width or x_boll <= 0:
                    x_change = -x_change
                x_boll += x_change
                y_boll += y_change

                pygame.draw.rect(screen, blue, [x_bot, 0, platform_width, platform_height])
                pygame.draw.circle(screen, red, [x_boll, y_boll], radius)
                pygame.draw.rect(screen, green, [x_player1, height - platform_height, platform_width, platform_height])

        if game_mode[1]:
            if y_boll + radius >= height - 10:
                if (x_boll >= x_player1) and x_boll <= x_player1+75:
                    if not kick[0]:
                        y_change = -boll_speed
                        kick = [True, False]
                    for i in range(-6, 7):
                        if x_boll <= x_player1+45+5*i:
                            x_change = i
                            break
                else:
                    score[1] += 1
                    game_type = 3

            if y_boll - radius <= 10:
                if (x_boll >= x_player2) and x_boll <= x_player2+75:
                    if not kick[1]:
                        y_change = boll_speed
                        kick = [False, True]
                    for i in range(-6, 7):
                        if x_boll <= x_player2+45+5*i:
                            x_change = i
                            break
                else:
                    score[0] += 1
                    game_type = 3

            if score[0] >= 11 or score[1] >= 11:
                game_type = 2

            if x_boll >= width or x_boll <= 0:
                x_change = -x_change
            x_boll += x_change
            y_boll += y_change

            pygame.draw.rect(screen, red, [x_player2, 0, platform_width, platform_height])
            pygame.draw.circle(screen, red, [x_boll, y_boll], radius)
            pygame.draw.rect(screen, green, [x_player1, height - platform_height, platform_width, platform_height])

        if game_mode[2]:

            if y_boll + radius >= height - 10 or y_boll - radius <= 10:
                if (x_boll >= x_player1) and x_boll <= x_player1+75:
                    if not kick:
                        y_change = -boll_speed if y_boll + radius >= height - 10 else boll_speed
                        kick = True
                    for i in range(-6, 7):
                        if x_boll <= x_player1+45+5*i:
                            x_change = i
                            score[0] += 1
                            break
                else:
                    game_type = 2
            else:
                kick = False

            if x_boll >= width or x_boll <= 0:
                x_change = -x_change
            x_boll += x_change
            y_boll += y_change

            pygame.draw.rect(screen, green, [x_player1, 0, platform_width, platform_height])
            pygame.draw.rect(screen, green, [x_player1, height - platform_height, platform_width, platform_height])
            pygame.draw.circle(screen, red, [x_boll, y_boll], radius)

        score_text = font(15, 'Счет'+str(score[0])+(':'+str(score[1]) if not game_mode[2] else ''), gray)
        screen.blit(score_text, (0, 0))

        if pressed[pygame.K_a] and x_player1 >= 0:
            x_player1 -= 6
        elif pressed[pygame.K_d] and x_player1+75 <= width:
            x_player1 += 6

        if pressed[pygame.K_LEFT] and x_player2 >= 0:
            x_player2 -= 6
        elif pressed[pygame.K_RIGHT] and x_player2+75 <= width:
            x_player2 += 6

    if game_type == 2:
        if game_mode[2]:
            screen.blit(text_replay, (width/2-text_replay.get_width()/2, height/2))
        if game_mode[0]:
            if score[0] > score[1]:
                screen.blit(text_win, (width/2-text_win.get_width()/2, height/2))
            else:
                screen.blit(text_loose, (width/2-text_loose.get_width()/2, height/2))
                screen.blit(text_replay, (width/2-text_replay.get_width()/2, height/2-height/4))
        if game_mode[1]:
            if score[0] > score[1]:
                screen.blit(player1_win, (width/2-player1_win.get_width()/2, height/2))
            else:
                screen.blit(player2_win, (width/2-player2_win.get_width()/2, height/2))
        screen.blit(score_text, (width/2-score_text.get_width()/2, height/2-25))

    if game_type == 3:
        if sum(score) % 4 > 1:
            y_boll = platform_height + radius
            y_change = 6
        else:
            y_boll = height - platform_height - radius
            y_change = -6
        x_boll = int(width/2)+17
        x_player1 = x_player2 = x_bot = width/2-platform_width/2
        game_type = 1
        clock.tick(5)

    pygame.display.update()
    clock.tick(60)
pygame.quit()
