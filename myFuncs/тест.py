import pygame
import os
pygame.init()

musics = []  # музыка
num = -1
for file in os.listdir(os.getcwd()):  # смотрим какие файлы с разрешением .mp3 и .MP3 есть в папке с проигрывателем
    if file.endswith('.mp3') or file.endswith('.MP3'):
        musics.append(file)
top = len(musics)-1

sc = pygame.display.set_mode((1, 1))
pause = False
done = False
if not pygame.mixer.music.get_busy():
        num += 1
        num = 0 if num == top+1 else top if num == -1 else num
        pygame.mixer.music.load(musics[num])  # загружаем и запускаем песню из списка
        pygame.mixer.music.play()
while True:
    pass
pygame.quit()
