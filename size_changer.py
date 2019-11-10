from PIL import Image, ImageGrab
import os
print('выберите файл или перейдите в нужную директорию\n.. для выхода из текущей директории')
file_path = None
path = os.getcwd()
directory = path+'\\size_changer'
while file_path is None:
    print('..')
    for file in os.listdir(path):  # выводит все папки и файлы нужных типов пльзователю
        if os.path.isfile(path+'\\'+file):
            if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
                print('file   '+file)  # выводит файлы
        else:   print('dir    '+file)  # выводит папки
    while 1:  # пока введёное не существует
        file_dir = input(path+'>')
        if os.path.exists(path+'\\'+file_dir):
            if file_dir == '..':               path = os.path.dirname(path)
            else:
                path += '\\' if path[-1] != '\\' else ''
                path += file_dir
                if os.path.isfile(path):       file_path = path
            break
size = input('''введите конечный размер изображения следующим ообразом: ширина высота
введите "0 0" чтобы использовать размеры экрана устройства\n>>> ''').split(' ')
while 1:  # пока пользователь не введет два целых числа через пробел
    try:
        size = (int(size[0]), int(size[1]))
        break
    except (TypeError, ValueError) as e:       size = input('>>> ').split(' ')
    except IndexError:                         size = input('введите два целых числа через прбел\n>>> ').split(' ')
size = ImageGrab.grab().size if size == (0, 0) else size
img = Image.open(file_path).resize(size, Image.ANTIALIAS)
if not os.path.exists(directory):              os.makedirs(directory)
img.save(f'{directory}\\{size[0]}x{size[1]}{os.path.split(file_path)[-1]}')
input(f'файл создан в папке {directory}')
