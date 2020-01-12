from PIL import Image
import pygame
import os
import tkinter as tk
pygame.init()
root = tk.Tk()
size = (root.winfo_screenwidth(), root.winfo_screenheight())  #размер экрана


def change_image(name, size):  # создаём копию изображения с отношением сторон и размерами как экран устройства
    img = Image.open(name)
    im = pygame.image.load(name)
    f_name = name
    if (im.get_size()[0], im.get_size()[1]) != size:
        img = img.resize(size, Image.ANTIALIAS)
        f_name = f'{size[0]}x{size[1]}{name}'
        img.save(f_name)
    return pygame.image.load(f_name)  # возвращаем картинку как поверхность поверхность


imgs = []  # задники
for file in os.listdir(os.getcwd()):  # смотрим какие файлы с разрешением .jpg, .png и .jpeg есть в папке с проигрывателем
    if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg'):
        imgs.append(change_image(file, size))  # и добавляем в список pygame.Surface

musics = []  # музыка
num = -1
top = -1
for file in os.listdir(os.getcwd()):  # смотрим какие файлы с разрешением .mp3 и .MP3 есть в папке с проигрывателем
    if file.endswith('.mp3') or file.endswith('.MP3'):
        musics.append(file)
        top += 1

sc = pygame.display.set_mode(size, pygame.FULLSCREEN)
number_bg = -1
timer = [0, 0, 0]
clock = pygame.time.Clock()
pause = False
done = False
while not done:
    if not pygame.mixer.music.get_busy():
        num += 1
        num = 0 if num == top+1 else top if num == -1 else num
        pygame.mixer.music.load(musics[num])  # загружаем и запускаем песню из списка
        pygame.mixer.music.play()
    if timer[1] % 5 == 0 and timer [2] == 1:  # крутим изобраения по кругу
        number_bg += 1 if number_bg != len(imgs)-1 else -number_bg
        sc.blit(imgs[number_bg], [0, 0])
        pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == 27:
                done = True
            if event.key == 32:  # на пробел остановить/продолжить воспроизведение музыки
                if pause:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()
                pause = not pause
            if event.key == 276 or event.key == 275:  # перемотка песен
                if event.key == 276:  # если влево, то отматывает на 1 назад
                    num = num-2 if num != 0 else top-1  # left
                pygame.mixer.music.stop()
    if timer[2] == 30:
        timer[1] += 1
        timer[2] = 0
    timer[2] += 1
    clock.tick(30)
pygame.quit()
